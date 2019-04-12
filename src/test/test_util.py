#!/opt/anaconda/bin/python

import sys
import os
import unittest
import string
import numpy as np
from StringIO import StringIO
import py_compile
from osgeo import gdal, ogr
# Simulating the Runtime environment

sys.path.append('/workspace/wfp-01-03-04/src/main/app-resources/notebook/libexec')

from aux_functions import matrix_sum, write_output_image, calc_average, get_matrix_list
os.environ['TMPDIR'] = '/tmp'
os.environ['_CIOP_APPLICATION_PATH'] = '/application'
os.environ['ciop_job_nodeid'] = 'dummy'
os.environ['ciop_wf_run_root'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'artifacts')

#sys.path.append('../main/app-resources/util/')

#from util import log_input


class NodeATestCase(unittest.TestCase):

    def setUp(self):
        self.mat1 = np.matrix('1, 1; 1, 1')
        self.mat2 = np.matrix('2, 2; 2, 2')
        self.mat3 = np.matrix('-9999, -9999; -9999, -9999')
        self.mat4 = np.matrix('-9999, 2; 3, -9999')
        self.mat5 = 0
        self.mat6 = np.matrix('1, 2; 3, 4')
        self.mat7 = np.matrix('2, 3; 1, 3')
        self.test_img = "/workspace/data/test_image_chirps.tif"
        
    def test_matrix_sum(self):
        sum1 = matrix_sum(self.mat1, self.mat2)
        self.assertTrue((sum1 == np.matrix('3, 3; 3, 3')).all())
    
    def test_matrix_sum_with_no_data_value(self):
        sum1 = matrix_sum(self.mat1, self.mat4, -9999)
        self.assertTrue((sum1 == np.matrix('1, 3; 4, 1')).all())
    
    def test_matrix_sum_with_different_sizes(self):
        sum1 = matrix_sum(self.mat1, self.mat5, -9999)
        self.assertTrue((sum1 == self.mat1).all())
        
    '''def test_write_image(self):
        matrix_rand = np.random.rand(30,30)
        mask_rand = np.random.randint(2, size=(30,30))
        filepath = "/workspace/wfp-01-03-04/src/test/output_test.tif"
        write_output_image(filepath, matrix_rand, "GTiff", mask=mask_rand)
        self.assertGreaterEqual(os.path.getsize(filepath), 0)
        os.remove('output_test.tif')'''
    
    def test_calc_average(self):
        mat_list = [self.mat1, self.mat2, self.mat6, self.mat7]
        average_matrix = calc_average(mat_list, 4)
        print(average_matrix)
        self.assertTrue((average_matrix == np.matrix('1.5, 2; 1.75, 2.5')).all())
        
    def test_get_matrix_list(self):
        img_list = []
        for i in range(4):
            img_list.append(self.test_img)
        matrix_list = get_matrix_list(img_list)
        self.assertEqual(len(matrix_list), len(img_list))
        for mat in matrix_list:
            self.assertTrue(mat.any())
    
    def test_compile(self):
        try:
          py_compile.compile('../main/app-resources/notebook/run', doraise=True)
        except:
          self.fail('failed to compile src/main/app-resources/notebook/run')
 
if __name__ == '__main__':
    unittest.main()


