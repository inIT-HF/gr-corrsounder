/* -*- c++ -*- */
/* gr-corrsounder
 * Copyright (C) 2017  hf-ag
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * 
 * gr-corrsounder  Copyright (C) 2017  hf-ag
 * This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
 * This is free software, and you are welcome to redistribute it
 * under certain conditions; type `show c' for details.
 */

#ifndef INCLUDED_CORRSOUNDER_SEQUENCE_GATE_CC_IMPL_H
#define INCLUDED_CORRSOUNDER_SEQUENCE_GATE_CC_IMPL_H

#include <corrsounder/sequence_gate_cc.h>

namespace gr {
  namespace corrsounder {

    class sequence_gate_cc_impl : public sequence_gate_cc
    {
     private:
      int d_sequence_length;
      double d_sample_rate;
      std::list<gr_complex> d_mem;
      pmt::pmt_t d_trigger_tag_key;

     public:
      sequence_gate_cc_impl(int sequence_length, double sample_rate);
      ~sequence_gate_cc_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);
    };

  } // namespace corrsounder
} // namespace gr

#endif /* INCLUDED_CORRSOUNDER_SEQUENCE_GATE_CC_IMPL_H */

