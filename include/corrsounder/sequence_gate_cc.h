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


#ifndef INCLUDED_CORRSOUNDER_SEQUENCE_GATE_CC_H
#define INCLUDED_CORRSOUNDER_SEQUENCE_GATE_CC_H

#include <corrsounder/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace corrsounder {

    /*!
     * \brief <+description of block+>
     * \ingroup corrsounder
     *
     */
    class CORRSOUNDER_API sequence_gate_cc : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<sequence_gate_cc> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of corrsounder::sequence_gate_cc.
       *
       * To avoid accidental use of raw pointers, corrsounder::sequence_gate_cc's
       * constructor is in a private implementation
       * class. corrsounder::sequence_gate_cc::make is the public interface for
       * creating new instances.
       */
      static sptr make(int sequence_length, double sample_rate=1.0);
    };

  } // namespace corrsounder
} // namespace gr

#endif /* INCLUDED_CORRSOUNDER_SEQUENCE_GATE_CC_H */

