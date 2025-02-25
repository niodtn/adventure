import sys
import numpy as np
import wave
import matplotlib.pyplot as plt


def main():
    print("Hello from shot!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("python main.py <sound file path>")
        sys.exit(1)

    path = sys.argv[1]
    # Open the WAV file
    with wave.open(path, 'rb') as wav_file:
        # Extract Raw Audio from Wav File
        signal = wav_file.readframes(-1)
        signal = np.frombuffer(signal, dtype=np.int16)

        # Get the frame rate
        framerate = wav_file.getframerate()

        # Perform FFT
        fft_spectrum = np.fft.fft(signal)
        freq = np.fft.fftfreq(len(fft_spectrum), 1.0/framerate)

        # Plot the FFT spectrum
        plt.figure(figsize=(12, 6))
        plt.plot(freq, np.abs(fft_spectrum))
        plt.title('FFT of the WAV file')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Amplitude')
        plt.xlim(0, framerate / 2)
        plt.show()

    main()
