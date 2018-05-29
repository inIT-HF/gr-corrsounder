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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include <pmt/pmt.h>
#include "sequence_gate_cc_impl.h"

namespace gr {
  namespace corrsounder {

    sequence_gate_cc::sptr
    sequence_gate_cc::make(int sequence_length, double sample_rate)
    {
      return gnuradio::get_initial_sptr
        (new sequence_gate_cc_impl(sequence_length, sample_rate));
    }

    /*
     * The private constructor
     */
    sequence_gate_cc_impl::sequence_gate_cc_impl(int sequence_length, double sample_rate)
      : gr::block("sequence_gate_cc",
              gr::io_signature::make(1, 1, sizeof(gr_complex)),
              gr::io_signature::make(1, 1, sizeof(gr_complex))),
        d_sequence_length(sequence_length),
        d_sample_rate(sample_rate)
    {}

    /*
     * Our virtual destructor.
     */
    sequence_gate_cc_impl::~sequence_gate_cc_impl()
    {
    }

    void
    sequence_gate_cc_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      /* <+forecast+> e.g. ninput_items_required[0] = noutput_items */
      ninput_items_required[0] = d_sequence_length + noutput_items;
    }

    int
    sequence_gate_cc_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const gr_complex *in = (const gr_complex *) input_items[0];
      gr_complex *out = (gr_complex *) output_items[0];

      pmt::pmt_t tag_key = pmt::intern("overflows");
      std::vector<tag_t> tags;
      get_tags_in_window(tags, 0, 0, noutput_items, tag_key);

      // Tell runtime system how many input items we consumed on
      // each input stream.
      if(tags.size() > 0)
      {
        uint64_t consume_input_items = tags[0].offset - this->nitems_read(0);
        consume_each (consume_input_items);
      }


      // Tell runtime system how many output items we produced.
      return 1;
    }

  } /* namespace corrsounder */
} /* namespace gr */

