import argparse
from ..utils.utils import get_os_api
from .cmd_impl import CMDImpl

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
parser.add_argument('--shutdown', action='store_true', help='Shutdown the server.', default=False)

def main():

    args = parser.parse_args()

    os_api = get_os_api()
    port = os_api.get_config().port

    if args.run:
        CMDImpl.run(os_api, port)

    elif args.play:
        CMDImpl.play_selected(os_api, port, args.lang)

    elif args.append_to_play:
        CMDImpl.append_selected(os_api, port, args.lang)

    elif args.speed_up:
        CMDImpl.speedup(os_api, port)

    elif args.speed_down:
        CMDImpl.speeddown(os_api, port)

    elif args.export:
        CMDImpl.export_selected(os_api, port, args.lang)

    elif args.play_pause:
        CMDImpl.toggle_pause(port)

    elif args.back:
        CMDImpl.back(port)

    elif args.shutdown:
        CMDImpl.shutdown(port)


if __name__ == "__main__":
    main()