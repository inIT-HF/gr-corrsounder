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

from gnuradio import gr, filter

class error_correction_cc(gr.hier_block2):
    """
    docstring for block error_correction_cc
    """
    def __init__(self, error_term_forward_transmission_tracking):
        gr.hier_block2.__init__(self,
            "error_correction_cc",
            gr.io_signature(1, 1, gr.sizeof_gr_complex * 1),  # Input signature
            gr.io_signature(1, 1, gr.sizeof_gr_complex * 1)) # Output signature

        ##################################################
        # Blocks
        ##################################################
        self.fir = filter.fft_filter_ccc(1, error_term_forward_transmission_tracking, 1)

        ##################################################
        # Connections
        ##################################################
        self.connect(self, self.fir, self)
