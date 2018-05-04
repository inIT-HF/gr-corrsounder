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
import corrsounder
import numpy as np
import pmt

class qa_sequence_gate_cc (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block()

        # origin data is equal to timestamps
        samp_rate = 1.

        # data [lost items 0, 1, ..., 9], 10, 11, ..., 19
        data_with_overflows = np.arange(10,20)

        # Overflow tag
        overflow = gr.tag_utils.python_to_tag(
            (0, pmt.intern("overflows"), pmt.from_long(10), pmt.intern("src0")))

        self.src = blocks.vector_source_c(data=data_with_overflows, repeat=False, vlen=1, tags=[overflow,])
        self.dut = corrsounder.sequence_gate_cc(3, samp_rate)
        self.dst = blocks.vector_sink_c(vlen=1)

        self.tb.connect(self.src, self.dut, self.dst)

    def tearDown (self):
        self.tb = None

    def test_001_timestamp (self):
        ''' Check correct timestamp tags '''

        self.tb.run()

        output_data = self.dst.data()
        output_tags = self.dst.tags()

        # Extract timestamp tags
        timestamp_tags = []
        for tag in output_tags:
            if pmt.to_python(tag.key) == "timestamp":
                timestamp_tags.append(tag)

        # Timestamp tags at index 12, 15
        self.assertEqual(len(timestamp_tags), 2)
        self.assertAlmostEqual(pmt.to_double(timestamp_tags[0].value), 12.0)
        self.assertAlmostEqual(pmt.to_double(timestamp_tags[1].value), 15.0)

    def test_002_full_sequences_output(self):
        ''' Check full sequences output '''

        self.tb.run()

        output_data = self.dst.data()

        # Full sequences: 12..14, 15..17
        expected_data = np.arange(12,18)
        self.assertFloatTuplesAlmostEqual(output_data, expected_data, 4)

    def test_003_uhd_source(self):
        self.assertTrue(False)

    def test_004_external_trigger(self):
        self.assertTrue(False)


if __name__ == '__main__':
    gr_unittest.run(qa_sequence_gate_cc, "qa_sequence_gate_cc.xml")
