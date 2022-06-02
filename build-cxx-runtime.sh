#!/usr/bin/env bash

# This script will build, install Chiakilisp C++ Runtime with library, header

# sudo is not required in Termux; its CMAKE_INSTALL_PREFIX is a bit different

# on MacOS we only allowed to write to /usr/local/ and it's fine, as it works

if [ -d /data/data/com.termux/files/ ]; then
  PREF=/data/data/com.termux/files/usr
elif [ "$(uname)" == "Darwin" ]; then
  PREF=/usr/local
  SUDO=sudo
else
  PREF=/usr
  SUDO=sudo
fi

cd runtime \
   && mkdir -p build && cd build \
   && cmake .. -DCMAKE_INSTALL_PREFIX:PATH=$PREF && make && $SUDO make install