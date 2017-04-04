packet-generation
=================

This project contain packet generation examples.

Summary
-------

1. FPM

2. CMake

### 1. FPM

The goal of fpm is to make it easy and quick to build packages such as rpms, debs, OSX packages, etc. For more informations about this project, please visit https://github.com/jordansissel/fpm

The FPM implementation use a python program, using GStreamer to display a video.

To generate the deb package, execute the packaging script inside `fpm` directory.

`$ ./package.sh`

### 2. CMake

CMake is the cross-platform, open-source make system. CMake is used to control the software compilation process using simple platform and compiler independent configuration files.

The CMake package generation use a "hello, world" C source file.

To generate the deb package, execute the following command inside `cmake` directory.

` $ cmake . && make && cpack`
