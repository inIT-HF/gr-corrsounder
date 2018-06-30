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
#include <vector>
#include "sequence_gate_cc_impl.h"

#define OUTPUT_SAMPLES {\
    uint64_t output_samples = (d_mem.size() / d_sequence_length) * d_sequence_length; \
    if(output_samples > 0) \
    { \
        produce_output_items += output_samples;  \
        for(uint64_t i = 0; i < output_samples; i++) \
        { \
          *out++ = d_mem.front(); \
          d_mem.pop_front(); \
        } \
    } \
}

#define REL_OFFSET(tag) tag.offset - this->nitems_read(0)

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
        d_sample_rate(sample_rate),
        d_mem(),
        d_trigger_tag_key(pmt::intern("overflows"))
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
      ninput_items_required[0] = noutput_items;
    }

    int
    sequence_gate_cc_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const gr_complex *in = (const gr_complex *) input_items[0];
      gr_complex *out = (gr_complex *) output_items[0];

      uint64_t max_consume_input_items = ninput_items[0];

      if(max_consume_input_items > noutput_items)
      {
        max_consume_input_items = noutput_items;
      }

      std::vector<tag_t> overflow_tags;
      get_tags_in_window(overflow_tags, 0, 0, max_consume_input_items, d_trigger_tag_key);

      uint64_t consume_input_items = 0;
      uint64_t produce_output_items = 0;

      OUTPUT_SAMPLES;

      if(overflow_tags.size() > 0)
      {
        GR_LOG_INFO(d_logger, "Overflow tag detected");

        //skip/copy samples until overflow
        for(uint64_t i = 0; i < REL_OFFSET(overflow_tags[0]); i++)
        {
          d_mem.push_back(in[i]);
        }

        OUTPUT_SAMPLES;

        d_mem.clear();

        uint64_t dropped_samples = pmt::to_long(overflow_tags[0].value);
        uint64_t skip_samples =  (d_sequence_length - (dropped_samples % d_sequence_length) ) % d_sequence_length;

        uint64_t until = max_consume_input_items;
        if(overflow_tags.size() > 1)
        {
          until = REL_OFFSET(overflow_tags[1]);
        }

        for(uint64_t i = REL_OFFSET(overflow_tags[0]) + skip_samples; i < until; i++)
        {
          d_mem.push_back(in[i]);
        }
        consume_input_items = until;
      }
      else
      {
        for(uint64_t i = 0; i < max_consume_input_items; i++)
        {
          d_mem.push_back(in[i]);
        }
        consume_input_items = max_consume_input_items;
      }

      OUTPUT_SAMPLES;

      consume_each (consume_input_items);

      // Tell runtime system how many output items we produced.
      return produce_output_items;
    }

  } /* namespace corrsounder */
} /* namespace gr */

