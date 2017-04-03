#! /bin/sh

#generate deb packabe for version 2.8 of construct
fpm -f -s python -t deb -v 2.8.8 construct

fpm -f \
	-s python \
	-t deb \
	--deb-changelog CHANGELOG \
	-d gstreamer1.0-plugins-base \
	-d gstreamer1.0-plugins-good \
	-d libgstreamer1.0-0 \
	-d python2.7 \
	-d python-gi \
	-d python-gst-1.0 \
	-d python-pkg-resources \
	setup.py
