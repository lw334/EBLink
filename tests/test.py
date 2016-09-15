import sys
sys.path.append("../")
import pandas as pd
import ebLink
import unittest
pd.options.mode.chained_assignment = None

def preprocess():
    df = pd.read_csv("data/RLData500.csv")
    categoricals = df["bd"]
    strings = df[['fname_c1', 'lname_c1', 'by', 'bm']]
    df["filenum"] = 1
    df["filenum"][:200] = 1
    df["filenum"][200:500] = 2
    df["filenum"][500:511] = 3
    Xc = categoricals
    Xs = strings
    filenum = df["filenum"]
    M = len(df)
    a = 1
    b = 999
    c = 1
    numgs = 5
    return filenum, Xs, Xc, numgs, a, b, c, M

class TestEBLink(unittest.TestCase):

    def test_invalid_string_metric(self):
        filenum, Xs, Xc, numgs, a, b, c, M = preprocess()
        d = "foo"
        self.assertRaises(ValueError, ebLink.EBLink, filenum, Xs, Xc, numgs, a, b, c, d, M)

    def test_MMS(self):
        available_string_dist = ["osa", "lv", "dl", "hamming", "lcs", "qgram", "cosine", "jaccard", "jw", "soundex"]
        filenum, Xs, Xc, numgs, a, b, c, M = preprocess()
        for d in available_string_dist:
            self.link = ebLink.EBLink(filenum, Xs, Xc, numgs, a, b, c, d, M)
            lamgs, estPopSize = self.link.get_link_structure()
            self.assertEqual(len(estPopSize), numgs, 'incorrect number of iterations')
            MMS = self.link.get_MMS(lamgs, estPopSize)
            self.assertGreater(len(MMS), 0, "No match is found.")

if __name__ == "__main__":
    unittest.main()