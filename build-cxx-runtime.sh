#!/usr/bin/env bash

# This script will build, install Chiakilisp C++ Runtime with library, header

# sudo is not required in Termux; its CMAKE_INSTALL_PREFIX is a bit different

if [ -d /data/data/com.termux/files/ ]; then
  PREF=/data/data/com.termux/files/usr
else
  PREF=/usr
  SUDO=sudo
fi

cd runtime \
   && mkdir -p build && cd build \
   && cmake .. -DCMAKE_INSTALL_PREFIX:PATH=$PREF && make && $SUDO make install