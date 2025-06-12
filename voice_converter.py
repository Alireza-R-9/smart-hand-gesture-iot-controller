import os
from pydub import AudioSegment
import librosa
import soundfile as sf

INPUT_DIR = "music"
OUTPUT_DIR = "music/processed"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def convert_mp3_to_wav(mp3_path, wav_path):
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")


def change_pitch(input_wav, output_wav, n_steps):
    y, sr = librosa.load(input_wav, sr=None)
    y_shifted = librosa.effects.pitch_shift(y=y, sr=sr, n_steps=n_steps)
    sf.write(output_wav, y_shifted, sr)


def convert_wav_to_mp3(wav_path, mp3_path):
    audio = AudioSegment.from_wav(wav_path)
    audio.export(mp3_path, format="mp3")


def convert_voice(input_mp3_path, to_gender="female"):
    base_name = os.path.basename(input_mp3_path).replace(".mp3", "")

    temp_wav = os.path.join(OUTPUT_DIR, base_name + "_temp.wav")
    processed_wav = os.path.join(OUTPUT_DIR, base_name + f"_{to_gender}.wav")
    output_mp3_path = os.path.join(OUTPUT_DIR, base_name + f"_{to_gender}.mp3")

    try:
        convert_mp3_to_wav(input_mp3_path, temp_wav)

        pitch_steps = 4 if to_gender == "female" else -4

        change_pitch(temp_wav, processed_wav, pitch_steps)
        convert_wav_to_mp3(processed_wav, output_mp3_path)

        print(f"[✔] فایل تبدیل‌شده ذخیره شد: {output_mp3_path}")
    except Exception as e:
        print(f"[!] خطا هنگام تبدیل {input_mp3_path}: {e}")
    finally:
        if os.path.exists(temp_wav):
            os.remove(temp_wav)
        if os.path.exists(processed_wav):
            os.remove(processed_wav)


if __name__ == "__main__":

    sample_file = os.path.join(INPUT_DIR, "song2.mp3")
    convert_voice(sample_file, to_gender="female")
    convert_voice(sample_file, to_gender="male")
