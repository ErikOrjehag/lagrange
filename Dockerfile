
FROM athackst/ros2:galactic-gazebo-nvidia

ARG USERNAME=ros
ARG WORKSPACE=/home/${USERNAME}

ENV HOME=/home/${USERNAME}
ENV WS=${WORKSPACE}
ENV DEPENDENCIES_WS /opt/dependencies_ws

ENV DEBIAN_FRONTEND=dialog
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES graphics,utility,compute
ENV QT_X11_NO_MITSHM=1

# Install additional dependencies
RUN apt-get update && \
    apt-get install -y -qq --no-install-recommends \
        software-properties-common \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y -qq --no-install-recommends \
        cmake \
        g++ \
        git \
#        ipython \
        minizip \
#        python-dev \
#        python-h5py \
#        python-numpy \
#        python-scipy \
#        python-sympy \
#        qt4-dev-tools \
        # openrave
        libassimp-dev \
        libavcodec-dev \
        libavformat-dev \
        libavformat-dev \
        libboost-all-dev \
        libboost-date-time-dev \
        libbullet-dev \
        libfaac-dev \
        libglew-dev \
        libgsm1-dev \
        liblapack-dev \
        liblog4cxx-dev \
        libmpfr-dev \
        libode-dev \
        libogg-dev \
        libpcrecpp0v5 \
        libpcre3-dev \
        libqhull-dev \
#        libqt4-dev \
#        libsoqt-dev-common \
#        libsoqt4-dev \
        libswscale-dev \
        libswscale-dev \
        libvorbis-dev \
        libx264-dev \
        libxml2-dev \
        libxvidcore-dev \
        # open scene graph
        libcairo2-dev \
#        libjasper-dev \
        libpoppler-glib-dev \
        libsdl2-dev \
        libtiff5-dev \
        libxrandr-dev \
        # flexible collision library
        libccd-dev \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# collada dom
RUN git clone https://github.com/rdiankov/collada-dom.git \
    && cd collada-dom \
    && mkdir build \
    && cd build \
    && cmake .. \
    && make -j4 \
    && sudo make install

# open scena graph
RUN git clone --branch OpenSceneGraph-3.4 https://github.com/openscenegraph/OpenSceneGraph.git \
    && cd OpenSceneGraph \
    && mkdir build \
    && cd build \
    && cmake .. -DDESIRED_QT_VERSION=4 \
    && make -j4 \
    && sudo make install

# flexible collision graph
RUN git clone https://github.com/flexible-collision-library/fcl.git \
    && cd fcl \
    && git checkout 0.5.0  # use FCL 0.5.0  \
    && mkdir build \
    && cd build \
    && sudo ln -sf /usr/include/eigen3/Eigen /usr/include/Eigen \
    && cmake .. \
    && make -j4 \
    && sudo make install

# openrave
RUN git clone --branch latest_stable https://github.com/rdiankov/openrave.git \
    && cd openrave && mkdir build && cd build \
    && cmake .. -DOSG_DIR=/usr/local/lib64/ \
    && make -j4 \
    && sudo make install

RUN echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(openrave-config --python-dir)/openravepy/_openravepy_" >> /home/ros/.bashrc
RUN echo "export PYTHONPATH=$PYTHONPATH:$(openrave-config --python-dir)" >> /home/ros/.bashrc

# Install python packages using pip
COPY requirements.txt /tmp/
RUN python3 -m pip install --no-cache-dir -r /tmp/requirements.txt