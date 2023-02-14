from nanoloop_mobile_sample_tools import commands


def test_process(audio_input_files):
    """Test calling process with an audio file

    :return None:
    :raises AssertionError:
    """
    assert commands.process(audio_input_files)


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