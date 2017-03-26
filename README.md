# Huge Google Maps

Program to make huge, detailed screenshots of Google Maps.

Developed as a one-off script to make a 4-foot square wall map of
Philadelphia (25000 x 25000 pixels). Will require minor tweaking to
work on other machines or zoom levels.

Please be respectful of the [Google Maps Terms of Service][TOS],
remember to attribute properly, and do not use this program for
commercial purposes.

## Requirements / Dependencies

* Python 3.5
* Selenium 3.0.2  (Browser automation to display the Google maps)
* PyScreenshot 0.4.2  (To capture an area of each map)
* Nose 1.3.7  (To run and time tests / map creation)
* [Mozilla Gecko driver][GECKO] -- `mv geckodriver /usr/bin`
* Set computer screen to not turn off / sleep while program is running

On Ubuntu:
```
sudo python3 -m pip install selenium
sudo python3 -m pip install pyscreenshot
sudo python3 -m pip install nose
sudo apt-get install python3-tk
```

## Using the program

Import the `hugegmaps` script and call the `create_map` function.
You can reference the `tests.py` file for examples of the below content.

If an `outfile` parameter is passed to the function,
then the finished map will be saved to that location.
Otherwise, the file will be saved to the current working
directory with the filename `testimg-<timestamp>.png`.

Start by going to [Google Maps][MAPS], and find the top-left
coordinate you want to use for the final map. At the moment,
the program always runs at a zoom level of `18z`. I anchored
my test runs around the Philly Art Museum, so my coordinates
were [`(39.9644273, -75.1801129)`][PHILLY-ANCHOR].

Run a quick test of the program to create an image from a single screenshot.

```
from hugegmaps import create_map
create_map(
    lat_start=39.9644273,
    long_start=-75.1801129,
    number_rows=1,
    number_cols=1,
    outfile='test_calibration.png',
)
```

Open the program in an image viewer of your choice. Using the Ubuntu
default viewer:

```
eog huge_gmap_calibration.png
```

Based on the results of the program run with `0` for all `offset_*` values,
make an estimate for what ratio should be trimmed from each side so that only
the pure map area is seen. On my laptop, a single display with left-side
taskbar, these values were:

```
offset_left=0,  # My value: 0.05
offset_top=0,  # My value: 0.17
offset_right=0,  # My value: 0.03
offset_bottom=0,  # My value: 0.09
```

Once you adjust the offsets to eliminate unwanted elements, delete the test
screenshot, and run the program again. This will take a few runs with
trial-and-error to get right.

When you're happy with the single screenshot and have the offsets configured,
run the program on a small 3x3 grid to ensure that the images get stitched
together seamlessly. You'll want to run the program at a scale of about
`0.2`, or else the resulting image can be too large to open in normal
image viewers.

At this point, you also want to increase the `sleep_time` to make sure that
all asynchronous image loading functions complete before you take your
screenshot. If this is set too low, some screenshots may appear with less
content and lower resolution than others in the final image.

```
create_map(
    lat_start=39.9644273,
    long_start=-75.1801129,
    number_rows=3,
    number_cols=3,
    scale=0.2,
    sleep_time=3,
    offset_left=0.05,
    offset_top=0.17,
    offset_right=0.03,
    offset_bottom=0.09,
    outfile='huge_gmap_small_area.png',
)
```

Look at the resulting image to ensure the offsets are correct, and make sure
the seams of the screenshots (at 1/3 and 2/3 of the final image's height
and width) line up. If these do not line up perfectly, you might need to make
small adjustments to the 'magic numbers' in the `calc_latitude_shift` and
`calc_longitude_shift` functions.

Once you are happy with the test of a 3x3 grid of images, estimate the total
number of rows and columns that your desired area will require, and run the
program at low resolution and no sleep time to confirm those numbers.

After you confirm your offsets and rows/columns at low resolution, run
the program with a `scale=1` and `sleep_time=3` (or more) to create your
print-ready huge Google Map.

## Contributing

If you have any suggestions for improvement, please update this code
in the simplest way that could possibly work, and submit a pull request.
Or, just open an Issue on GitHub.

## Wishlist / TODO

* Remove `pyscreenshot` dependency by hand-rolling a `crop_image_by_offsets`
  function using PIL. Selenium can take full-screen screenshots already.
* Allow for adjustable zoom levels. Will require adjusting the formula
  and magic numbers for the lat and long shift calculations.
* Allow the program to work with Google Earth, not just Google Maps.


[GECKO]: https://github.com/mozilla/geckodriver/releases
[MAPS]: https://www.google.com/maps
[PHILLY-ANCHOR]: https://www.google.com/maps/@39.9644273,-75.1801129,18z
[TOS]: https://www.google.com/help/terms_maps.html
