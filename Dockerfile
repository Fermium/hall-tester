FROM phusion/baseimage

MAINTAINER Davide Bortolami <d@fermiumlabs.com>

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    git mercurial subversion

RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/archive/Anaconda3-5.0.1-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh


ENV PATH /opt/conda/bin:$PATH

RUN conda update --all

#R and python dependencies
RUN apt-get install -y libbz2-dev libreadline-dev 
RUN conda install -y r-essentials

#Programming ICs and stuff
RUN apt-get install -y avrdude flashrom dialog
RUN apt-get install -y build-essential

ADD requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

CMD ["/sbin/my_init"]
