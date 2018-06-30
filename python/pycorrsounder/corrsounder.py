import numpy as np

def sequence_frank_zadoff_chu(sequence_length, q):
    return [pow(-1, q * i) * np.exp(1j * np.pi * q * sequence_length * sequence_length / sequence_length) for i in range(1, sequence_length + 1)]

# Source: gnuradio/gr-digital/lib/glfsr.cc
glfsr_polynomial_masks = [
    0x00000000,
    0x00000001,		# x^1 + 1
    0x00000003,     # x^2 + x^1 + 1
    0x00000005,     # x^3 + x^1 + 1
    0x00000009,		# x^4 + x^1 + 1
    0x00000012,		# x^5 + x^2 + 1
    0x00000021,		# x^6 + x^1 + 1
    0x00000041,     #/ x^7 + x^1 + 1
    0x0000008E,		# x^8 + x^4 + x^3 + x^2 + 1
    0x00000108,		# x^9 + x^4 + 1
    0x00000204,		# x^10 + x^4 + 1
    0x00000402,		# x^11 + x^2 + 1
    0x00000829,		# x^12 + x^6 + x^4 + x^1 + 1
    0x0000100D,		# x^13 + x^4 + x^3 + x^1 + 1
    0x00002015,		# x^14 + x^5 + x^3 + x^1 + 1
    0x00004001,		# x^15 + x^1 + 1
    0x00008016,		# x^16 + x^5 + x^3 + x^2 + 1
    0x00010004,		# x^17 + x^3 + 1
    0x00020013,		# x^18 + x^5 + x^2 + x^1 + 1
    0x00040013,		# x^19 + x^5 + x^2 + x^1 + 1
    0x00080004,		# x^20 + x^3 + 1
    0x00100002,		# x^21 + x^2 + 1
    0x00200001,		# x^22 + x^1 + 1
    0x00400010,		# x^23 + x^5 + 1
    0x0080000D,		# x^24 + x^4 + x^3 + x^1 + 1
    0x01000004,		# x^25 + x^3 + 1
    0x02000023,		# x^26 + x^6 + x^2 + x^1 + 1
    0x04000013,		# x^27 + x^5 + x^2 + x^1 + 1
    0x08000004,		# x^28 + x^3 + 1
    0x10000002,		# x^29 + x^2 + 1
    0x20000029,		# x^30 + x^4 + x^1 + 1
    0x40000004,		# x^31 + x^3 + 1
    0x80000057		# x^32 + x^7 + x^5 + x^3 + x^2 + x^1 + 1
    ]

# Source: gnuradio/gr-digital/include/glfsr.h
def sequence_maximum_length(sequence_length):
    degree = int(np.ceil(np.log2(sequence_length)))
    mask = glfsr_polynomial_masks[degree]
    shift_register = 1
    out = []
    for n in range(sequence_length):
        bit = shift_register & 1
        out.append(float(bit) * 2. -1.)
        shift_register >>= 1
        if bit:
            shift_register ^= mask
    return np.array(out)

def cross_correlate_sequences(sequence_one, sequence_two):
    return np.correlate(np.array(sequence_one), np.array(sequence_two), mode='full')

def cross_correlate_peridoc_sequences(sequence_one, sequence_two):
    N = max(len(sequence_one), len(sequence_two))
    return np.fft.ifft(np.multiply(np.conj(np.fft.fft(sequence_one, n=N)), np.fft.fft(sequence_two, n=N)))

def auto_correlate_sequence(sequence):
    return np.correlate(np.array(sequence), np.array(sequence), mode='full')

def auto_correlate_peridoc_sequence(sequence):
    return np.fft.ifft(np.multiply(np.conj(np.fft.fft(sequence)), np.fft.fft(sequence)))