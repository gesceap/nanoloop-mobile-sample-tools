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


logger = logging.getLogger(__name__)


def process(
        audio_inputs: list,
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
            "compress={compress}, "
            "normalize={normalize}, reverse={reverse}"
        ).format(
            audio_inputs=audio_inputs,
            concatenate=concatenate,
            mono=mono,
            compress=compress,
            normalize=normalize,
            reverse=reverse
        )
    )
    audios_arrays = []
    for audio_input in audio_inputs:
        with pedalboard.io.AudioFile(audio_input, 'r') as f:
            audios_arrays.append(f.read(f.frames))

    if mono is not None:
        audios_arrays = [mono_audio(audios_array, mono) for audios_array in audios_arrays]

    if concatenate:
        logger.debug("Concatenating {} audio arrays.".format(len(audios_arrays)))
        audios_arrays = [concatenate_audio(audios_arrays)]

    if compress is not None:
        audios_arrays = [compress_audio(audios_array, compress) for audios_array in audios_arrays]

    if normalize:
        audios_arrays = [peak_normalize_audio(audios_array) for audios_array in audios_arrays]

    if reverse:
        audios_arrays = [numpy.flip(audioaudios_array) for audios_array in audios_arrays]

    logger.info("Completed processing, outputting {} audio arrays.".format(len(audios_arrays)))
    return audios_arrays


def save(
        processed_audio: list,
        sample_rate: float = 44100.0,
        bit_rate: int = 16,
        speed_multiplier: float = 1.0,
        audio_output: str = "output.wav") -> None:
    """Save the processed audio files.

    :param list processed_audio: list of processed audio arrays.
    :param float sample_rate: sample rate of output files.
    :param int bit_rate: bit rate of output files.
    :param str audio_output: filename to output to. If multiple files present use a prefix.
    :return None:
    """
    logger.info("Saving {} processed audio arrays.".format(len(processed_audio)))
    logger.debug(
        (
            "save the processed audio with the following args; "
            "sample_rate={sample_rate}, bit_rate={bit_rate}, "
            "audio_output={audio_output}, speed_multiplier={speed_multiplier}"
        ).format(
            sample_rate=sample_rate,
            bit_rate=bit_rate,
            audio_output=audio_output,
            speed_multiplier=speed_multiplier
        )
    )
    folder, filename = os.path.split(audio_output)
    prefix, extension = os.path.splitext(filename)
    
    for index, processed in enumerate(processed_audio, 1):

        suffix = "_{}{extension}".format(index, extension=extension)
        if len(processed_audio) == 1:
            suffix = "{extension}".format(index, extension=extension)
        
        output_filename = prefix + suffix

        logger.debug("Writing audio to output filename; {}".format(output_filename))
        
        with pedalboard.io.AudioFile(
            output_filename, 
            "w", 
            samplerate=sample_rate*speed_multiplier,
            bit_depth=bit_rate,
            num_channels=processed.shape[0]
        ) as f:
            f.write(processed)
    
    logger.info("Completed saving audio files.")


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


def compress_audio(audio_array: numpy.ndarray, compress: str) -> numpy.ndarray:
    """Compress the audio using a pedalboard.

    :param numpy.ndarray audio_array:
    :param str compress: compression type 'hard' or 'soft'
    :return numpy.ndarray:
    """
    gain = pedalboard.Gain(gain_db=2)
    compressor = pedalboard.Compressor(threshold_db=-15, ratio=10)
    if compress == 'hard':
        gain = pedalboard.Gain(gain_db=10)
        compressor = pedalboard.Compressor(threshold_db=-30, ratio=20)
    board = pedalboard.Pedalboard([gain, compressor])
    return board(audio_array)