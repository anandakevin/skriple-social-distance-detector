FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    libopencv-dev \
    cmake \
    wget

# Install CUDA (optional, based on machine configuration)
RUN if lspci | grep -i nvidia; then \
        wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-repo-ubuntu2204_12.0.1-1_amd64.deb && \
        dpkg -i cuda-repo-ubuntu2204_12.0.1-1_amd64.deb && \
        apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/3bf863cc.pub && \
        apt-get update && apt-get install -y cuda; \
    fi

# Clone and build Darknet
WORKDIR /darknet
RUN git clone https://github.com/hank-ai/darknet.git /darknet
COPY build_darknet.sh /darknet/build_darknet.sh
RUN chmod +x build_darknet.sh && ./build_darknet.sh

# Package and deploy Darknet
CMD ["/usr/bin/darknet", "version"]
