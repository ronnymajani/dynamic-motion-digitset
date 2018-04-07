#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Used this file to rename files from the old timestamp format "%H.%M_%d.%m.%Y_digitset.json"
# to the new timestamp format in v2.11 "%Y.%m.%d_%H.%M_digitset.json"

import os

folder = "other"

dirs = os.listdir(folder)

temp = {}

for file in dirs:
    f = file.split(sep="_")
    time = f[0].split(sep=".")
    date = f[1].split(sep=".")
    date.reverse()
    time = ".".join(time)
    date = ".".join(date)
    newfile = date + "_" + time + "_" + f[2]
    oldfile = os.path.join(folder, file)
    newfile = os.path.join(folder, newfile)
    os.rename(oldfile, newfile)





