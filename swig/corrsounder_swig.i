/* -*- c++ -*- */

#define CORRSOUNDER_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "corrsounder_swig_doc.i"

%{
#include "corrsounder/sequence_gate_cc.h"
%}

%include "corrsounder/sequence_gate_cc.h"
GR_SWIG_BLOCK_MAGIC2(corrsounder, sequence_gate_cc);
