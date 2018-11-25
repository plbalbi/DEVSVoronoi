#!/bin/bash

git clone git@github.com:rogersce/cnpy.git
mkdir cnpy/bin
cd cnpy/bin
cmake ..
make
make install
