import unittest
from will import utils


class Testkey_gen(unittest.TestCase):
    def setUp(self):
        self.keylist=['ABCWE','TKG1','BMCQWR', 'TIAUT']
        self.keylength=10

    def test_key_gen(self):
        tmp = utils.key_gen('Test Key Generation',
                            self.keylength, self.keylist)
        self.assertTrue(tmp)
        self.assertTrue((len(tmp)<=self.keylength))
        self.assertTrue((tmp not in self.keylist))

    def test_key_gen_unique(self):

        tmp = utils.key_gen('This Is A Unique Test',
                            self.keylength, self.keylist)
        self.assertTrue(tmp)
        self.assertTrue((len(tmp)<=self.keylength))
        self.assertTrue((tmp not in self.keylist))

