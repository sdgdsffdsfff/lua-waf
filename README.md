## What

A single-file build script using the Python-based [Waf](http://code.google.com/p/waf) tool that
downloads the Lua source and quickly builds the Lua binaries for use on Windows systems.

## Prerequisites

* Python 2.7
* MinGW or similar build environment
* Live internet connection if Lua source not locally available

## Usage

1.  ensure the MinGW toolchain is on your `PATH`
2. download the `wscript` build file ([zipball](http://github.com/jonforums/liblua-waf/zipball/master)) into `<your_build_dir>`
3. `cd <your_build_dir>`
4. *[optional]* `python wscript prepare` (if source not already in `<your_build_dir>/src`)
5. `python waf configure --check-c-compiler=gcc`
6. `python waf` (just build)
7. `python waf build package` (build and zip the dll, static library, headers, def, and implib)

## TODO

* add build code for `luac.exe` Lua compiler
* add `clobber` task
* add `test` task
* add `llvm-gcc` compiler support
* add binary downloads
* refactor to support both MinGW and MSVC toolchains
