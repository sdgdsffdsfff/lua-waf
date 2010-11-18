## Prerequisites

* Python 2.7
* MinGW or similar build environment
* Live internet connection if Lua source not locally available

## Usage

1. download the `wscript` build file ([zipball](http://github.com/jonforums/liblua-waf/zipball/master)) into `<your_build_dir>`
2. `cd <your_build_dir>`
3. *[optional]* `python wscript prepare` (if source not already in `<your_build_dir>/src`)
4. `python waf configure --check-c-compiler=gcc`
5. `python waf` (just build)
6. `python waf build package` (build and zip the dll, static library, headers, def, and implib)

## TODO

* add build code for `luac.exe` Lua compiler
* add `lua.hpp` header to zip package's `include` directory
* add `clobber` task
* add `llvm-gcc` compiler support
