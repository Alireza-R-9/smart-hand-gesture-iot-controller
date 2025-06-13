import os
import vlc


class MusicController:
    def __init__(self, music_folder):
        self.music_folder = music_folder
        self.processed_folder = os.path.join(music_folder, "processed")
        self.voice_gender = "male"
        self.player = vlc.MediaPlayer()
        self.track_list = self.load_tracks()
        self.track_index = 0

        if self.track_list:
            self.load_track(self.track_index)
            self.play()

    def load_tracks(self):
        return [file for file in os.listdir(self.music_folder) if file.endswith('.mp3')]

    def get_processed_track_path(self, filename):
        name, _ = os.path.splitext(filename)
        processed_filename = f"{name}_{self.voice_gender}.mp3"
        processed_path = os.path.join(self.processed_folder, processed_filename)
        return processed_path if os.path.exists(processed_path) else os.path.join(self.music_folder, filename)

    def load_track(self, index):
        if 0 <= index < len(self.track_list):
            original_file = self.track_list[index]
            track_path = self.get_processed_track_path(original_file)
            self.player.set_media(vlc.Media(track_path))

    def play(self):
        if not self.player.is_playing():
            self.player.play()

    def pause(self):
        if self.player.is_playing():
            self.player.pause()

    def stop(self):
        self.player.stop()

    def next_track(self):
        self.track_index = (self.track_index + 1) % len(self.track_list)
        self.load_track(self.track_index)
        self.play()

    def previous_track(self):
        self.track_index = (self.track_index - 1) % len(self.track_list)
        self.load_track(self.track_index)
        self.play()

    def set_volume(self, volume):  # مقدار بین ۰ تا ۱
        volume = int(max(0, min(volume, 1)) * 100)
        self.player.audio_set_volume(volume)

    def set_playback_speed(self, speed):  # سرعت بین 0.5 تا 2.0
        if 0.5 <= speed <= 2.0:
            self.player.set_rate(speed)

    def toggle_voice_gender(self):
        self.voice_gender = "female" if self.voice_gender == "male" else "male"
        print(f"[Voice Gender] Switched to {self.voice_gender}")
        self.load_track(self.track_index)
        self.play()
