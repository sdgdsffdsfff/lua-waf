#! /usr/bin/env python
# coding: utf-8

import os
import os.path
import shutil
import sys

PY_MIN_VERSION = 0x020700F0
WAF_VERSION = '1.6.1'
BSDTAR_FILE = 'basic-bsdtar-2.8.3-1-mingw32-bin.zip'

APPNAME = 'lua'
VERSION = '5.1.4'

top = '.'
src_root = 'src'
out = 'build'
utils_root = 'utils'

def options(opt):
    opt.load('compiler_c')

# TODO how to use for llvm-gcc, llvm-cpp which uses ar, ranlib, as,
#      windres, ld, dlltool, dllwrap, etc from MinGW binutils pkg?
def configure(conf):

    print('-> use --check-c-compiler=gcc to use gcc for compile/link')
    conf.load('compiler_c')

    conf.env.CFLAGS = [ '-O3', '-mtune=native', '-march=native' ]

    # override gcc defaults normally stored in _cache.py
    conf.env.SHLIB_MARKER = ''  # '-Wl,-Bdynamic'
    conf.env.STLIB_MARKER = ''  # '-Wl,-Bstatic'
    conf.env.CFLAGS_cshlib = [ '-Wall', '-O3', '-mtune=native', '-march=native' ]   # ['-DDLL_EXPORT']

def build(bld):
    lib_sources = bld.path.ant_glob(
                    '%s/l*.c' % src_root,
                    excl=[ '%s/lua.c' % src_root, '%s/luac.c' % src_root ]
                    )

    # create yaml.dll and its import lib and def files
    # TODO genericize the version numbers
    bld.shlib(
        source = lib_sources,
        target = 'lua51',
        linkflags = '-Wl,--output-def,liblua51.def',
        defines = [ 'LUA_BUILD_AS_DLL' ],
        )

    # create Lua interpreter
    # TODO genericize the version numbers
    bld.program(
        source = '%s/lua.c' % src_root,
        target = 'lua',
        defines = [ 'LUA_BUILD_AS_DLL' ],
        use = 'lua51',
        )

# TODO genericize the version numbers
def package(ctx):
    import zipfile
    with zipfile.ZipFile('%s-%s.zip' % (APPNAME, VERSION), 'w', zipfile.ZIP_DEFLATED) as zip:
        for f in ['build/liblua51.def', 'build/lua51.dll', 'build/lua.exe']:
            zip.write(f, 'bin/%s' % os.path.basename(f))
        zip.write('%s/lua.h' % src_root, 'include/lua.h')
        zip.write('%s/lualib.h' % src_root, 'include/lualib.h')
        zip.write('%s/lauxlib.h' % src_root, 'include/lauxlib.h')
        zip.write('build/liblua51.dll.a', 'lib/liblua51.dll.a')

# TODO update this for downloading Lua source code
def _prepare(args):

    import urllib2
    from contextlib import closing

    # download utilities if not already present
    if not os.path.exists(utils_root):
        with closing(urllib2.urlopen(bsdtar['url'])) as f, open(bsdtar['local_name'], 'wb') as b:
            b.write(f.read())
        print('-> downloaded basic-bsdtar from %s' % bsdtar['url'])
        _zip_extract(bsdtar['local_name'], bsdtar['exe'], utils_root)

    # download and extract Lua source if local source directory (src_root) is empty
    if not os.path.exists(src_root) or not os.listdir(src_root):
        with closing(urllib2.urlopen(lua['url'])) as f, open(lua['local_name'], 'wb') as u:
            u.write(f.read())
        print('-> downloaded Lua source from %s' % lua['url'])
        _bsdtar_extract(lua['local_name'])

    else:
        print('-> using existing Lua source in project directory')

    # download waf if not already present
    if not os.path.exists('waf'):
        with closing(urllib2.urlopen(waf['url'])) as f, open('waf', 'wb') as w:
            w.write(f.read())
        print('-> downloaded waf from %s' % waf['url'])


def _zip_extract(zip_file, item, target):
    import zipfile
    with zipfile.ZipFile(zip_file, 'r') as zip:
        zip.extract(item, target)
    print('-> extracted %s from %s into %s' % (item, zip_file, target))

def _bsdtar_extract(archive, strip_count=1):
    import subprocess
    cmd = '-x --strip-components %s --include="*/src" --include="*/etc"' % strip_count
    if not subprocess.call(r'%s\%s %s -f %s' % (utils_root, bsdtar['exe'], cmd, lua['local_name']), shell=True):
        pass
    else:
        pass


if __name__ == '__main__':
    if sys.hexversion < PY_MIN_VERSION:
        print('At least Python v%d.%d.%d required, exiting...' % (
                (PY_MIN_VERSION & 0xF000000) >> 24,
                (PY_MIN_VERSION & 0x00F0000) >> 16,
                (PY_MIN_VERSION & 0x0000F00) >> 8))
        sys.exit(1)

    args = sys.argv

    TASKS = ('prepare',)
    USAGE = '''usage: python wscript TASK [OPTION]

where TASK is one of:
  prepare   prepare current dir for building Lua
'''

    if len(args) != 2 or args[1].lower() not in TASKS:
        print(USAGE)
        sys.exit(1)

    bsdtar = {
                'url' : 'http://downloads.sourceforge.net/mingw/%s' % BSDTAR_FILE,
                'local_name' : 'basic-bsdtar.zip',
                'exe' : 'basic-bsdtar.exe',
             }

    lua = {
            'url' : 'http://www.lua.org/ftp/lua-%s.tar.gz' % VERSION,
            'local_name' : 'lua-%s.tar.gz' % VERSION,
          }

    waf = {
            'url' : 'http://waf.googlecode.com/files/waf-%s' % WAF_VERSION,
          }

    task = args[1].lower()

    if task == 'prepare':
        _prepare(args)

# vim: ft=python ai ts=4 sw=4 sts=4 et
