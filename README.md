# drawbase

This repo contains a base drawing task template for web experiments. It is meant to be forked and modified for various specific experimental needs. It will also include templates for common auxiliary tasks, including sketch recognition and sketch annotation. 

# task repository

## draw

This is the primary task class for running experiments that collect drawings from human participants. In general, the structure of each trial consists of two parts: cue + response. 

The cue can be one or more of the following data types: string, image, video. The URL or path for accessing cue data will be fetched from a mongo database that is already running on a per-trial basis. 

The response will be a sketch. Both svg representations of each stroke and a final bitmap rendering of the finished sketch will be saved to a mongo database that is already running. 

## recog


## annotate
