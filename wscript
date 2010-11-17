#! /usr/bin/env python
# coding: utf-8

import os
import os.path
import shutil
import sys

PY_MIN_VERSION = 0x020700F0
WAF_VERSION = '1.6.1'

APPNAME = 'lua'
VERSION = '5.1.4'

top = '.'
src_root = 'src'
out = 'build'

def options(opt):
    opt.load('compiler_c')

# TODO how to use for llvm-gcc, llvm-cpp which uses ar, ranlib, as,
#      windres, ld, dlltool, dllwrap, etc from MinGW binutils pkg?
def configure(conf):

    print('-> use --check-c-compiler=gcc to use gcc for compile/link')
    conf.load('compiler_c')

    conf.env.CFLAGS = [ '-O3', '-mtune=native', '-march=native' ]

    # override gcc defaults normally stored in _cache.py
    # TODO submit a patch for gcc.py
    conf.env.SHLIB_MARKER = ''         # '-Wl,-Bdynamic'
    conf.env.STLIB_MARKER = ''         # '-Wl,-Bstatic'
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
    print('[TODO] implement for Lua')
'''
    import subprocess, urllib2
    from contextlib import closing
    # download waf if not already present
    if not os.path.exists('waf'):
        with closing(urllib2.urlopen(waf['url'])) as f, open('waf', 'wb') as w:
            w.write(f.read())
        print('-> downloaded waf from %s' % waf['url'])

    # get libyaml source from SVN if local source directory (src_root) is empty
    if not os.listdir(src_root):
        if not subprocess.call('%s %s %s > NUL 2>&1' % (vcs['exe'], vcs['chk'], vcs['url']), shell=True):
            if not os.path.exists('%s/.svn' % src_root):
                if not subprocess.call([ vcs['exe'], vcs['co'], vcs['url'], src_root ]):
                    print('-> checked out libyaml source from %s' % vcs['url'])
            elif os.path.exists('%s/.svn' % src_root) and os.path.isdir('%s/.svn' % src_root):
                if not subprocess.call([ vcs['exe'], vcs['up'] ]):
                    print('-> updated libyaml source from %s' % vcs['url'])
        else:
            print('-> unable to connect to %s' % vcs['url'])
    else:
        print('-> using existing libyaml source in project directory')
'''

def _zip_extract(zip_file, item, target):
    import zipfile
    with zipfile.ZipFile(zip_file, 'r') as zip:
        zip.extract(item, target)

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

    # TODO update for Lua source
    '''
    vcs = {
            'exe' : 'svn',
            'co'  : 'co',
            'up'  : 'up',
            'chk' : 'info',
            'url' : 'http://svn.pyyaml.org/libyaml/tags/%s' % VERSION
          }
    '''

    waf = {
            'url' : 'http://waf.googlecode.com/files/waf-%s' % WAF_VERSION
          }

    task = args[1].lower()

    if task == 'prepare':
        _prepare(args)

# vim: ft=python ai ts=4 sw=4 sts=4 et
