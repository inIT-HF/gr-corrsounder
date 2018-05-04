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

from gnuradio import gr
from gnuradio import blocks
import numpy as np
import pycorrsounder as pycor

class fzc_source_c(gr.hier_block2):
    """
    FZC sequence generator x(n) with n=1...n_fzc:
     x(n) = -1^(q * n) * exp(j * pi * q * n^2 / n_fzc)
    """
    def __init__(self, n_fzc=255, q=7, repeat=True):
        gr.hier_block2.__init__(
            self, "FZC Sequence Source",
            gr.io_signature(0, 0, 0),
            gr.io_signature(1, 1, gr.sizeof_gr_complex * 1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.q = q
        self.n_fzc = n_fzc

        ##################################################
        # Variables
        ##################################################
        self.fzc_sequence = pycor.corrsounder.sequence_frank_zadoff_chu(sequence_length=n_fzc, q=q)

        ##################################################
        # Blocks
        ##################################################
        self.src = blocks.vector_source_c(data=self.fzc_sequence, repeat=repeat, vlen=1, tags=[])

        ##################################################
        # Connections
        ##################################################
        self.connect((self.src, 0), (self, 0))

    def get_q(self):
        return self.q

    def set_q(self, q):
        self.q = q
        self.set_fzc_sequence(pycor.corrsounder.sequence_frank_zadoff_chu(sequence_length=self.n_fzc, q=q))

    def get_n_fzc(self):
        return self.n_fzc

    def set_n_fzc(self, n_fzc):
        self.n_fzc = n_fzc
        self.set_fzc_sequence(pycor.corrsounder.sequence_frank_zadoff_chu(sequence_length=n_fzc, q=self.q))

    def get_fzc_sequence(self):
        return self.fzc_sequence

    def set_fzc_sequence(self, fzc_sequence):
        self.fzc_sequence = fzc_sequence
        self.src.set_data(self.fzc_sequence, [])
