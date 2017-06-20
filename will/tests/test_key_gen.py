import unittest
from will import utils


class Testkey_gen(unittest.TestCase):
    def setUp(self):
        self.keylength=10
        self.fail_count=1

    def test_key_gen(self):
        tmp = utils.key_gen('Test Key Generation',
                            self.keylength, None)
        self.assertTrue(tmp)
        self.assertTrue((len(tmp)<=self.keylength))

    def test_key_gen_cb_test(self):

        tmp = utils.key_gen('This Is A CallBack Test',
                            self.keylength,
                            self._key_check_cb)

        self.assertTrue(tmp)

        self.assertTrue((len(tmp)<=self.keylength))

    def _key_check_cb(self, key=None):
        """ call back to simulate the check for an existing
        key
        """
        if self.fail_count <= 0:
            return False
        else:
            self.fail_count += -1
            return True

