import argparse
import logging
from pathlib import Path

from intelligent_visualiser.core.audio.audio_data import AudioData
from intelligent_visualiser.core.audio.audio_stream import AudioStream
from intelligent_visualiser.core.mixer.mixer import Mixer
from intelligent_visualiser.core.video.live_polar_animator import LivePolarAnimator
from intelligent_visualiser.core.video.polar_animator import PolarAnimator
from intelligent_visualiser.utils.config_utils import ConfigUtils
from intelligent_visualiser.utils.constants import PolarAnimationTypes


def main():
    default_output_dir = Path(ConfigUtils.get_output_directory())
    parser = argparse.ArgumentParser(description='CLI for Intelligent Music visualizer')
    parser.add_argument('--log_level', default=logging.INFO, type=int, help="Logging level")
    parser.add_argument('--duration', type=int, default=5, help="Duration in seconds")
    parser.add_argument('--fps', type=int, default=40, help="FPS")
    parser.add_argument('--save', action='store_true', help="Save animation")
    parser.add_argument('--speed', type=int, default=0.005, help="Animation speed")
    parser.add_argument('--video_file', default=str(default_output_dir.joinpath("video_output.mp4")),
                        help="Animation file output path")
    parser.add_argument('--output_file', default=str(default_output_dir.joinpath("animation_output.mp4")),
                        help="Video only file output path")

    subparsers = parser.add_subparsers(title='Modes', dest='mode', required=True)

    live_input_parser = subparsers.add_parser('live_input', help='Record audio  data and process it')
    live_input_parser.add_argument('--template', default=PolarAnimationTypes.SPIRAL, help="Animation template")

    live_input_parser.add_argument('--record_audio_file', default=str(default_output_dir.joinpath("audio_output.wav")),
                                   help="Record audio file output path")

    live_input_parser.add_argument('--speed', type=int, default=0.005, help="Animation speed")

    load_data_parser = subparsers.add_parser('data_input', help='Loads data from a file and process it')
    load_data_parser.add_argument('--template', default="SPIRAL", help="Animation template")
    load_data_parser.add_argument('--music_file',
                                  default=str(default_output_dir.joinpath("audio_data").joinpath("sample.wav")),
                                  help="Music file input path in wav format")

    load_data_parser.add_argument('--speed', type=int, default=0.005, help="Animation speed")

    args = parser.parse_args()

    log_level = args.log_level
    duration_arg = args.duration
    fps_arg = args.fps
    video_file_arg = args.video_file
    output_file_arg = args.output_file
    save_arg = args.save
    speed_arg = args.speed

    logging.basicConfig()
    logging.root.setLevel(level=log_level)

    mode = args.mode
    if mode == "live_input":
        record_audio_file_arg = args.record_audio_file
        template_arg = args.template

        audio_stream = AudioStream(duration_arg, save_arg, {"file": record_audio_file_arg})
        audio_stream.start()

        polar_animation = LivePolarAnimator(template_arg, duration_arg, fps_arg, speed_arg)
        polar_animation.generate(audio_stream, save_arg, video_file_arg)

        if save_arg:
            Mixer.join_audio_video(video_file_arg, record_audio_file_arg, duration_arg, output_file_arg)

    elif mode == "data_input":
        music_file_arg = args.music_file
        template_arg = args.template
        audio_data = AudioData(music_file_arg)

        polar_animation = PolarAnimator(template_arg, duration_arg, fps_arg, speed_arg)
        polar_animation.generate(audio_data, save_arg, video_file_arg)

        if save_arg:
            Mixer.join_audio_video(video_file_arg, music_file_arg, duration_arg, output_file_arg)


if __name__ == '__main__':
    main()
