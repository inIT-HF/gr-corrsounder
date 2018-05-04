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

import numpy as np
from gnuradio import gr

class ir_snr(gr.sync_block):
    """
    docstring for block ir_snr
    """
    def __init__(self, seq_len=255, max_ir_len=10):
        gr.sync_block.__init__(self,
            name="ir_snr",
            in_sig=[(np.complex64, seq_len)],
            out_sig=[np.float32])

        self.seq_len = seq_len
        self.max_ir_len = max_ir_len

    def lin2log(self, vector):
        return 20 * np.log10(np.abs(vector))

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]

        # Detect IR peak
        ir = np.array(in0[0])
        iPeak = np.argmax(ir)
        signal = self.lin2log(ir[iPeak])

        # Compute noise
        iNoise = [i for i in range(self.seq_len) if i <= iPeak - self.max_ir_len or i >= iPeak + self.max_ir_len]
        noise = self.lin2log(np.average(np.abs(ir[iNoise])))

        snr = signal - noise

        out[:] = snr
        return len(output_items[0])

