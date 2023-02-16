import pytest
import os
import numpy
import pedalboard


ABSPATH = os.path.realpath("./tests/audio_files")


@pytest.fixture(scope="session")
def mock_audio_input_files():
    """Fixture for audio input files.

    list of filename paths.

    :return list:
    """
    return list(
        map(
            lambda fn: "{}/{}".format(ABSPATH, fn), 
            [
                "audio_input_1.wav",
                "audio_input_2.wav",
                "think.wav"
            ]
        )
    )


@pytest.fixture(scope="session")
def mock_audio_arrays(mock_audio_input_files):
    """Fixture for audio input files.

    list of filename paths.

    :return list:
    """
    audio_arrays = []
    for path in mock_audio_input_files:
        with pedalboard.io.AudioFile(path, 'r') as f:
            audio_arrays.append(f.read(f.frames))
    return audio_arrays


@pytest.fixture(scope="session")
def mock_audio_array(mock_audio_arrays):
    """Fixture for mock audio input array.

    :return numpy.ndarray:
    """
    return mock_audio_arrays[0]