"""Tests to make some huge Gmaps."""

from hugegmaps import create_map


def test_philly_art_museum():
    """Quick, small 2x3 map of the Philly Art museum area.
    Takes about 30 seconds to run.
    """
    create_map(
        lat_start=39.9644273,
        long_start=-75.1801129,
        number_rows=2,
        number_cols=3,
        scale=0.2,
        sleep_time=0,
    )


def test_philly_full_size():
    """Full-size map of Philly.
    About the biggest size I can make and still open in ImageViewer (~7mb).
    Takes about 12 minutes to run.
    """
    create_map(
        lat_start=39.9746524,
        long_start=-75.2020434,
        number_rows=16,
        number_cols=8,
        scale=0.1,
        sleep_time=0,
    )


def test_philly_high_res():
    """High-res map of Philly.
    University City, Templetown, South Philly, Delaware River.
    Takes about 20 minutes to run.
    """
    create_map(
        lat_start=39.9746524,
        long_start=-75.2020434,
        number_rows=16,
        number_cols=8,
        scale=1,
        sleep_time=5,
    )
