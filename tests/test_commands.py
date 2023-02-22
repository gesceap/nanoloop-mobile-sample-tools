from nanoloop_mobile_sample_tools import commands
import os
import numpy
import math


def test_process(mock_audio_input_files):
    """Test calling process with audio files

    :return None:
    :raises AssertionError:
    """
    assert commands.process(mock_audio_input_files)


def test_process_concatenate(mock_audio_input_files):
    """Test calling process concatenating audio file

    :return None:
    :raises AssertionError:
    """
    assert len(mock_audio_input_files) > 1
    processed_audio = commands.process(mock_audio_input_files, concatenate=True)
    assert len(processed_audio) == 1 and len(mock_audio_input_files) > 1


def test_save_file(mock_audio_array):
    """Test calling wave with an audio array.

    :return None:
    :raises AssertionError:
    """
    abspath = commands.save(mock_audio_array, audio_output = "mock.wav")
    assert os.path.isfile("mock.wav") and os.path.isfile(abspath)
    os.remove("mock.wav")


def test_save_file_16_bit(mock_audio_array):
    """Test calling wave with an audio array to 16 bit

    :return None:
    :raises AssertionError:
    """
    filename = "mock16.wav"
    abspath = commands.save(mock_audio_array, audio_output = filename, bit_rate=16, sample_rate=22050)
    assert os.path.isfile(filename) and os.path.isfile(abspath)
    os.remove(filename)


def test_save_file_8_bit(mock_audio_array):
    """Test calling wave with an audio array to 8 bit

    :return None:
    :raises AssertionError:
    """
    filename = "mock8.wav"
    abspath = commands.save(mock_audio_array, audio_output = filename, bit_rate=8, sample_rate=8000)
    assert os.path.isfile(filename) and os.path.isfile(abspath)
    os.remove(filename)


def test_make_mono_left(mock_audio_array):
    """Test make mono left.

    :return None:
    :raises AssertionError:
    """
    a = commands.mono_audio(mock_audio_array, 'left')
    assert a.any() and a.shape[0] == 1


def test_make_mono_right(mock_audio_array):
    """Test make mono right.

    :return None:
    :raises AssertionError:
    """
    a = commands.mono_audio(mock_audio_array, 'right')
    assert a.any() and a.shape[0] == 1


def test_peak_normalize(mock_audio_array):
    """Test peak normalization of audio.

    :return None:
    :raises AssertionError:
    """
    assert not math.isclose(numpy.max(mock_audio_array), 1.0)
    normalized_audio = commands.peak_normalize_audio(mock_audio_array)
    assert math.isclose(numpy.max(normalized_audio), 1.0, abs_tol = 0.000001)


def test_reverse_audio():
    """Test compressing audio.

    :return None:
    :raises AssertionError:
    """
    audio_array = numpy.array([1,2,3,4])
    expected_audio_array = numpy.array([4,3,2,1])
    reversed_audio_array = commands.reverse_audio(audio_array)
    assert numpy.array_equiv(reversed_audio_array, expected_audio_array)


def test_compress_audio(mock_audio_array):
    """Test compressing audio.

    :return None:
    :raises AssertionError:
    """
    assert commands.compress_audio(mock_audio_array, 'soft', 44100.0).any()