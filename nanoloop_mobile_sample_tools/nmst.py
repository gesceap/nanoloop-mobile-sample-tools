import argparse
import logging
from nanoloop_mobile_sample_tools import commands


def get_parser() -> argparse.Namespace:
    """Get the CLI parser.

    :return argparse.Namespace:
    """
    parser = argparse.ArgumentParser(
        description="Nanoloop Mobile Sample Tools CLI"
    )

    parser.add_argument(
        "--debug",
        dest="debug",
        nargs='?',
        const=logging.DEBUG,
        default=logging.INFO,
        help="Set logging level to DEBUG, default INFO.",
    )

    parser.add_argument(
        "audio_inputs",
        nargs='+',
        help="Audio files to process in order.",
    )
    parser.add_argument(
        "--concatenate",
        dest="concatenate",
        action="store_true",
        help="Concatenate the audio inputs to the output. Deafult 'False'.",
    )
    parser.add_argument(
        "--mono",
        dest="mono",
        nargs='?',
        const='left',
        type=str,
        default='left',
        choices=['left', 'right'],
        help="Make audio mono. Default 'left'. Options; 'left' and 'right'",
    )
    parser.add_argument(
        "--sample-rate",
        dest="sample_rate",
        nargs='?',
        const=44100.0,
        type=float,
        default=44100.0,
        help="Sample rate for audio. Default '44100.0'",
    )
    parser.add_argument(
        "--bit-rate",
        dest="bit_rate",
        nargs='?',
        const=16,
        type=int,
        default=16,
        choices=[8, 16],
        help="Bit rate for audio. Default '16'. Options; '8' or '16' bit.",
    )
    parser.add_argument(
        "--speed-multiplier",
        dest="speed_multiplier",
        nargs='?',
        const=1.0,
        type=float,
        default=1.0,
        help="Speed multiplier for audio. Default '1.0' i.e. no change",
    )
    parser.add_argument(
        "--compress",
        dest="compress",
        nargs='?',
        type=str,
        choices=['soft', 'hard'],
        help="Compress the audio signal. Default 'None'. Options; 'soft' and 'hard'",
    )
    parser.add_argument(
        "--normalize",
        dest="normalize",
        action="store_true",
        help="Normalize the audio output. Deafult 'False'.",
    )
    parser.add_argument(
        "--reverse",
        dest="reverse",
        action="store_true",
        help="Reverse the audio output. Deafult 'False'.",
    )
    parser.add_argument(
        "--audio-output",
        dest="audio_output",
        nargs='?',
        const="output.wav",
        type=str,
        default="output.wav",
        help="Audio output filename. Default 'output.wav'",
    )
    return parser


def main():
    """Run the main CLI."""
    parser = get_parser()
    args = parser.parse_args()
    
    logging.basicConfig(level=args.debug)

    commands.process(
        args.audio_inputs,
        concatenate=args.concatenate,
        mono=args.mono,
        sample_rate=args.sample_rate,
        bit_rate=args.bit_rate,
        compress=args.compress,
        normalize=args.normalize,
        reverse=args.reverse,
        audio_output=args.audio_output
    )