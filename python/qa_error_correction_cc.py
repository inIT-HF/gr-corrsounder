#!/usr/bin/env python
# -*- coding: utf-8 -*-
# gr-corrsounder
# Copyright (C) 2017  hf-ag
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# gr-corrsounder  Copyright (C) 2017  hf-ag
# This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
# This is free software, and you are welcome to redistribute it
# under certain conditions; type `show c' for details.

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from error_correction_cc import error_correction_cc
import numpy as np

class qa_error_correction_cc (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_one_tap_error_correction (self):
        src_data = [1. + 0.j, ] * 128
        expected_result = np.multiply(src_data, 0.5)

        src = blocks.vector_source_c(data=src_data, vlen=1, repeat=False)
        dut = error_correction_cc(error_term_forward_transmission_tracking=[0.5, ])
        dst = blocks.vector_sink_c(vlen=1)

        self.tb.connect(src, dut, dst)
        self.tb.run()

        result_data = dst.data()
        self.assertFloatTuplesAlmostEqual(expected_result, result_data, 6)


if __name__ == '__main__':
    gr_unittest.run(qa_error_correction_cc, "qa_error_correction_cc.xml")
