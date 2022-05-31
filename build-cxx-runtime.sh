#!/usr/bin/env bash

# This script will build, install Chiakilisp C++ Runtime with library/header

cd runtime \
   && mkdir -p build && cd build \
   && cmake .. -DCMAKE_INSTALL_PREFIX:PATH=/usr && make && sudo make install