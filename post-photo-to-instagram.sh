#!/usr/bin/env bash

python3 generate_in_file.py
python3 post-photo-to-instagram.py < in.txt
