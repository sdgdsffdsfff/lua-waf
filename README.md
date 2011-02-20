## What

A single-file build script using the Python-based [Waf](http://code.google.com/p/waf) tool that
downloads the Lua source and quickly builds the Lua binaries for use on Windows systems.

## Prerequisites

* Python 2.7
* MinGW or similar build environment
* Live internet connection if Lua source not locally available

## Usage

1. Ensure a MinGW toolchain is on your `PATH`. Windows users are encouraged to use the
   [DevKit](http://github.com/oneclick/rubyinstaller/wiki/Development-Kit). While my
   instructions and install script are specific to Ruby, you can simply run the
   `devkitvars.bat` or `devkitvars.ps1` scripts to bring the toolchain onto `PATH`
   and use it as a general purpose GCC-based build toolchain.
2. Download the `wscript` build file ([zipball](http://github.com/jonforums/liblua-waf/zipball/master)) into `<your_build_dir>`
3. `cd <your_build_dir>`
4. *[optional]* `python wscript prepare` (if source not already in `<your_build_dir>/src`)
5. `python waf configure --check-c-compiler=gcc`
6. `python waf` (just build)
7. `python waf build package` (build and zip the dll, static library, headers, def, and implib)

## TODO

* add `clobber` task
* add `test` task
* add `llvm-gcc` compiler support
* add binary downloads
* refactor to support both MinGW and MSVC toolchains
