FROM ubuntu:xenial

MAINTAINER Davide Bortolami <d@fermiumlabs.com>

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV DEBIAN_FRONTEND noninteractive

# Basic Packages
RUN apt-get update -yyq --fix-missing && apt-get install -yyq wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    git mercurial subversion \
    software-properties-common apt-transport-https

# Add R-CRAN repository
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9
RUN add-apt-repository 'deb [arch=amd64,i386] https://cran.rstudio.com/bin/linux/ubuntu xenial/'
RUN apt-get update -yyq

# Install Tini
RUN apt-get install -yyq curl grep sed dpkg && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb 

# Install QT and X11
RUN apt-get install -yyq  qt5-default libgl1-mesa-glx
#ENV QT_GRAPHICSSYSTEM native

# Install R and python 3
RUN apt-get install -yyq python3-setuptools build-essential python3-pip
RUN apt-get install -yyq r-base r-base-dev
# R and python dependencies
RUN apt-get install -y libbz2-dev libreadline-dev 

# Programming ICs and stuff
RUN apt-get install -y avrdude flashrom dialog

# Install python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

# Cleanup
RUN rm tini.deb
RUN rm /tmp/requirements.txt
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "/bin/bash" ]
