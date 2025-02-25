import logging
import sys
import wave

import colorlog
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

from utils import select

handler = colorlog.StreamHandler()
formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)-8s %(message)s",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "white",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
)
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def freq_to_note(freq):
    A440 = 440.0
    if freq == 0:
        return None
    midi_num = 69 + 12 * np.log2(freq / A440)
    return round(midi_num)


def process_wav_file(path):
    logging.info(f"Starting to process WAV file: {path}")

    y, sr = librosa.load(path, sr=44100)
    fft_result = np.fft.fft(y)
    freqs = np.fft.fftfreq(len(fft_result), 1 / sr)

    valid_freqs = (freqs > 80) & (freqs < 1200)
    fft_magnitude = np.abs(fft_result[valid_freqs])
    freqs = freqs[valid_freqs]

    midi_notes = [freq_to_note(f) for f in freqs]
    midi_notes = list(set(filter(None, midi_notes)))

    note_names = librosa.midi_to_note(midi_notes)
    print("🎸 검출된 노트:", note_names)

    plt.figure(figsize=(12, 6))
    plt.plot(freqs, fft_magnitude)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.title("FFT Spectrum of Guitar Audio")
    plt.show()


def process_wav_file_old(path):
    try:
        logging.info(f"Processing WAV file: {path}")
        # Open the WAV file
        with wave.open(path, "rb") as wav_file:
            # Extract Raw Audio from Wav File
            signal = wav_file.readframes(-1)
            signal = np.frombuffer(signal, dtype=np.int16)

            # Get the frame rate
            framerate = wav_file.getframerate()

            # Perform FFT
            fft_spectrum = np.fft.fft(signal)
            freq = np.fft.fftfreq(len(fft_spectrum), 1.0 / framerate)

            # Plot the FFT spectrum
            plt.figure(figsize=(12, 6))
            plt.plot(freq, np.abs(fft_spectrum))
            plt.title("FFT of the WAV file")
            plt.xlabel("Frequency (Hz)")
            plt.ylabel("Amplitude")
            plt.xlim(0, framerate / 2)
            plt.show()
    except wave.Error as e:
        if "unknown format: 3" in str(e):
            logging.error(f"Error processing WAV file: {e}")
            # Handle the specific error related to the WAV file format
        else:
            logging.error(f"Error processing WAV file: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


def main():
    options = ["test1", "test2", "test3"]
    selected = select.menu(options)

    logging.info(f"User selected {selected}.")


if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print("python main.py <sound file path>")
    #     sys.exit(1)

    # path = sys.argv[1]
    # process_wav_file(path)
    main()
