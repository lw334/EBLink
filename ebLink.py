import os
import numpy as np
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
import sys
sys.setrecursionlimit(5000)

class EBLink(object):

    ## TODO: add in a parameter for specifiying distance function for string values
    def __init__(self, filenum, Xs, Xc, numgs, a, b, c, d, M):
        '''
        :param filenum: An array of numbers indicating which file the entries are from
        :param Xs: An array of string variables
        :param Xc: An array of categorical variables
        :param numgs: An integer indicating total number of gibb iterations
        :param a: An integer indicating the shape parameter of Beta prior
        :param b: An integer indicating the scale paramter of Beta prior
        :param c: An integer that is a positive constant
        :param d: Any distance metric measure the latent and observed string
                - "adist": Standard Levenshtein distance
        :param M: The true value of the population size

        :Return: Returns the estimated linkage structure via Gibbs sampling
        '''

        self.filenum = filenum
        self.Xs = Xs
        self.Xc = Xc
        self.numgs = numgs
        self.a = a
        self.b = b  # a string specifying the type of distance measurement
        self.c = c
        self.d = d
        self.M = M

    ## TODO: Return a link structure and estimated population size
    def build(self):
        pandas2ri.activate()
        matrix = ro.r['as.matrix']
        xc = matrix(self.Xs)
        xs = matrix(self.Xc)
        numgs = ro.IntVector([self.numgs])
        m = ro.IntVector([self.M])
        filenum = ro.IntVector(np.array(self.filenum))
        a = ro.IntVector([self.a])
        b = ro.IntVector([self.b])
        c = ro.IntVector([self.c])

        #TODO: Enable other types of string match
        if self.d == "adist":
            ro.r("d <- function(string1,string2){adist(string1,string2)}")
            d = ro.r['d']

        # Loads in Gibbs sampler and plyr packages
        ro.r("source('../ebLink/R/code/ebGibbsSampler.R', chdir = TRUE)")
        importr("plyr")

        # Runs the gibbs sampler
        gibbs = ro.r["rl.gibbs"]
        #lam = gibbs(file_num=self.filenum, X_s=self.Xs, X_c=self.Xc, num_gs=self.numgs, a=self.a, b=self.b, c=self.c, d=d, M=self.M)
        lam = gibbs(file_num=filenum, X_s = xs, X_c=xc, num_gs=numgs, a=a,b=b,c=c,d=d,M=m)
        # Calculate estimated population sizes by finding number of uniques
        apply = ro.r["apply"]
        ro.r("len_uniq <- function(x){length(unique(x))}")
        len_uniq = ro.r['len_uniq']
        estPopSize = apply(lam, 1, len_uniq)
        return np.array(lam), np.array(estPopSize)

    ## TODO: Return Maximum Matching Set