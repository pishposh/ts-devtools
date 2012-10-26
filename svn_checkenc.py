#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

PATHS = [
  # ignore third-party sources:
  (r'^vendor/', ''),
  
  # ignore jscalendar:
  (r'(^|/)jscalendar-1\.0/', ''),
  
  # ignore CKEditor lang files:
  (r'(^|/)(editor|[^/]*CKEditor[^/]*)/(_source/)?lang/[^/]+\.js$', ''),
  
  # ignore WebMarker help files:
  (r'(^|/)WebMarker/WebHelp/', ''),
  
  # ignore AspSite /main/neweb/... static files with Windows-1252 meta charset tag:
  (r'(^|/)main/neweb/.*\.html?$', ''),
  
  # ignore JSSpellChecker (VBScript.Encode):
  (r'(^|/)JSSpellChecker/ServerEngine\.asp$', ''),
  
  # ignore outdated JQuery UI:
  (r'(^|/)JQueryUI/development-bundle/', ''),
  
  # these get re-encoded automatically (from Windows-1252) by the ASP.NET interpreter:
  (r'^Projects/.*\.(aspx|cshtml)$', ''),
  
  # I think these things under /Site/Scripts/ get concatenated together with a BOM-aware
  # file reader (TODO: verify this):
  (r'^Projects/Site/(trunk|branches/[^/]+|tags/[^/]+)/Site/Scripts/(TS|Base)/.*\.js$', 'utf8'),
  
  # # ASP interpreter treats BOM as equivalent to <%@ CodePage=65001 %> directive, so it's
  # # okay for some classic ASP files to have a BOM:
  # (r'\.(asp|ashx)$', 'utf8'),
  # NO. This is confusing, disallow it.
  
  # check for utf-8 and disallow BOM on these filetypes:
  (r'\.(asp|ashx|aspx|cshtml|html|htm|js|css|txt|text|csv)$', 'utf8-no-bom'),
]

EMAIL_FROM = '"SVN Monitor" <svnmonitor@taskstream.com>'
EMAIL_REPLY_TO = 'kkaji@taskstream.com'

ERRORS_HTML = """\
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title></title>
  <style>

body {{
  font-family: "Helvetica Neue", Helvetica, Arial;
}}

.initial {{ margin-top: 0 }} /* damn Outlook for using Word as its HTML renderer */

.errors {{
  margin: 1em 0;
  font-size: smaller;
}}

.error {{ margin: 0.5em 0; }}

.fname, .lnum, .code {{
  font-family: Menlo, Consolas, Monaco, "Courier New", Courier, monospace;
}}

.code {{
  color: #999;
  white-space: pre-wrap;
  word-wrap: break-word;
}}

.bad {{ color: red }}

  </style>
</head>
<body>
  <p class="initial">
    <strong>{author}</strong> committed new text to <strong>{project_name}</strong>
    (revision <strong>{revision}</strong>) with these UTF-8 encoding issue(s):
  </p>
  
  <div class="errors">
{errors}
  </div>
</body>
</html>
"""

ERROR_FILE_HTML = """\
    <div class="error">
      <span class="fname">{fname}:</span>
      <span class="desc">{desc}</desc>
    </div>
"""

ERROR_LINE_HTML = """\
    <div class="error">
      <span class="fname">{fname}:</span><span class="lnum">{lnum}:</span>
      <span class="code">{code}</span>
    </div>
"""


import sys
import os
import codecs
import re
from pprint import pprint


def check_for_file( fname ):
  for (pattern, check) in PATHS:
    if re.search( pattern, fname, re.IGNORECASE ):
      if check == '':
        return None
      else:
        return check
  return None


def get_errors( diffproc_stdout ):
  errors = []
  
  fname = ''
  fcheck = ''
  line_num = None
  
  CHOMP_RE = re.compile(br'(\r|\n|\r\n)$')
  FILENAME_RE = re.compile(br'^\w+: (.*)$')
  LINENUM_RE = re.compile(br'^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@$')
  COMMONLINE_RE = re.compile(br'^ ')
  ADDEDLINE_RE = re.compile(br'^\+(.*?)$')
  
  for diffline in diffproc_stdout:
    
    # chomp CR, LF, or CRLF:
    diffline = CHOMP_RE.sub(b'', diffline)
    # pprint( diffline )
    
    m = FILENAME_RE.search(diffline)
    if m:
      fname = m.group(1).decode('utf-8')
      fcheck = check_for_file( fname )
      line_num = None
      # pprint( (fcheck, fname) )
      continue
    
    if fcheck is None: continue
    
    m = LINENUM_RE.search(diffline)
    if m:
      line_num = int( m.group(1).decode('utf-8') )
      continue
    
    if line_num is None: continue
    
    # Lines in common are counted in line numbering, so increment our line number:
    m = COMMONLINE_RE.search(diffline)
    if m:
      line_num += 1
      continue
      
    m = ADDEDLINE_RE.search(diffline)
    if m:
      data = m.group(1)
      
      if line_num == 1 and fcheck in ('utf8-no-bom',) and data.startswith(codecs.BOM_UTF8):
        errors.append( (fname, None, "file begins with UTF-8 BOM") )
      
      if fcheck in ('utf8','utf8-no-bom',):
        # HACK: This will report false positives wherever the Unicode replacement
        # character (U+FFFD) is being used on purpose. In TaskStream code, hopefully,
        # this will happen rarely or never.
        string = data.decode('utf-8', 'replace')
        if string.find("\uFFFD") != -1: # U+FFFD = Unicode replacement char
          errors.append( (fname, line_num, string) )
          
      # pprint((line_num,data))
      line_num += 1
      continue
  
  return errors


##  main  ####################################################################

def main():
  import subprocess
  import email
  import smtplib
  from email.mime.multipart import MIMEMultipart
  from email.mime.text import MIMEText
  import cgi
  import argparse
  
  parser = argparse.ArgumentParser()
  parser.add_argument( 'repo_path', type=str )
  parser.add_argument( 'revision_num', type=str )
  parser.add_argument( '--project-name', type=str )
  parser.add_argument( '--svnlook', type=str, help="path to svnlook",
                          metavar="SVNLOOK_PATH" )
  parser.add_argument( '--dump-html', '--html', action='store_true',
                          help="write html to stdout" )
  parser.add_argument( '--email-to', '-e', action='append', type=str )
  parser.add_argument( '--smtp-host', type=str, default='localhost' ) # qa-smtp1.TS.com
  parser.add_argument( '--smtp-username', type=str, default='' )
  parser.add_argument( '--smtp-password', type=str, default='' )
  parser.add_argument( '--smtp-ssl', action='store_true' )
  args = parser.parse_args()
  
  repo_path, rev, project_name, svnlook = \
    args.repo_path, args.revision_num, args.project_name, args.svnlook
  
  # try to guess path to svnlook, if not provided:
  if svnlook is None and os.getenv('VISUALSVN_SERVER'):
    svnlook = os.getenv('VISUALSVN_SERVER') + r"\bin\svnlook.exe"
  if svnlook is None:
    svnlook = 'svnlook'
  
  # use last component of repository path for project name:
  if project_name is None:
    project_name = os.path.basename( os.path.normpath( repo_path ) )
  
  # read line by line so we don't blow up on large commits:
  diffproc = subprocess.Popen(
    [svnlook, 'diff', repo_path, '-r', rev, '--diff-copy-from', '--no-diff-deleted'],
    stdout = subprocess.PIPE
  )
  errors = get_errors( diffproc.stdout )
  
  if errors:
    email_to, smtp_host, dump_html = args.email_to, args.smtp_host, args.dump_html
    
    # build and send email if able:
    if (email_to and smtp_host) or dump_html:
      smtp_ssl, smtp_username, smtp_password = \
        args.smtp_ssl, args.smtp_username, args.smtp_password
      
      error_list_html = ""
      
      for fname, lnum, string in errors:
        
        if lnum is None:
          error_list_html += ERROR_FILE_HTML.format( fname = cgi.escape(fname),
                                                      desc = cgi.escape(string) )
        
        else:
          error_list_html += ERROR_LINE_HTML.format(
            fname = cgi.escape(fname),
             lnum = cgi.escape(str(lnum)),
             code = cgi.escape(
                      string.strip().replace("\t", " ")
                    ).replace("\uFFFD", "<span class=\"bad\">?</span>")
          )                   # HACK, false positives, etc. (see above)
      
      author = subprocess.check_output(
        [svnlook, 'author', repo_path, '-r', rev]
      ).decode('utf-8').strip()
      
      html = ERRORS_HTML.format(       author = cgi.escape(author),
                                 project_name = cgi.escape(project_name),
                                     revision = cgi.escape(rev),
                                       errors = error_list_html )
      
      if (dump_html):
        print( html )
      else:
        msg = MIMEText(html, 'html', 'utf-8')
        msg['Subject'] = "Warning: {0} committed bad UTF-8 to {1} (r{2})".format(
                                                            author, project_name, rev)
        msg['To'] = ', '.join(email_to)
        msg['From'] = EMAIL_FROM
        msg['Sender'] = EMAIL_FROM
        msg['Reply-To'] = EMAIL_REPLY_TO #msg.add_header('Reply-To', EMAIL_REPLY_TO)
        
        server = smtplib.SMTP( smtp_host )
        if smtp_ssl:
          server.starttls()
        if (smtp_username or smtp_password):
          server.login( smtp_username, smtp_password )
        server.send_message( msg )
        server.quit()
    
    else: # no email specified, dump errors to stdout
      if sys.stdout.encoding != 'UTF-8':
        sys.stdout = codecs.getwriter(sys.stdout.encoding)(sys.stdout.buffer, 'replace')
        sys.stderr = codecs.getwriter(sys.stderr.encoding)(sys.stderr.buffer, 'replace')
        # python defaults can DIAF, so too can windows
      
      for fname, lnum, string in errors:
        if lnum is None:
          print( "{0}: {1}".format(fname, string) )
        else:
          print( "{0}:{1}: {2}".format(fname, lnum, string) )
        
  return 0
  
if __name__ == '__main__':
  sys.exit( main() )
  

