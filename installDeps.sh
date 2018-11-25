#!/bin/bash

git clone https://github.com/rogersce/cnpy.git
mkdir cnpy/bin
cd cnpy/bin
cmake ..
make
make install
