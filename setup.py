from distutils.core import setup
import py2exe
setup(windows=[{"script":"core.py"}], options={"py2exe":{"includes":["sip", "psycopg2"], "packages":["sqlalchemy.dialects.postgresql"], 'bundle_files':1, 'dll_excludes':['w9xpopen.exe', 'msvcr71.dll', "IPHLPAPI.DLL", "NSI.dll",  "WINNSI.DLL",  "WTSAPI32.dll"]}})
