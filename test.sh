#! /bin/sh

if [ -z "$*" ]; then
	(set -x; python3 -m unittest discover --verbose -s src)
else
	(set -x; python3 -m unittest discover --verbose -s src "$@")
fi
