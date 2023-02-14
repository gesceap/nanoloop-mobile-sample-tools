"""Top level commands for nanoloop mobile sample tools.

Should only support basic actions in fixed order:

1. Concatenate files (if multiple)
2. Mono (None L R)
3. Resample (44k 22k 11k) [output sample rate]
4. Speed up (1x 2x 4x 8x)
5. Compress (None, Soft, Hard)
6. Normalize (T/F)
7. Reverse (T/F)
"""

import pedalboard
import logging
import numpy


logger = logging.getLogger(__name__)


def process(
        audio_inputs: list,
        concatenate: bool = False,
        mono: str = 'left',
        sample_rate: float = 44100.0,
        bit_rate: int = 16,
        speed_multiplier: float = 1.0,
        compress: str = None,
        normalize: bool = False,
        reverse: bool = False) -> list:
    """Process the audio files.

    :param list audio_inputs: list of audio files.
    :param bool concatenate: concatenate the audio files before processing. (default; False)
    :param str mono: make audio mono. 'left' or 'right' or None i.e. leave it alone (default; None)
    :param float sample_rate: sample rate to convert (default; 44100)
    :param int speed_multiplier: speed up the sample by a factor. (default; 1.0)
    :param str compress: compress the audio. 'soft' or 'hard' or None i.e. leave it alone (default; None)
    :param bool normalize: normalize the audio to 0 db. (default; False)
    :param bool reverse: reverse the audio. (default; False)
    :return list: array of processed audio files.
    """
    logger.debug(
        (
            "process called with the following args; "
            "audio_inputs={audio_inputs}, concatenate={concatenate}, mono={mono}, "
            "sample_rate={sample_rate}, bit_rate={bit_rate}, "
            "speed_multiplier={speed_multiplier}, compress={compress}, "
            "normalize={normalize}, reverse={reverse}"
        ).format(
            audio_inputs=audio_inputs,
            concatenate=concatenate,
            mono=mono,
            sample_rate=sample_rate,
            bit_rate=bit_rate,
            speed_multiplier=speed_multiplier,
            compress=compress,
            normalize=normalize,
            reverse=reverse
        )
    )
    for audio_input in audio_inputs:
        audios = []
        with pedalboard.io.AudioFile(audio_input, 'r') as f:
            audios.append(f.read(f.frames))

    if mono is not None:
        audios = [make_mono(audio, mono) for audio in audios]

    if concatenate:
        audios = [numpy.concatenate(audios)]

    return audios


def make_mono(input_audio: numpy.ndarray, channel_name: str) -> numpy.ndarray:
    """Make the audio mono.

    :return numpy.ndarray:
    """
    # Left is 0? shrug
    channel = input_audio[0]
    if channel_name == 'right':
        channel = input_audio[1]
    return numpy.array([channel])