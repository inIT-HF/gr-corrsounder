import unittest
import numpy as np
from . import *

class Corrsounder(unittest.TestCase):
    def test_sequence_frank_zadoff_chu(self):
        ''' Check exemplary FZC sequence '''
        N_seq = 10
        q = 1
        res = corrsounder.sequence_frank_zadoff_chu(N_seq, q)
        exp = [(-1+1.2246467991473533e-15j), (1-1.2246467991473533e-15j), (-1+1.2246467991473533e-15j), (1-1.2246467991473533e-15j), (-1+1.2246467991473533e-15j), (1-1.2246467991473533e-15j), (-1+1.2246467991473533e-15j), (1-1.2246467991473533e-15j), (-1+1.2246467991473533e-15j), (1-1.2246467991473533e-15j)]
        np.testing.assert_almost_equal(res, exp)

    def test_sequence_maximum_length(self):
        ''' Check exemplary MLS'''
        N_seq = 7
        res = corrsounder.sequence_maximum_length(N_seq)
        exp = [(1+0j), (1+0j), (1+0j), (-1+0j), (1+0j), (-1+0j), (-1+0j)]
        np.testing.assert_almost_equal(res, exp)

    def test_cross_correlate_sequences(self):
        ''' Cross-correlate random complex sequences '''
        N_seq = 10
        seq0 =  np.random.rand(N_seq) + 1j*np.random.rand(N_seq)
        seq1 = np.random.rand(N_seq) + 1j * np.random.rand(N_seq)
        res = corrsounder.cross_correlate_sequences(seq0, seq1)
        exp_zero_tap = np.sum(np.multiply(seq0, np.conj(seq1)))
        self.assertEqual(len(res), N_seq*2-1)
        self.assertAlmostEqual(res[N_seq-1], exp_zero_tap)

    def test_cross_correlate_peridoc_sequences(self):
        ''' Test with circular cross-correlation theorem '''
        N_seq = 10
        seq0 = np.random.rand(N_seq) + 1j * np.random.rand(N_seq)
        seq1 = np.random.rand(N_seq) + 1j * np.random.rand(N_seq)
        res = corrsounder.cross_correlate_peridoc_sequences(seq0, seq1)
        Seq0 = np.fft.fft(seq0)
        Seq1 = np.fft.fft(seq1)
        exp = np.fft.ifft(np.multiply(np.conj(Seq0), Seq1))
        np.testing.assert_almost_equal(res, exp)

    def test_auto_correlate_sequence(self):
        ''' Auto-correlate random complex sequences '''
        N_seq = 10
        seq =  np.random.rand(N_seq) + 1j*np.random.rand(N_seq)
        res = corrsounder.auto_correlate_sequence(seq)
        exp_zero_tap = np.sum(np.multiply(seq, np.conj(seq)))
        self.assertEqual(len(res), N_seq*2-1)
        self.assertAlmostEqual(res[N_seq-1], exp_zero_tap)

    def test_auto_correlate_peridoc_sequence(self):
        ''' Test with circular auto-correlation theorem '''
        N_seq = 10
        seq = np.random.rand(N_seq) + 1j * np.random.rand(N_seq)
        res = corrsounder.auto_correlate_peridoc_sequence(seq)
        Seq = np.fft.fft(seq)
        exp = np.fft.ifft(np.multiply(np.conj(Seq), Seq))
        np.testing.assert_almost_equal(res, exp)

class TransmissionFactor(unittest.TestCase):
    def test_transmission_factor(self):
        ''' Test TF based on known IR '''
        N_ir = 8
        ir = np.array([0,]*N_ir)
        ir[0:3] = [0.1,0.8,0.1]

        F_c = 1e9
        T_s = 1e-6
        frequency_response = np.fft.fft(ir, norm="ortho")
        tf = transmission_factor.transmission_factor(frequency_response=frequency_response,
                                                     frequency_center=F_c,
                                                     bandwidth=1./T_s)
        self.assertAlmostEqual(tf.frequency_center, F_c)
        self.assertAlmostEqual(tf.time_resolution, T_s)
        self.assertEqual(tf.number_points, N_ir)

        self.assertEqual(len(ir), len(tf.impulse_response))
        for sample_exp, sample_res in zip(ir, tf.impulse_response):
            self.assertAlmostEqual(sample_exp, sample_exp)

    def test_extract_band(self):
        N_fr = 8
        F_c = 1e9
        F_bw = 1e6
        fr = fr = np.array([1.,]*N_fr)
        tf = transmission_factor.transmission_factor(frequency_response=fr, frequency_center=F_c, bandwidth=F_bw)
        F_bw_new = F_bw/2.0
        tf_new = tf.extract_band(frequency_center=F_c, bandwidth=F_bw_new)

        self.assertEqual(tf_new.number_points, N_fr/2+1)
        exp = np.array([1., ] * (N_fr/2+1))
        res = tf_new.frequency_response
        for sample_exp, sample_res in zip(exp, res):
            self.assertAlmostEqual(sample_exp, sample_exp)

    def test_histogram(self):
        N_fr = 8
        F_c = 1e9
        F_bw = 1e6
        fr = np.array([1., ] * N_fr)
        tf = transmission_factor.transmission_factor(frequency_response=fr, frequency_center=F_c, bandwidth=F_bw)
        hist, bin_centers = tf.histogram(bin_count=3, range_max=2.5, range_min=-0.5)

        np.testing.assert_almost_equal(bin_centers, [0., 1., 2.])
        np.testing.assert_almost_equal(hist, [0., 1., 0.])

    def test_norm_rician_generator(self):
        # TODO: Add unit test Normalized Rician distribution generator
        self.assertEqual(True, False)

    def test_estimate_rician(self):
        # TODO: Add unit test Normalized Rician distribution estimator
        self.assertEqual(True, False)

    def test_estimate_path_loss_exponent(self):
        ''' Test ideal path-loss conditions '''
        N_fr = 8
        F_c = 1e6
        F_bw = 1e0
        d = 1e3
        G_ant = 1.0
        fspl = (4.* np.pi * d * F_c / 3e8)**2
        fr = np.sqrt([1./fspl, ] * N_fr)
        tf = transmission_factor.transmission_factor(frequency_response=fr, frequency_center=F_c, bandwidth=F_bw)
        n, _ = tf.estimate_path_loss_exponent(antenna_gain=G_ant, distance=d)
        self.assertAlmostEqual(n, 2.00, places=3)

    def test_estimate_frequency_edge(self):
        N_fr = 8
        F_c = 1e9
        F_bw = 1e6
        fr = np.array([1., ] * N_fr)
        fr[0] = 0.
        tf = transmission_factor.transmission_factor(frequency_response=fr, frequency_center=F_c, bandwidth=F_bw)
        edge_frequency, edge_index = tf.estimate_frequency_edge()

        self.assertEqual(edge_index, 1)
        self.assertAlmostEqual(edge_frequency, F_c - F_bw/2.0 + F_bw/float(N_fr))

class UtilsTestCase(unittest.TestCase):
    def test_fraction_to_dB(self):
        self.assertAlmostEqual(utils.fraction_to_dB(1), 0.0)
        self.assertAlmostEqual(utils.fraction_to_dB(10), 10.0)

    def test_generator_read_raw_complex64_frame(self):
        g = utils.generator_read_raw_complex64_frame('fzc-capture-seq_len_255-q_7-snr_0dB.dat', 255)
        filesize = 6120
        n_sequences = 0
        for sequence in g:
            n_sequences += 1

        self.assertAlmostEqual(np.floor(filesize/8/255), n_sequences)

    def test_discrete_fourier_transform(self):
        N = 8
        x = [1.,]*N
        X = [0.,]*N
        X[N/2] = N
        res = utils.discrete_fourier_transform(x)
        np.testing.assert_almost_equal(res, X)

    def test_discrete_fourier_transform_frequency(self):
        N = 8
        T_s = 1.
        df = 1./float(T_s*N)
        f_start = -1./(2.*T_s)
        exp = f_start + df * np.arange(N)
        res = utils.discrete_fourier_transform_frequency(n_fft=N, time_resolution=T_s)
        np.testing.assert_almost_equal(res, exp)

    def test_inverse_discrete_fourier_transform(self):
        N = 8
        x = [1.,]*N
        X = [0.,]*N
        X[N/2] = N
        res = utils.inverse_discrete_fourier_transform(X)
        np.testing.assert_almost_equal(res, x)

    def test_inverse_discrete_fourier_transform_time(self):
        N = 8
        T_s = 1.
        exp = T_s * np.arange(N)
        res = utils.inverse_discrete_fourier_transform_time(n_ifft=N, bandwidth=1./T_s)
        np.testing.assert_almost_equal(res, exp)

class ErrorCorrectionTestCase(unittest.TestCase):
    def test_adjust_through(self):
        error_term = (0.5+0j, )*10
        frequency_response = (1.0+0j, )*10
        exp = np.divide(frequency_response, error_term)
        res = error_correction.adjust_through(frequency_response, error_term)
        self.assertEqual(len(exp), len(res))
        for i in range(len(frequency_response)):
            self.assertAlmostEquals(exp[i], res[i])

    def test_fade_out_and_interpolate_range(self):
        frequency_response = [1.0 + 0j,] * 10
        frequency_response[5] = 10. + 0j # DC bias

        res = error_correction.fade_out_and_interpolate_range(frequency_response=frequency_response, range_length=1, range_center=5)
        exp = [1.0 + 0j, ] * 10
        for i in range(len(frequency_response)):
            self.assertAlmostEquals(exp[i], res[i])

if __name__ == '__main__':
    unittest.main()
