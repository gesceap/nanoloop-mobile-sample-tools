def test_version():
    """Test that the standard __version__ dunder is available.

    :return None:
    :raises AssertionError:
    """
    import nanoloop_mobile_sample_tools
    assert nanoloop_mobile_sample_tools.__version__