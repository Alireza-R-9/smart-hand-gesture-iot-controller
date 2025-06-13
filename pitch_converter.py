import os
import librosa
import soundfile as sf

MUSIC_FOLDER = "music"
OUTPUT_FOLDER = os.path.join(MUSIC_FOLDER, "frequency_versions")
PITCH_LEVELS = {
    "very_low": 0.75,
    "low": 0.9,
    "medium": 1.0,
    "high": 1.15,
    "very_high": 1.3
}


def ensure_output_folder():
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)


def change_pitch(audio_path, pitch_factor, output_path):
    """تغییر فرکانس فایل صوتی با استفاده از librosa"""
    try:
        y, sr = librosa.load(audio_path, sr=None)
        y_shifted = librosa.effects.pitch_shift(y=y, sr=sr, n_steps=12 * (pitch_factor - 1))
        sf.write(output_path, y_shifted, sr)
        print(f"[✓] ذخیره شد: {output_path}")
    except Exception as e:
        print(f"[!] خطا در تبدیل {audio_path}: {e}")


def convert_all_tracks():
    ensure_output_folder()
    print("🎵 شروع تبدیل فرکانس‌ها...")

    for filename in os.listdir(MUSIC_FOLDER):
        if filename.endswith(".mp3"):
            source_path = os.path.join(MUSIC_FOLDER, filename)
            name, _ = os.path.splitext(filename)

            for level_name, factor in PITCH_LEVELS.items():
                output_filename = f"{name}_{level_name}.wav"
                output_path = os.path.join(OUTPUT_FOLDER, output_filename)
                if not os.path.exists(output_path):
                    change_pitch(source_path, factor, output_path)
                else:
                    print(f"[!] موجود است: {output_filename}")


if __name__ == "__main__":
    convert_all_tracks()
