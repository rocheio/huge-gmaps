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

## Testing / Making a Map

```
nosetests  # don't do this
nosetests tests:test_philly_art_museum  # just run one at a time
```

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
[TOS]: https://www.google.com/help/terms_maps.html
