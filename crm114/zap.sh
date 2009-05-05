#!/bin/bash

rm -rf reaver_cache
rm spam.css nonspam.css
cssutil -b -r spam.css
cssutil -b -r nonspam.css
./trainer.py
