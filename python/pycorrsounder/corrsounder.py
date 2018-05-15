import numpy as np

def sequence_frank_zadoff_chu(sequence_length, q):
    return [pow(-1, q * i) * np.exp(1j * np.pi * q * sequence_length * sequence_length / sequence_length) for i in range(1, sequence_length + 1)]

def sequence_maximum_length(sequence_length):
    return []

def cross_correlate_sequences(sequence_one, sequence_two):
    return np.correlate(np.array(sequence_one), np.array(sequence_two), mode='full')

def cross_correlate_peridoc_sequences(sequence_one, sequence_two):
    N = max(len(sequence_one), len(sequence_two))
    return np.fft.ifft(np.multiply(np.conj(np.fft.fft(sequence_one, n=N)), np.fft.fft(sequence_two, n=N)))

def auto_correlate_sequence(sequence):
    return np.correlate(np.array(sequence), np.array(sequence), mode='full')

def auto_correlate_peridoc_sequence(sequence):
    return np.fft.ifft(np.multiply(np.conj(np.fft.fft(sequence)), np.fft.fft(sequence)))