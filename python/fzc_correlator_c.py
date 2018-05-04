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

from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
import numpy as np
import pycorrsounder as pycor

class fzc_correlator_c(gr.hier_block2):
    """
    FZC correlator with cyclic sequence x(n) for n=1...n_fzc:
     x(n) = -1^(q * n) * exp(j * pi * q * n^2 / n_fzc)
    """
    def __init__(self, n_fzc=255, q=7):
        gr.hier_block2.__init__(self,
            "FZC Correlator",
            gr.io_signature(1, 1, gr.sizeof_gr_complex * 1),
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
        self.fir = filter.fft_filter_ccc(1, (np.conj(self.fzc_sequence[::-1])), 1)
        self.fir.declare_sample_delay(0)
        self.norm = blocks.multiply_const_vcc((1. / n_fzc,))

        ##################################################
        # Connections
        ##################################################
        self.connect((self.norm, 0), (self, 0))
        self.connect((self.fir, 0), (self.norm, 0))
        self.connect((self, 0), (self.fir, 0))

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
        self.fir.set_taps((np.conj(self.fzc_sequence[::-1])))