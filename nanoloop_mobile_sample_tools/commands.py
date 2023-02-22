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
import os
import wave


logger = logging.getLogger(__name__)


def process(
        audio_inputs: list,
        sample_rate: float = 44100.0,
        speed_multiplier: float = 1.0,
        concatenate: bool = False,
        mono: str = 'left',
        compress: str = None,
        normalize: bool = False,
        reverse: bool = False) -> list:
    """Process the audio files.

    :param list audio_inputs: list of audio files.
    :param bool concatenate: concatenate the audio files before processing. (default; False)
    :param str mono: make audio mono. 'left' or 'right' or None i.e. leave it alone (default; None)
    :param int speed_multiplier: speed up the sample by a factor. (default; 1.0)
    :param str compress: compress the audio. 'soft' or 'hard' or None i.e. leave it alone (default; None)
    :param bool normalize: normalize the audio to 0 db. (default; False)
    :param bool reverse: reverse the audio. (default; False)
    :return list: array of processed audio files.
    """
    logger.info("Processing {} audio inputs.".format(len(audio_inputs)))
    logger.debug(
        (
            "process called with the following args; "
            "audio_inputs={audio_inputs}, concatenate={concatenate}, mono={mono}, "
            "compress={compress}, speed_multiplier={speed_multiplier}, "
            "normalize={normalize}, reverse={reverse}, sample_rate={sample_rate}"
        ).format(
            audio_inputs=audio_inputs,
            sample_rate=sample_rate,
            speed_multiplier=speed_multiplier,
            concatenate=concatenate,
            mono=mono,
            compress=compress,
            normalize=normalize,
            reverse=reverse
        )
    )
    audio_arrays = []
    for audio_input in audio_inputs:
        with pedalboard.io.AudioFile(audio_input, 'r').resampled_to(sample_rate/speed_multiplier) as f:
            audio_arrays.append(f.read(f.frames))

    if mono is not None:
        audio_arrays = [mono_audio(audios_array, mono) for audios_array in audio_arrays]

    if concatenate:
        logger.debug("Concatenating {} audio arrays.".format(len(audio_arrays)))
        audio_arrays = [concatenate_audio(audio_arrays)]

    if compress is not None:
        audio_arrays = [compress_audio(audio_array, compress, sample_rate) for audio_array in audio_arrays]
        
    if normalize:
        audio_arrays = [peak_normalize_audio(audios_array) for audios_array in audio_arrays]

    if reverse:
        audio_arrays = [reverse_audio(audio_array) for audio_array in audio_arrays]

    logger.info("Completed processing, outputting {} audio arrays.".format(len(audio_arrays)))
    return audio_arrays


def save(
        processed_audio_array: numpy.ndarray,
        sample_rate: float = 44100.0,
        bit_rate: int = 16,
        audio_output: str = "output.wav") -> str:
    """Save the processed audio files.

    :param list processed_audio: list of processed audio arrays.
    :param float sample_rate: sample rate of output files.
    :param int bit_rate: bit rate of output files.
    :param str audio_output: filename to output to. If multiple files present use a prefix.
    :return str: audio output file path
    """
    logger.info("Saving processed audio array to {}.".format(audio_output))
    logger.debug(
        (
            "save the processed audio with the following args; "
            "sample_rate={sample_rate}, bit_rate={bit_rate}, "
            "audio_output={audio_output}"
        ).format(
            sample_rate=sample_rate,
            bit_rate=bit_rate,
            audio_output=audio_output
        )
    )
    data = None
    sampwidth = None
    if bit_rate == 8:
        # 8-bit
        sampwidth = 1
        multiplier = 127
        data = (
            (processed_audio_array * multiplier) + multiplier
        ).astype(numpy.uint8)
    else: # bit_rate == 16:
        # 16 bit
        sampwidth = 2
        multiplier = 32767
        data = (
            processed_audio_array * multiplier
        ).astype(numpy.int16)
    
    # Let the operation fail if bit-rate is not valid, i.e. data is None
    with wave.open(audio_output, 'w') as f:
        f.setnchannels(processed_audio_array.shape[0])
        f.setsampwidth(sampwidth) # 1=8-bit unsigned, 2=16-bit signed 
        f.setframerate(sample_rate)
        f.writeframes(data)

    logger.info("Completed saving audio files.")

    return os.path.abspath(audio_output)


def mono_audio(audio_array: numpy.ndarray, channel_name: str) -> numpy.ndarray:
    """Make the audio mono.

    :return numpy.ndarray:
    """
    # Left is 0? shrug
    channel = audio_array[0]
    if channel_name == 'right':
        channel = audio_array[1]
    return numpy.array([channel])


def peak_normalize_audio(audio_array: numpy.ndarray) -> numpy.ndarray:
    """Perform peak normalization on audio array.

    :return numpy.ndarray:
    """
    maximum = numpy.max(audio_array)
    delta = 1.0 - maximum
    factor = 1.0 + (delta/maximum)
    return audio_array * factor


def concatenate_audio(audio_arrays: numpy.ndarray) -> numpy.ndarray:
    """Concatenate audio arrays.

    :return numpy.ndarray:
    """
    # get max channels 1 or 2
    max_channels = max([audio_array.shape[0] for audio_array in audio_arrays])

    for index in range(len(audio_arrays)):
        # If max channels is more than this audio array
        # duplicate its channels i.e. mono -> stereo
        if audio_arrays[index].shape[0] < max_channels:
            audio_arrays[index] = numpy.concatenate([audio_arrays[index], audio_arrays[index]])
    
    return numpy.concatenate(audio_arrays, axis = 1)


def compress_audio(audio_array: numpy.ndarray, compress: str, sample_rate: float) -> numpy.ndarray:
    """Compress the audio using a pedalboard.

    :param numpy.ndarray audio_array:
    :param str compress: compression type 'hard' or 'soft'
    :return numpy.ndarray:
    """
    board = pedalboard.Pedalboard()
    
    gain = pedalboard.Gain(gain_db=2)
    compressor = pedalboard.Compressor(threshold_db=-10, ratio=10)

    if compress == 'hard':
        gain = pedalboard.Gain(gain_db=10)
        compressor = pedalboard.Compressor(threshold_db=-20, ratio=20)
    
    board.append(gain)
    board.append(compressor)

    effected = board(audio_array, sample_rate)
    return effected


def reverse_audio(audio_array: numpy.ndarray) -> numpy.ndarray:
    """Reverse the audio array.

    :return numpy.ndarray:
    """
    return numpy.flip(audio_array)