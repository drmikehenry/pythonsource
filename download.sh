#!/bin/bash

versions=(
2.7.15
2.7.16
2.7.17
2.7.18
3.5.7
3.5.8
3.5.9
3.6.8
3.6.9
3.6.10
3.6.11
3.6.12
3.6.13
3.7.2
3.7.3
3.7.4
3.7.5
3.7.6
3.7.7
3.7.8
3.7.9
3.7.10
3.8.0
3.8.1
3.8.2
3.8.3
3.8.4
3.8.5
3.8.6
3.8.7
3.8.8
3.8.9
3.9.0
3.9.1
3.9.2
3.9.3
3.9.4
)

URL='https://www.python.org/ftp/python'
for i in "${versions[@]}"; do
    name="Python-$i.tar.xz"
    if [ -f "$name" ]; then
        echo "[cached] $name"
    else
        echo "[download] $name"
        wget "$URL/$i/Python-$i.tar.xz"
    fi
done
