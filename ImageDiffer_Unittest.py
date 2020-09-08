import unittest
from ImageDiffer_Script import ImageDiffer

class ImageDifferTestCase(unittest.TestCase):
    # Test 1: checking validity of extension of image file.
    def test_hasValidImageExtension(self):
        diff = ImageDiffer("", "")
        self.assertTrue(diff.hasValidImageExtension('valid.png'))
        self.assertTrue(diff.hasValidImageExtension('valid.jpeg'))
        self.assertFalse(diff.hasValidImageExtension('valid.txt'))
    
    # Test 2: checking similarites between image. 
    # 'Test1.jpg', 'Test2.jpg', 'Test1.bmp' exist in the same directoy of the script.
    def test_sift_sim(self):
        diff = ImageDiffer("", "")
        self.assertEqual(diff.sift_sim("Test1.jpg", "Test1.jpg"), (True, 1.0))
        self.assertEqual(diff.sift_sim("Test1.jpg", "Test2.jpg"), (True, 0.7518796992481203))
        self.assertEqual(diff.sift_sim("Test1.jpg", "Test1.bmp"), (True, 1.0))
        self.assertEqual(diff.sift_sim("Test4.jpg", "Test1.bmp"), (False, 'Invalid image Test4.jpg'))

    # Test 3: checking conversion of similarity values as per user requirements. 
    def test_similar_value(self):
        diff = ImageDiffer("", "")
        self.assertEqual(diff.similar_value(0.0), 1.0)
        self.assertEqual(diff.similar_value(1.0), 0.0)
        self.assertEqual(diff.similar_value(0.75), 0.75)

    # Test 4: checking validity of header files of input file.
    def test_check_invalidfileheaders(self):
        diff = ImageDiffer("", "")
        self.assertFalse(diff.check_invalidfileheaders(['Image_1', 'Image_2']))
        self.assertTrue(diff.check_invalidfileheaders(['Image1', 'Image_2']))
        self.assertTrue(diff.check_invalidfileheaders(['Image_1', 'Image_2', 'Image_3']))

if __name__ == '__main__':
    unittest.main()
