#!/bin/bash

source activate solaris

traindatapath=$/home/siddeshwarraghavan/data/train
traindataargs="\
--sardir $/home/siddeshwarraghavan/data/train/SAR-Intensity \
--opticaldir $/home/siddeshwarraghavan/data/train/PS-RGB \
--labeldir $/home/siddeshwarraghavan/data/train/geojson_buildings \
--rotationfile $/home/siddeshwarraghavan/data/train/SummaryData/SAR_orientations.txt \
"

source settings.sh

./baseline.py --pretrain --train $traindataargs $settings
