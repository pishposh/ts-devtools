#!/usr/local/bin/python
#
# Quick and dirty script to guess the character encodings of text files
# (passed in as arguments) using various techniques.
#
# Assumes 'chardet' module installed (pip install chardet), also assumes
# 'file' utility available at /usr/bin/file.

import sys
import chardet
import codecs
import re
import signal
from multiprocessing import Pool, cpu_count
from subprocess import Popen, PIPE

BOMS = {
    codecs.BOM_UTF8:     'UTF-8 BOM',
    codecs.BOM_UTF16_BE: 'UTF-16be BOM',
    codecs.BOM_UTF16_LE: 'UTF-16le BOM',
    codecs.BOM_UTF32_BE: 'UTF-32be BOM',
    codecs.BOM_UTF32_LE: 'UTF-32le BOM'
}

CR   = re.compile(r'\r(?!\n)')
LF   = re.compile(r'(?<!\r)\n')
CRLF = re.compile(r'\r\n')

UTF8_DECODER = codecs.getdecoder("utf-8")


def sniff(filename):
    try:
        result = { 'filename': filename, 'guessed_mimetype': None,
                   'utf8_decode_err': None, 'bom': None,
                   'chardet_encoding': None, 'chardet_confidence': None,
                   'chardet_decode_err': None, 'line_endings': None }
        
        with open(filename,'rb') as f: data = f.read()
        
        # attempt decoding as utf-8:
        
        utf8_string = None
        
        try:
            utf8_string = UTF8_DECODER(data)[0]
        except UnicodeError as e:
            result['utf8_decode_err'] = str(e)
        
        # check for Unicode BOM:
        
        for b, bname in BOMS.items():
            if data.startswith(b):
                result['bom'] = bname
                break
        
        # use /usr/bin/file to guess mime type:
        
        if len(data) != 0:
            p = Popen(['/usr/bin/file', '-bI', '-'], stdin=PIPE, stdout=PIPE)
            result['guessed_mimetype'] = p.communicate(data)[0].strip()
        else:
            result['guessed_mimetype'] = "application/x-empty; charset=binary"
        
        result['chardet_encoding'] = '-'
        result['chardet_confidence'] = 0
        chardet_string = None
        
        # use Mozilla's universal charset detector to guess encoding:
        
        chardet_result = chardet.detect(data)
        result['chardet_encoding'] = chardet_result['encoding']
        result['chardet_confidence'] = chardet_result['confidence']
        
        # attempt decoding as Mozilla's guessed charset:
        
        chardet_string = None
        
        if chardet_result['encoding'] is not None:
           try:
               chardet_decoder = codecs.getdecoder(chardet_result['encoding'])
               
               if chardet_decoder is UTF8_DECODER:
                   result['chardet_decode_err'] = result['utf8_decode_err']
                   chardet_string = utf8_string
                   
               else:
                   try:
                       chardet_string = chardet_decoder(data)[0]
                   except UnicodeError as e:
                       result['chardet_decode_err'] = str(e)
                       
           except LookupError as e:
               result['chardet_decode_err'] = str(e)
            
        # detect line endings:
        
        string = utf8_string or chardet_string # assume utf-8 if at all possible
        if string is not None:
            line_endings = []
            if CR.search(string):   line_endings.append('CR')
            if LF.search(string):   line_endings.append('LF')
            if CRLF.search(string): line_endings.append('CRLF')
            result['line_endings'] = ", ".join(line_endings)
        
        return result
        
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    pool = Pool(processes=cpu_count())
    results = [pool.apply_async(sniff, [filename]) for filename in sys.argv[1:]]
    
    try:
        for r in results:
            result = r.get()
            print "\t".join([result['filename'],
                             result['utf8_decode_err'] or '',
                             result['bom'] or '',
                             result['guessed_mimetype'],
                             result['chardet_encoding'] or '',
                             ("%f" % result['chardet_confidence']),
                             result['chardet_decode_err'] or '',
                             result['line_endings'] or ''])
            sys.stdout.flush()
        
    except KeyboardInterrupt:
        pool.terminate()
        pool.join()
        