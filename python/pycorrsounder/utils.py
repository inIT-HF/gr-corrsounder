import numpy as np

def fraction_to_dB(fraction):
    return 10*np.log10(np.abs(fraction))

def generator_read_raw_complex64_frame(file_name, frame_length):
    ''' Generator to read binary *frame_length* complex64 samples from file *file_name* '''
    with open(file_name, mode='rb') as f:
        while True:
            frame = np.frombuffer(f.read(frame_length*8), dtype=np.complex64)
            if len(frame) != frame_length:
                break
            yield frame

def discrete_fourier_transform(x):
    return np.fft.fftshift(np.fft.fft(x))

def discrete_fourier_transform_frequency(n_fft, time_resolution, center_frequency=0.0):
    return np.fft.fftshift(np.fft.fftfreq(n=n_fft, d=time_resolution)) + center_frequency

def inverse_discrete_fourier_transform(X):
    return np.fft.ifft(np.fft.ifftshift(X))

def inverse_discrete_fourier_transform_time(n_ifft, bandwidth):
    return np.linspace(0., float(n_ifft-1)/bandwidth, num=n_ifft)