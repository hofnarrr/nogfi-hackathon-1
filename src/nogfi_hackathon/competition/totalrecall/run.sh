#!/usr/bin/env bash

python3 scalpel.py 0 & 
python3 scalpel.py 1 & 
python3 scalpel.py 2 &

while true; do
    sleep 10
done

