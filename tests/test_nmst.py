import sys
import os
from nanoloop_mobile_sample_tools import nmst


def test_main(mock_audio_input_files):
    """Test calling main in CLI.

    :return None:
    """
    mock_output_filename = "mock.wav"
    sys.argv = [
        "",
        *mock_audio_input_files,
        "--concatenate",
        "--compress",
        "hard",
        "--reverse",
        "--mono",
        "--debug",
        "--sample-rate",
        "22050.0",
        "--bit-rate",
        "8",
        "--normalize",
        "--speed-multiplier",
        "2.0",
        "--audio-output",
        mock_output_filename
    ]

    nmst.main()
    assert os.path.isfile(mock_output_filename)
    os.remove(mock_output_filename)
