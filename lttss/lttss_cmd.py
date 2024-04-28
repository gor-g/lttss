import argparse
import tts_server_config
import cmd_impl

parser = argparse.ArgumentParser(description='TTS Command')

parser.add_argument('-r', '--run', action='store_true', help='Run the server.', default=False)
parser.add_argument('-p', '--play', action='store_true', help='Generate and play the sound.', default=False)
parser.add_argument('-ap', '--append-to-play', action='store_true', help='Append the text at the end of the generated sound.', default=False)
parser.add_argument('-s', '--speed-up', action='store_true', help='Speed up the sound.', default=False)
parser.add_argument('-d', '--speed-down', action='store_true', help='Speed down the sound.', default=False)
parser.add_argument('-e', '--export', action='store_true', help='Export the sound.', default=False)

args = parser.parse_args()

config = tts_server_config.TTSServerConfig()

if args.run:
    cmd_impl.run(config)

elif args.play:
    cmd_impl.play(config)