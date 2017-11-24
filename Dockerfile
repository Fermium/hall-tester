FROM ubuntu:xenial

MAINTAINER Davide Bortolami <d@fermiumlabs.com>

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV DEBIAN_FRONTEND noninteractive

# Basic Packages
RUN apt-get update -yyq --fix-missing && apt-get install -yyq wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    git mercurial subversion

# Install Anaconda 3
RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/archive/Anaconda3-5.0.1-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh
RUN /opt/conda/bin/conda update --all
ENV PATH /opt/conda/bin:$PATH

# Install Tini
RUN apt-get install -yyq curl grep sed dpkg && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb 

# Install QT and X11
RUN apt-get install -yyq  qt5-default libgl1-mesa-glx
ENV QT_GRAPHICSSYSTEM native

# R and python dependencies
RUN apt-get install -y libbz2-dev libreadline-dev 
RUN conda install -y r-essentials

# Programming ICs and stuff
RUN apt-get install -y avrdude flashrom dialog
RUN apt-get install -y build-essential

# Install python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Cleanup
RUN rm tini.deb
RUN rm /tmp/requirements.txt
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "/bin/bash" ]
