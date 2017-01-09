############################################################
# Dockerfile to build Matplotlib 1.4.3 (Python library
# container images.
#
# build: docker build -t matplotlib-test .
# run with: docker run -v /Users/_PATH_TO_/matplotlib/share/:/share/ matplotlib-test
#
# Based on Ubuntu
############################################################
FROM ubuntu:14.04

RUN apt-get update
# Install pip, Python and matplotlib required libraries
RUN apt-get update && apt-get install -y python python-dev python-pip libxft-dev libfreetype6 libfreetype6-dev

# Install matplotlib
RUN pip install 'matplotlib==1.4.3'

# run matplotlib example and save file to shared dir
WORKDIR /src
CMD ["python", "/share/simpleapp.py"]
