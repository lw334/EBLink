import sys
sys.path.append("../")
import pandas as pd
import numpy as np
import ebLink

def test_create():
    df = pd.read_csv("data/RLData500.csv")
    categoricals = df["bd"]
    strings = df[['fname_c1', 'lname_c1','by','bm']]
    df["filenum"] = 1
    df["filenum"][:200] = 1
    df["filenum"][200:350] = 2
    df["filenum"][350:500] = 3
    # Xc = np.matrix(categoricals)
    # Xs = np.matrix(strings)
    # filenum = np.matrix(df["filenum"])
    Xc = categoricals
    Xs = strings
    filenum = df["filenum"]
    M = len(df)
    a = 1
    b = 999
    c = 1
    numgs = 10
    link = ebLink.EBLink(filenum, Xs, Xc, numgs, a, b, c, "jaro-winkler", M)
    return link

def test_build(link):
    lamgs, estPopSize = link.build()
    return lamgs, estPopSize