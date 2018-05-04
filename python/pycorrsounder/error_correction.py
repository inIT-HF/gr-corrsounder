import numpy as np

'''
Ref: Agilent Application Note AN 1287-3 "Applying Error Correction to Network Analyzer Measurements", 2002

Systematic Error Terms:

* error_term_forward_directivity
* error_term_forward_source_match
* error_term_forward_reflection_tracking
* error_term_forward_load_match
* error_term_forward_transmission_tracking
* error_term_forward_isolation

* error_term_reverse_directivity
* error_term_reverse_source_match
* error_term_reverse_reflection_tracking
* error_term_reverse_load_match
* error_term_reverse_transmission_tracking
* error_term_reverse_isolation
'''

def adjust_through(frequency_response, error_term_forward_transmission_tracking):
    assert len(frequency_response) == len(error_term_forward_transmission_tracking)
    return np.divide(frequency_response, error_term_forward_transmission_tracking)

def fade_out_and_interpolate_range(frequency_response, range_length=8, range_center=None):
    ''' Fade out and interpolate a range of values from the frequency response (default: remove DC bias) '''
    if range_center == None:
        range_center = len(frequency_response) / 2
    range_start = range_center - range_length / 2
    range_end = range_start + range_length
    index = np.arange(len(frequency_response))
    index_clip = np.concatenate((index[:range_start],index[range_end:]))
    frequency_response_clip = np.array(frequency_response)[[index_clip]]
    return np.interp(x=index, xp=index_clip, fp=frequency_response_clip)