#!/bin/sh

python synthetic_data_gen.py
python data_reader.py --use-synthetic
python plotting.py --use-synthetic
