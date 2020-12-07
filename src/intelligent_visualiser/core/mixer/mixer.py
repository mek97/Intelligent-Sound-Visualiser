import ffmpeg


class Mixer:
    @staticmethod
    def join_audio_video(video_path, audio_path, duration, output_path):
        input_video = ffmpeg.input(video_path).filter('trim', duration=duration)

        input_audio = ffmpeg.input(audio_path).filter('atrim', duration=duration)

        ffmpeg.concat(input_video, input_audio, v=1, a=1).output(output_path).run(overwrite_output=True)
