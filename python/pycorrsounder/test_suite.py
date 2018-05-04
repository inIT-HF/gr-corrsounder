import unittest
import numpy as np
import transmission_factor as tf
import error_correction as ec
from utils import *

class Corrsounder(unittest.TestCase):
    def test_sequence_frank_zadoff_chu(self):
        self.assertEqual(True, False)

    def test_sequence_maximum_length(self):
        self.assertEqual(True, False)

    def test_cross_correlate_sequences(self):
        self.assertEqual(True, False)

    def test_cross_correlate_peridoc_sequences(self):
        self.assertEqual(True, False)

    def test_auto_correlate_sequences(self):
        self.assertEqual(True, False)

    def test_auto_correlate_peridoc_sequences(self):
        self.assertEqual(True, False)

class TransmissionFactor(unittest.TestCase):
    def test_transmission_factor(self):
        self.assertEqual(True, False)

    def test_norm_rician_generator(self):
        self.assertEqual(True, False)

    def test_extract_band(self):
        self.assertEqual(True, False)

    def test_histogram(self):
        self.assertEqual(True, False)

    def test_estimate_rician(self):
        self.assertEqual(True, False)

    def test_estimate_path_loss_exponent(self):
        self.assertEqual(True, False)

    def test_estimate_frequency_edge(self):
        self.assertEqual(True, False)

class UtilsTestCase(unittest.TestCase):
    def test_fraction_to_dB(self):
        self.assertAlmostEqual(fraction_to_dB(1), 0.0)
        self.assertAlmostEqual(fraction_to_dB(10), 10.0)

    def test_generator_read_raw_complex64_frame(self):
        g = generator_read_raw_complex64_frame('fzc-capture-seq_len_255-q_7-snr_0dB.dat', 255)
        filesize = 6120
        n_sequences = 0
        for sequence in g:
            n_sequences += 1

        self.assertAlmostEqual(np.floor(filesize/8/255), n_sequences)

    def test_discrete_fourier_transform(self):
        self.assertEqual(True, False)

    def test_discrete_fourier_transform_frequency(self):
        self.assertEqual(True, False)

    def test_inverse_discrete_fourier_transform(self):
        self.assertEqual(True, False)

    def test_inverse_discrete_fourier_transform_time(self):
        self.assertEqual(True, False)

class ErrorCorrectionTestCase(unittest.TestCase):
    def test_adjust_through(self):
        error_term = (0.5+0j, )*10
        frequency_response = (1.0+0j, )*10
        exp = np.divide(frequency_response, error_term)
        res = ec.adjust_through(frequency_response, error_term)
        self.assertEqual(len(exp), len(res))
        for i in range(len(frequency_response)):
            self.assertAlmostEquals(exp[i], res[i])

    def test_fade_out_and_interpolate_range(self):
        frequency_response = [1.0 + 0j,] * 10
        frequency_response[5] = 10. + 0j # DC bias

        res = ec.fade_out_and_interpolate_range(frequency_response=frequency_response, range_length=1, range_center=5)
        exp = [1.0 + 0j, ] * 10
        for i in range(len(frequency_response)):
            self.assertAlmostEquals(exp[i], res[i])

if __name__ == '__main__':
    unittest.main()
