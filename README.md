## What

A single-file build script using the Python-based [Waf](http://code.google.com/p/waf) tool that
downloads the Lua source and quickly builds the Lua binaries for use on Windows systems.

## Prerequisites

* Python 2.7
* A zip extraction utility such as [7-Zip](http://www.7-zip.org/)
* MinGW, VC++, or Windows SDK build environment
* Live internet connection if Lua source or the [Waf](http://code.google.com/p/waf/)
  cross-platform build tool haven't already been downloaded

## Usage

1. When building with VC++ or the Windows SDK, waf will select the build environment
   based upon it's `--msvc_version` and `--msvc_targets` command line options. When
   building with a MinGW toolchain, ensure it's on your `PATH` and use waf's
   `--check-c-compiler` command line option. If you choose to build with MinGW, I
   encourage you to use the [DevKit](https://github.com/oneclick/rubyinstaller/wiki/Development-Kit).
   While my instructions and install script at that link are specific to Ruby, you
   can simply run the `devkitvars.bat` or `devkitvars.ps1` scripts to bring the
   DevKit onto `PATH` and use it as a general purpose GCC-based build toolchain.
2. Download the `wscript` build file ([zipball](http://github.com/jonforums/lua-waf/zipball/master))
   into `<your_build_dir>`
3. `cd <your_build_dir>`
4. *[optional]* `python wscript prepare` (if waf and Lua source not already in `<your_build_dir>/src`)
5. **Windows SDK:** `python waf configure --msvc_version="wsdk 7.1" --msvc_targets="x86"` or
   **MinGW:** `python waf configure --check-c-compiler=gcc`
6. `python waf` to build
7. `python waf clean build` to rebuild
8. `python waf build package` (build and zip the dll, static library, headers, def, and implib)
9. `python waf distclean` to remove the build directory and build lock files
10. `python wscript pristine` to delete all downloaded and built artifacts

## TODO

* add `test` task
* add binary downloads
