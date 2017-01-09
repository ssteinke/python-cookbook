# Docker container with Matplotlib 1.4.3
Example: run a docker container with python and Matplotlib 1.4.3.

The container runs a simple python script to generate a plots on stores the plot as png file on shared storage.

Usage:
* cd to the matplotlib directory
* build container:
```
docker build -t matplotlib-test .
```
* run the container (and execute the simpleapp.py):
```
docker run -v /Users/_PATH_TO_/matplotlib/share/:/share/ matplotlib-test
```

Check the share directory for a new scatter.png file
