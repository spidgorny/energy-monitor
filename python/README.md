# Python image recognition

## Idea

We want to be able to take an image from a camera that is pointing to a energy meter
(or any other changing number) and detect the number displayed. This number can be stored
in the database or sent somewhere else.

## How it works

The code in this repo is an experiment of the inexperienced ML developer. The code contains
code for different attempts of detecting numbers using K-Nearest Neighbours, Support Vector Machine,
Gaussian Naive Bayes, Supervised Neural Network. The last one seems to work best.

Make sure to read the original [blog post](https://www.mkompf.com/cplus/emeocv.html) which explains
the process in the details (with images).

## Config

The code was made to work for a specific digits of a specific electricity meter filmed from
a specific angle by a specific web-cam. Making it work for your situation is not plug-and-play.
It will take time and some minimal ML understanding and tweaking the parameters.

## Steps

1. The images from the cam should be put in ../cache folder
1. The image from the cam should be processed to isolate the digits from the background.
See Pipeline class.
1. Training should be run to train the model for your specific situation. 
The training results are stored by pickle to a file so it can be reused later.
See Train class.
1. After the training, new images can be recognized and used. See index.py

