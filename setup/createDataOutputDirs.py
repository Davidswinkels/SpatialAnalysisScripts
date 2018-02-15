#! /usr/bin/python
## Import libraries
import os
import shutil

## Check if repositories exist and otherwise make data and output repository
for data_dir in ['./data', './output']:
    if os.path.isdir(data_dir):
        shutil.rmtree(data_dir, ignore_errors=True)
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)
	
