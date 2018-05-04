import numpy as np
from scipy import constants
from scipy.special import i0
from scipy.stats import rv_continuous
import utils

class norm_rician_generator(rv_continuous):
    "Normalized Rician distribution (see Proakis)"
    def _pdf(self, a, v, sigma):
        sigma_sqr = sigma**2
        return a/sigma_sqr * i0(a*v/sigma_sqr) * np.exp(- (a**2 + v**2) / (2. * sigma_sqr))

class transmission_factor:
    def __init__(self, frequency_response, frequency_center, bandwidth):
        
        self.frequency_response = np.array(frequency_response)
        self.frequency_response_magnitude = np.abs(self.frequency_response)
        
        self.psd = np.square(self.frequency_response_magnitude)
        self.psd_dB = utils.fraction_to_dB(self.psd)
        
        self.H_median, self.H_10, self.H_90 = np.percentile(self.frequency_response_magnitude, (50., 10., 90.))
        
        self.frequency_center = frequency_center
        self.bandwidth = bandwidth
        self.time_resolution = 1./self.bandwidth
        
        self.number_points = len(self.frequency_response)
        
        self.impulse_response = utils.inverse_discrete_fourier_transform(self.frequency_response)
        self.impulse_response_magnitude = np.abs(self.impulse_response)
        
        self.frequency_axis = utils.discrete_fourier_transform_frequency(self.number_points, self.time_resolution, self.frequency_center)
        self.time_axis = utils.inverse_discrete_fourier_transform_time(self.number_points, self.bandwidth)

        self.pdp = np.square(self.impulse_response_magnitude)
        self.pdp_dB = utils.fraction_to_dB(self.pdp)

        self.tau_mean = np.sum(self.pdp*self.time_axis)/np.sum(self.pdp)
        #self.tau_mean = np.average(a=self.pdp, weights=self.time_axis)
        self.tau_rms = np.sqrt(np.sum((self.time_axis-self.tau_mean)**2 * self.pdp)/np.sum(self.pdp))
        
    
    def extract_band(self, frequency_center, bandwidth):
        ''' Extract some band from the channel response '''
        indices = [i for i,f in enumerate(self.frequency_axis) if abs(f-frequency_center) <= bandwidth/2.]
        return transmission_factor(self.frequency_response[indices], frequency_center, bandwidth)
    
    def histogram(self, bin_count = 61, range_max = 3e-3, range_min = 0.0):
        ''' Histogram of magnitude '''
        hist, bin_edges = np.histogram(self.frequency_response_magnitude,
                                       bins = bin_count,
                                       range=[range_min, range_max],
                                       density=True)
        
        # Arrange centers
        bin_centers = (bin_edges[:-1]+bin_edges[1:])/2.0
        
        return hist, bin_centers

    def estimate_rician(self):
        ''' Fit normalized Rician distribution (see Proakis) '''
        rician = norm_rician_generator()
        v, sigma, _, _ = rician.fit(self.frequency_response_magnitude,
                                    floc=0.0, fscale=1.0)
        rician_frozen = rician.__call__(v, sigma, loc=0.0, scale=1.0)
        rician_frozen.K = v**2/sigma**2
        return rician_frozen.K, v, sigma, rician_frozen

    def estimate_path_loss_exponent(self, distance, antenna_gain=1.0):
        ''' Estimate path-loss exponent with a given antenna gain and and distance '''
        pl = np.square(antenna_gain) / np.square(np.abs(self.frequency_response))
        n = np.log(np.array(pl))/np.log(4.*np.pi*np.array(distance)*np.array(self.frequency_axis)/constants.c)
        return np.mean(n), np.std(n)

    def estimate_frequency_edge(self, magnitude_ratio=1./2.**0.5):
        ''' Compute frequency edge of channel gain (default: half-power bandwidth) '''
        edge_index = np.where(self.psd >= np.max(self.psd) * magnitude_ratio)[0][0]
        edge_frequency = self.frequency_axis[edge_index]
        return edge_frequency, edge_index
