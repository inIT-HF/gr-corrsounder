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
from fzc_source_c import fzc_source_c
from pycorrsounder import corrsounder

class qa_fzc_source_c (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_single_sequence (self):
        N = 1024
        q = 7
        expected_result = corrsounder.sequence_frank_zadoff_chu(sequence_length=N, q=q)

        dut = fzc_source_c(n_fzc=N, q=q, repeat=False)
        dst = blocks.vector_sink_c(vlen=1)

        self.tb.connect(dut, dst)
        self.tb.run()

        result_data = dst.data()
        self.assertFloatTuplesAlmostEqual(expected_result, result_data, 6)


if __name__ == '__main__':
    gr_unittest.run(qa_fzc_source_c, "qa_fzc_source_c.xml")
