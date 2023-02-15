from nanoloop_mobile_sample_tools import commands
import os


def test_process(audio_input_files):
    """Test calling process with audio files

    :return None:
    :raises AssertionError:
    """
    assert commands.process(audio_input_files)


def test_process_concatenate(audio_input_files):
    """Test calling process concatenating audio file

    :return None:
    :raises AssertionError:
    """
    processed_audio = commands.process(audio_input_files, concatenate=True)
    assert len(processed_audio) == 1 and len(audio_input_files) > 1


def test_save_single_file(mock_audio_input):
    """Test calling process with a single audio file

    :return None:
    :raises AssertionError:
    """
    processed_audio = [mock_audio_input]
    commands.save(processed_audio, audio_output = "mock.wav")
    assert os.path.isfile("mock.wav")
    os.remove("mock.wav")


def test_save_multiple_files(mock_audio_input):
    """Test calling process with multiple audio files

    :return None:
    :raises AssertionError:
    """
    processed_audio = [mock_audio_input, mock_audio_input]
    commands.save(processed_audio, audio_output = "mock.wav")
    assert os.path.isfile("mock_1.wav") and  os.path.isfile("mock_2.wav")
    os.remove("mock_1.wav")
    os.remove("mock_2.wav")


def test_make_mono_left(mock_audio_input):
    """Test make mono left.

    :return None:
    :raises AssertionError:
    """
    a = commands.make_mono(mock_audio_input, 'left')
    assert a.any() and a.shape[0] == 1


def test_make_mono_right(mock_audio_input):
    """Test make mono right.

    :return None:
    :raises AssertionError:
    """
    a = commands.make_mono(mock_audio_input, 'right')
    assert a.any() and a.shape[0] == 1