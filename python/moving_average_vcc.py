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

import numpy
from gnuradio import gr
import numpy as np

class moving_average_vcc(gr.sync_block):
    """
    Elemen-wise moving average
    
    If window <= 0 then it integrates all prev vectors
    """
    def __init__(self, vlen, window=10):
        gr.sync_block.__init__(self,
            name="moving_average_vcc",
            in_sig=[(np.complex64, vlen)],
            out_sig=[(np.complex64, vlen)])
        
        self.vmem = np.zeros(vlen)
        self.count = 0.

    def work(self, input_items, output_items):
        self.vmem = self.vmem + np.array(input_items[0])
        print self.vmem
        self.count = self.count + 1.
        output_items[0][:] = self.vmem/self.count
        return 1

