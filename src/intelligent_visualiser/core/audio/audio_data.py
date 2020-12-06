import struct
import wave

import numpy as np
import soundfile as sf


class AudioData:

    def __init__(self, audio_path):
        self.audio_path = audio_path
        self.audio_data, self.samplerate = sf.read(audio_path)
        self.duration = self.audio_data.shape[0] / self.samplerate

    @staticmethod
    def fft_from_wav(file_name, channels, sample_size, rate, n_fft, fps):
        max_y = 2.0 ** (sample_size * 8 - 1)
        with wave.open(file_name, 'rb') as wf:
            assert wf.getnchannels() == channels
            assert wf.getsampwidth() == sample_size
            assert wf.getframerate() == rate

            frames = wf.getnframes()

            freq_list = []
            for i in range(0, int((frames / rate) * fps)):
                N = (int((i + 1) * rate / fps) - wf.tell()) / n_fft
                if not N:
                    return
                N = int(N * n_fft)
                data = wf.readframes(N)

                y = np.array(struct.unpack("%dh" % (len(data) / sample_size), data)) / max_y
                y_L = y[::2]
                y_R = y[1::2]

                Y_L = np.fft.fft(y_L, n_fft)
                Y_R = np.fft.fft(y_R, n_fft)

                Y = abs(np.hstack((Y_L[int(-n_fft / 2):-1], Y_R[:int(n_fft / 2)])))

                freq_list.append(Y)

        avg_freq = []

        for i in range(0, len(freq_list) - 1):
            x = []
            for j in range(0, len(freq_list[i]) - 1):
                x.append((freq_list[i][j] - freq_list[i][j + 1]) ** 2)
            avg_freq.append(np.sum(x) / len(x))

        return avg_freq

    def get_interval_data(self, start, end):
        if end >= self.duration:
            end = self.duration

        return self.audio_data[int(self.samplerate * start): int(self.samplerate * end)]


