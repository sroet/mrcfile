# Copyright (c) 2016, Science and Technology Facilities Council
# This software is distributed under a BSD licence. See LICENSE.txt.

"""
Tests for gzipmrcfile.py
"""

# Import Python 3 features for future-proofing
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import unittest

from .test_mrcfile import MrcFileTest
from mrcfile.gzipmrcfile import GzipMrcFile


class GzipMrcFileTest(MrcFileTest):
    
    """Unit tests for gzipped MRC file I/O.
    
    Note that this test class inherits MrcFileTest to ensure all of the tests
    for MrcObject and MrcFile work correctly for the GzipMrcFile subclass.
    
    """
    
    def setUp(self):
        # Set up as if for MrcFileTest
        super(GzipMrcFileTest, self).setUp()
        
        # Replace test MRC files with their gzipped equivalents
        self.example_mrc_name = os.path.join(self.test_data, 'emd_3197.map.gz')
        self.ext_header_mrc_name = os.path.join(self.test_data, 'emd_3001.map.gz')
        self.fei1_ext_header_mrc_name = os.path.join(self.test_data, 'fei-extended.mrc.gz')
        self.fei2_ext_header_mrc_name = os.path.join(self.test_data, 'epu2.9_example.mrc.gz')
        
        # Set the newmrc method to the GzipMrcFile constructor
        self.newmrc = GzipMrcFile
        
        # Set up parameters so MrcObject tests run on the GzipMrcFile class
        obj_mrc_name = os.path.join(self.test_output, 'test_mrcobject.mrc')
        self.mrcobject = GzipMrcFile(obj_mrc_name, 'w+', overwrite=True)
        # Flush and re-read to ensure underlying file is valid gzip
        self.mrcobject.flush()
        self.mrcobject._read()
    
    def test_non_mrc_file_is_rejected(self):
        """Override test to change expected error message."""
        name = os.path.join(self.test_data, 'emd_3197.png')
        with (self.assertRaisesRegex(IOError, 'Not a gzipped file')):
            GzipMrcFile(name)
    
    def test_non_mrc_file_gives_correct_warnings_in_permissive_mode(self):
        """Override test - permissive mode still can't read non-gzip files."""
        name = os.path.join(self.test_data, 'emd_3197.png')
        with (self.assertRaisesRegex(IOError, 'Not a gzipped file')):
            GzipMrcFile(name, permissive=True)
    
    def test_repr(self):
        """Override test to change expected repr string."""
        with GzipMrcFile(self.example_mrc_name) as mrc:
            assert repr(mrc) == "GzipMrcFile('{0}', mode='r')".format(self.example_mrc_name)


if __name__ == "__main__":
    unittest.main()
