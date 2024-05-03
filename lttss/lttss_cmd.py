import argparse
from utils import get_config
import cmd_impl

parser = argparse.ArgumentParser(description='TTS Command')

parser.add_argument('-r', '--run', action='store_true', help='Run the server.', default=False)
parser.add_argument('-p', '--play', action='store_true', help='Generate and play the sound.', default=False)
parser.add_argument('-ap', '--append-to-play', action='store_true', help='Append the text at the end of the generated sound.', default=False)
parser.add_argument('-s', '--speed-up', action='store_true', help='Speed up the sound.', default=False)
parser.add_argument('-d', '--speed-down', action='store_true', help='Speed down the sound.', default=False)
parser.add_argument('-e', '--export', action='store_true', help='Export the sound.', default=False)
parser.add_argument('-pp', '--play-pause', action='store_true', help='Pause the sound.', default=False)
parser.add_argument('-b', '--back', action='store_true', help='Go back.', default=False)
parser.add_argument('-l', '--lang', help='Language of the text.', default="english")

args = parser.parse_args()

config = get_config()

if args.run:
    cmd_impl.run(config)

elif args.play:
    cmd_impl.play_selected(config, args.lang)

elif args.append_to_play:
    cmd_impl.append_selected(config, args.lang)

elif args.speed_up:
    cmd_impl.speedup(config)

elif args.speed_down:
    cmd_impl.speeddown(config)

elif args.export:
    cmd_impl.export_selected(config, args.lang)

elif args.play_pause:
    cmd_impl.toggle_pause(config)

elif args.back:
    cmd_impl.back(config)