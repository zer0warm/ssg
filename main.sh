#! /bin/sh

python3 src/main.py
python3 -m http.server -d public 8888
