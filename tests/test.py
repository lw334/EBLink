import sys
sys.path.append("../")
import pandas as pd
import ebLink
import unittest
pd.options.mode.chained_assignment = None

file_paths = ["data/RLData500_1.csv", "data/RLData500_2.csv", "data/RLData500_3.csv"]
string_cols = ["fname_c1", "lname_c1", "by", "bm"]
cate_cols = ["bd"]
numgs = 10
a = 1
b = 999
c = 1
M = 500

class TestEBLink(unittest.TestCase):

    def test_filenum(self):
        d = "lv"
        self.link = ebLink.EBLink(file_paths, string_cols, cate_cols, numgs, a, b, c, d, M)
        self.assertEqual(len(self.link.df), 515)
        self.assertEqual(sum(self.link.df[:250]['filenum'] == 0), 250)
        self.assertEqual(sum(self.link.df[250:400]['filenum'] == 1), 150)
        self.assertEqual(sum(self.link.df[400:515]['filenum'] == 2), 115)


    def test_invalid_string_metric(self):
        d = "foo"
        self.assertRaises(ValueError, ebLink.EBLink, file_paths, string_cols, cate_cols, numgs, a, b, c, d, M)

    def test_MMS(self):
        available_string_dist = ["osa", "lv", "dl", "hamming", "lcs", "qgram", "cosine", "jaccard", "jw", "soundex"]
        for d in available_string_dist:
            self.link = ebLink.EBLink(file_paths, string_cols, cate_cols, numgs, a, b, c, d, M)
            lamgs, estPopSize = self.link.get_link_structure()
            self.assertEqual(len(estPopSize), numgs, 'incorrect number of iterations')
            MMS = self.link.get_MMS(lamgs, estPopSize)
            self.assertGreater(len(MMS), 0, "No match is found.")

if __name__ == "__main__":
    unittest.main()