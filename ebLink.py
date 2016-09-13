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
        '''
        :return:
         lamgs: R matrix of identified matches in each Gibbs sampling iteration
         estPopSize: R matrix of estimated population size in each Gibbs sampling iteration
        '''

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

        # Load in Gibbs sampler and plyr packages
        ro.r("source('../ebLink/R/code/ebGibbsSampler.R', chdir = TRUE)")
        importr("plyr")

        # Run the gibbs sampler
        gibbs = ro.r["rl.gibbs"]
        lamgs = gibbs(file_num=filenum, X_s=xs, X_c=xc, num_gs=numgs, a=a, b=b, c=c, d=d, M=m)

        # Calculate estimated population sizes by finding number of uniques
        apply = ro.r["apply"]
        ro.r("len_uniq <- function(x){length(unique(x))}")
        len_uniq = ro.r['len_uniq']
        estPopSize = apply(lamgs, 1, len_uniq)

        print("Estimated population size: ", estPopSize)

        return lamgs, estPopSize


    def get_MMS(self, lamgs, estPopSize):

        '''
        :param lamgs:
        :param estPopSize:
        :return: a list of tuples of indexes of matched records
        '''

        pair_output = []

        # Only look for linked pairs if there are pairs to look for
        if estPopSize < self.M:

            pandas2ri.activate()

            ro.r("source('../ebLink/R/code/analyzeGibbs.R', chdir = TRUE)")
            links = ro.r["links"]
            pairwise = ro.r["pairwise"]

            est_links = links(lamgs)
            est_pairs = pairwise(est_links)
            est_pairs = np.array(est_pairs)

            pair_output = [tuple(x) for x in est_pairs]

        return pair_output


    def build_crosswalk(self):
        pass

    def build_linked_data(self):
        pass