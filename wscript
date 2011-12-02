#! /usr/bin/env python
# coding: utf-8

import os
import os.path
import shutil
import sys

PY_MIN_VERSION = (2, 7, 0)
WAF_VERSION = '1.6.9'
BSDTAR_FILE = 'basic-bsdtar-2.8.3-1-mingw32-bin.zip'

APPNAME = 'lua'
VERSION = '5.2.0-rc4'
MAJOR_MINOR = VERSION.translate(None, '.')[:2]

top = '.'
src_root = 'src'
out = 'build'
utils_root = 'utils'

def options(opt):
    opt.load('compiler_c')
    opt.add_option('--arch', action='store', default='x86',
       help='Select target architecture (ia64, x64, x86, x86_amd64, x86_ia64)')

# TODO how to use for llvm-gcc, llvm-cpp which uses ar, ranlib, as,
#      windres, ld, dlltool, dllwrap, etc from MinGW binutils pkg?
def configure(conf):
    conf.load('compiler_c')

    # override gcc defaults stored in _cache.py
    if conf.env.CC_NAME in ('gcc'):
        conf.env.SHLIB_MARKER = ''     # '-Wl,-Bdynamic'
        conf.env.STLIB_MARKER = ''     # '-Wl,-Bstatic'
        conf.env.CFLAGS_cshlib = ['']  # ['-DDLL_EXPORT']
        conf.env.LINKFLAGS = ['']      # ['-Wl,--enable-auto-import']

def build(bld):
    lib_sources = bld.path.ant_glob(
                    '%s/l*.c' % src_root,
                    excl=[ '%s/lua.c' % src_root, '%s/luac.c' % src_root ]
                    )

    if bld.env.CC_NAME == 'msvc':
        my_cflags = [ '/O2', '/W2', '/MD' ]
        my_dll_lflags = []
        my_exe_lflags = []
        my_static_exe_lflags = []
        bld.env.STLIB_ST = '%s-static.lib'
        bld.env.cstlib_PATTERN = '%s-static.lib'
    else:
        my_cflags = [ '-Wall', '-O3', '-mtune=native', '-march=native' ]
        my_dll_lflags = [ '-Wl,--output-def,liblua%s.def' % MAJOR_MINOR ]
        my_exe_lflags = [ '-s' ]
        my_static_exe_lflags = [ '-static', '-s' ]

    # create luaXY.dll and its import lib and def files
    bld.shlib(
        source = lib_sources,
        target = 'lua%s' % MAJOR_MINOR,
        cflags = my_cflags,
        linkflags = my_dll_lflags,
        defines = [ 'LUA_BUILD_AS_DLL' ],
        name = 'shared-lua',
        )

    # create static liblua.a
    bld.stlib(
        source = lib_sources,
        target = 'lua%s' % MAJOR_MINOR,
        cflags = my_cflags,
        name = 'static-lua',
        )

    # create Lua interpreter
    bld.program(
        source = '%s/lua.c' % src_root,
        target = 'lua',
        cflags = my_cflags,
        linkflags = my_exe_lflags,
        defines = [ 'LUA_BUILD_AS_DLL' ],
        use = 'shared-lua',
        )

    # create Lua compiler
    bld.program(
        source = [ '%s/luac.c' % src_root ],
        target = 'luac',
        cflags = my_cflags,
        linkflags = my_static_exe_lflags,
        use = 'static-lua',
        )

def package(ctx):
    '''package built Lua into a zip file'''
    import zipfile
    with zipfile.ZipFile('%s-%s.zip' % (APPNAME, VERSION), 'w', zipfile.ZIP_DEFLATED) as zip:
        for f in [ 'build/lua%s.dll' % MAJOR_MINOR, 'build/lua.exe', 'build/luac.exe' ]:
            zip.write(f, 'bin/%s' % os.path.basename(f))
        for f in [ '%s/lua.h', '%s/luaconf.h', '%s/lualib.h', '%s/lauxlib.h', '%s/lua.hpp' ]:
            zip.write(f % src_root, 'include/%s' % os.path.basename(f))
        #zip.write('etc/lua.hpp', 'include/lua.hpp')
        for f in [ 'build/liblua%s.dll.a' % MAJOR_MINOR,
                   'build/liblua%s.def' % MAJOR_MINOR,
                   'build/liblua%s.a' % MAJOR_MINOR ]:
            zip.write(f, 'lib/%s' % os.path.basename(f))


# helper functions
def _prepare(args):

    import urllib2
    from contextlib import closing

    # download utilities if not already present
    if not os.path.exists(utils_root):
        with closing(urllib2.urlopen(bsdtar.url)) as f, open(bsdtar.local_name, 'wb') as b:
            b.write(f.read())
        print('-> downloaded basic-bsdtar from %s' % bsdtar.url)
        _zip_extract(bsdtar.local_name, bsdtar.exe, utils_root)

    # download and extract Lua source if local source directory (src_root) is empty
    if not os.path.exists(src_root) or not os.listdir(src_root):
        with closing(urllib2.urlopen(lua.url)) as f, open(lua.local_name, 'wb') as u:
            u.write(f.read())
        print('-> downloaded Lua source from %s' % lua.url)
        _bsdtar_extract(lua.local_name, 1, '*/src')
    else:
        print('-> using existing Lua source in project directory')

    # download waf if not already present and make executable if not on Windows
    if not os.path.exists('waf'):
        with closing(urllib2.urlopen(waf.url)) as f, open('waf', 'wb') as w:
            w.write(f.read())
        if not hasattr(sys, 'winver'):
            os.chmod('waf', 0755)
        print('-> downloaded waf from %s' % waf.url)
    else:
        print('-> nothing to download; using existing waf library')


def _zip_extract(zip_file, item, target):
    import zipfile
    with zipfile.ZipFile(zip_file, 'r') as zip:
        zip.extract(item, target)
    print('-> extracted %s from %s into %s' % (item, zip_file, target))

def _bsdtar_extract(archive, strip_count, *args):
    import subprocess

    exe = r'%s\%s' % (utils_root, bsdtar.exe)
    cmd = '-x --strip-components %s ' % strip_count
    for a in args:
        cmd += '--include="%s" ' % a

    if not subprocess.call(r'%s %s -f %s' % (exe, cmd, archive), shell=True):
        print('-> extracted from %s' % archive)
    else:
        print('-> unable to extract from %s' % archive)


if __name__ == '__main__':
    if sys.version_info < PY_MIN_VERSION:
        print('At least Python v%d.%d.%d required, exiting...' %
            (PY_MIN_VERSION[0], PY_MIN_VERSION[1], PY_MIN_VERSION[2]))
        sys.exit(1)

    class ResourceInfo(object):
        def __init__(self, **kwargs):
            for i in kwargs.iteritems():
                setattr(self, i[0], i[1])

    args = sys.argv[:]

    TASKS = ('prepare',)
    USAGE = '''usage: python wscript TASK [OPTION]

where TASK is one of:
  prepare   prepare current dir for building Lua
'''

    if len(args) != 2 or args[1].lower() not in TASKS:
        print(USAGE)
        sys.exit(1)

    bsdtar = ResourceInfo(
        url = 'http://downloads.sourceforge.net/mingw/%s' % BSDTAR_FILE,
        local_name = 'basic-bsdtar.zip',
        exe = 'basic-bsdtar.exe'
        )

    url_base = 'http://www.lua.org/ftp' if len(VERSION.split('-')) == 1 else 'http://www.lua.org/work'
    lua = ResourceInfo(
        url = '%s/lua-%s.tar.gz' % (url_base, VERSION),
        local_name = 'lua-%s.tar.gz' % VERSION
        )

    waf = ResourceInfo(
        url = 'http://waf.googlecode.com/files/waf-%s' % WAF_VERSION
        )

    task = args[1].lower()

    if task == 'prepare':
        _prepare(args)

# vim: ft=python ai ts=4 sw=4 sts=4 et
