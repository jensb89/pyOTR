import unittest
from Src.cutlists import CutlistDownloader
import os


class TestCutlist(unittest.TestCase):

    def setUp(self):
        self.filename = 'Marvel_s_Agents_of_S_H_I_E_L_D___Wake_Up_17.01.24_22-00_uswabc_60_TVOON_DE.mpg.HQ.avi'

    def test_search_name(self):
        print "Cutlist Search test with file" + self.filename
        c=CutlistDownloader(self.filename)
        c.search(mode='name')
        self.assertTrue(len(c.data_cl_search)>=3)
    
    def test_download(self):
        c=CutlistDownloader(self.filename)        
        c.search(mode='name')
        c.sort_cutlists()
        c.download(toprated=True)
        self.assertTrue( os.path.isfile("Marvel_s_Agents_of_S_H_I_E_L_D___Wake_Up_17.01.24_22-00_uswabc_60_TVOON_DE.mpg.HQ.avi.cutlist") )
        if (os.path.isfile("Marvel_s_Agents_of_S_H_I_E_L_D___Wake_Up_17.01.24_22-00_uswabc_60_TVOON_DE.mpg.HQ.avi.cutlist")):
            os.remove("Marvel_s_Agents_of_S_H_I_E_L_D___Wake_Up_17.01.24_22-00_uswabc_60_TVOON_DE.mpg.HQ.avi.cutlist")



if __name__ == '__main__':
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCutlist)
    unittest.TextTestRunner(verbosity=2).run(suite)