#! /usr/bin/env python

import sys, shutil, os, tempfile
from cStringIO import StringIO

TIMEOUT = 5
SANDBOX_BIN = '/opt/pypy-sandbox/pypy/translator/goal/pypy-c'
sys.path += [ '/opt/pypy-sandbox']
tempfile.tempdir = '/tmp/ramdisk/virtualtmp/'
# import pypy now that it's added to the path
from pypy.translator.sandbox import pypy_interact

def exec_sandbox(code):
    try:
        tmpdir = tempfile.mkdtemp()
        tmpscript = open(os.path.join(tmpdir, "script.py"),'w')
        tmpscript.write(code)
        tmpscript.close()
        sandproc = pypy_interact.PyPySandboxedProc(
            SANDBOX_BIN,
            #['-c', code]
            ['/tmp/script.py','--timeout',str(TIMEOUT),],
           tmpdir
        )
        try:
            code_output = StringIO()
            code_log = StringIO()
            sandproc.interact(stdout=code_output, stderr=code_log)
            return code_output.getvalue(), code_log.getvalue()
        except Exception, e:
            sandproc.kill()
        finally:
            sandproc.kill()

        shutil.rmtree(tmpdir)
    except Exception, e:
        pass
    return 'Error, could not evaluate', e

print exec_sandbox("print 'hi there'")
