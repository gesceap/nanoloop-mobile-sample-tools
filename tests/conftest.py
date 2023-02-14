import pytest
import os
import numpy


ABSPATH = os.path.realpath("./tests/audio_files")


@pytest.fixture(scope="session")
def audio_input_files():
    """Fixture for audio input files.

    list of filename paths.

    :return list:
    """
    return list(
        map(
            lambda fn: "{}/{}".format(ABSPATH, fn), 
            [
                "audio_input_1.wav",
                "audio_input_2.wav"
            ]
        )
    )


@pytest.fixture(scope="session")
def mock_audio_input():
    """Fixture for mock audio input array.

    :return numpy.ndarray:
    """
    return numpy.random.rand(2, 100)