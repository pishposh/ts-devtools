#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from svn_checkenc import check_for_file
import sys
import os
import codecs
import re
from pprint import pprint
import xml.etree.ElementTree as ETree

CHOMP_RE = re.compile(br'(\r|\n|\r\n)$')
LINEBREAK_RE = re.compile('\r\n|\r|\n')

# TODO: MAKE EVERYTHING NOT SUCK

##  main  ####################################################################

def main():
  import subprocess
  import argparse
  
  parser = argparse.ArgumentParser()
  parser.add_argument('--svn', type=str, help="path to svn", metavar="SVN_PATH")
  parser.add_argument('--revision', '-r', type=str, default="HEAD")
  parser.add_argument('target', type=str, default=".")
  args = parser.parse_args()
  
  svn, rev, target = args.svn, args.revision, args.target
  
  # try to guess path to svnlook, if not provided:
  if svn is None and os.getenv('VISUALSVN_SERVER'):
    svn = os.getenv('VISUALSVN_SERVER') + r"\bin\svn.exe"
  if svn is None:
    svn = 'svn'
  
  errors = []
  
  svn_ls = subprocess.Popen([svn, "ls", "-R", "-r", rev, target + '@' + rev], stdout=subprocess.PIPE)
  for fname in svn_ls.stdout:
    fname = CHOMP_RE.sub(b'', fname).decode()
    if fname.endswith('/'): continue
    
    check = check_for_file(fname)
    if check is None: continue
    
    fdata = subprocess.check_output([svn, 'cat', '-r', rev, target + "/" + fname + '@' + rev])
    has_errors = False
    
    if check == 'utf8-no-bom' and fdata.startswith(codecs.BOM_UTF8):
      has_errors = True
    
    fstring = fdata.decode('utf-8', 'replace')
    
    if fstring.find("\uFFFD") != -1:
      has_errors = True
    
    if has_errors:
      blame_tree = ETree.fromstring(subprocess.check_output(
        [svn, 'blame', '--xml', '-r', rev, target + "/" + fname + '@' + rev]
      ).decode())
      
      line_num = 0
      for line in LINEBREAK_RE.split(fstring):
        line_num += 1
        
        line_rev, line_author, line_date = None, None, None
        
        commit_el = blame_tree.find('./target/entry[@line-number=\'' + str(line_num) + '\']/commit')
        if commit_el is not None:
          line_rev = commit_el.attrib['revision']
          line_author = commit_el.find('author').text
          line_date = commit_el.find('date').text
        
        if check in ('utf8-no-bom',) and line_num == 1 \
        and line.startswith(codecs.BOM_UTF8.decode('utf-8')):
          print(fname + ' (' + line_author + ' r' + line_rev + '): file starts with UTF-8 BOM')
        
        if check in ('utf8','utf8-no-bom',) and line.find("\uFFFD") != -1:
          print(fname + ':' + str(line_num) + ' (' + line_author + ' r' + line_rev + '): ' + line)
  
  
if __name__ == '__main__':
  sys.exit( main() )
  

