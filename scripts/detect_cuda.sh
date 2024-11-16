#!/bin/bash

# Check for CUDA support
if command -v nvcc >/dev/null 2>&1; then
    echo "CUDA is installed."
    CUDA_ENABLED=ON
else
    echo "CUDA is not installed."
    CUDA_ENABLED=OFF
fi

# Prepare build directory
mkdir -p build && cd build

# Run CMake with the detected CUDA setting
cmake -DCMAKE_BUILD_TYPE=Release -DENABLE_CUDA=${CUDA_ENABLED} ..
make -j$(nproc) package
