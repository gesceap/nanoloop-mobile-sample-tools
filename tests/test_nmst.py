import sys
import os
from nanoloop_mobile_sample_tools import nmst


def test_main(audio_input_files):
    """Test calling main in CLI.

    :return None:
    """
    mock_output_filename = "mock.wav"
    sys.argv = [
        "",
        *audio_input_files,
        "--concatenate",
        "--audio-output",
        mock_output_filename
    ]

    nmst.main()
    assert os.path.isfile(mock_output_filename)
    os.remove(mock_output_filename)
