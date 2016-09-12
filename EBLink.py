import os
import subprocess

import pandas as pd
import numpy as np
import rpy2
import rpy2.robjects as robjects

import csv

class EBLink(object):

    # ' @param file.num The number of the file
    # ' @param X.s A vector of string variables
    # ' @param X.c A vector of categorical variables
    # ' @param num.gs Total number of gibb iterations
    # ' @param a Shape parameter of Beta prior
    # ' @param b Scale parameter of Beta prior
    # ' @param c Positive constant
    # ' @param d Any distance metric measuring the latent and observed string
    # ' @param M The true value of the population size
    # ' @return Returns the estimated linkage structure via Gibbs sampling

    def __init__(self, files, iterations, alpha, beta, constant, distance):
        self.files = files
        self.iterations = iterations
        self.alpha = alpha
        self.beta = beta
        self.constant = constant
        self.distance = distance

        ## Constructed inputs
        self.file_num = len(files)
        self.Xs =
        self.Xc =
        self.M =

