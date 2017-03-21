"""Take huge detailed screenshots of Google Maps."""

from datetime import datetime
import time
import tkinter

from PIL import Image
import pyscreenshot
from selenium import webdriver


def create_map(lat_start: float, long_start: float,
               number_rows: int, number_cols: int,
               scale: float=1, sleep_time: float=3,
               offset_left: float=0.05, offset_top: float=0.17,
               offset_right: float=0.03, offset_bottom: float=0.09):
    """Create a big Google Map image from a grid of screenshots.

    ARGS:
        lat_start: Top-left coodinate to start taking screenshots.
        long_start: Top-left coodinate to start taking screenshots.
        number_rows: Number of screenshots to take for map.
        number_cols: Number of screenshots to take for map.
        scale: Percent to scale each image to reduce final resolution
            and filesize. Should be a float value between 0 and 1.
            Recommend to leave at 1 for production, and between 0.05
            and 0.2 for testing.
        sleep_time: Seconds to sleep between screenshots.
            Needed because Gmaps has some AJAX queries that will make
            the image better a few seconds after confirming page load.
            Recommend 0 for testing, and 3-5 seconds for production.
        offset_*: Percent of each side to crop from screenshots.
            Each should be a float value between 0 and 1. Offsets should
            account for all unwanted screen elements, including:
            taskbars, windows, multiple displays, and Gmaps UI (minimap,
            search box, compass/zoom buttons). Defaults are set for an
            Ubuntu laptop with left-side taskbar, and will need to be
            tuned to the specific machine and setup where it will be run.
    """
    driver = webdriver.Firefox()
    driver.maximize_window()
    # 2D grid of Images to be stitched together
    images = [[None for _ in range(number_cols)]
              for _ in range(number_rows)]

    # Calculate amount to shift lat/long each screenshot
    screen_width, screen_height = get_screen_resolution()
    lat_shift = calc_latitude_shift(screen_height,
                                    (offset_top + offset_bottom))
    long_shift = calc_longitude_shift(screen_width,
                                      (offset_left + offset_right))

    for row in range(number_rows):
        for col in range(number_cols):
            latitude = lat_start + (lat_shift * row)
            longitude = long_start + (long_shift * col)
            # Show the map using the Firefox driver
            url = (
                'https://www.google.com/maps/@{lat},{long},18z'
                ).format(lat=latitude, long=longitude)
            driver.get(url)
            # Let the map load all assets before taking a screenshot
            time.sleep(sleep_time)
            images[row][col] = screenshot(screen_width, screen_height,
                                          offset_left, offset_top,
                                          offset_right, offset_bottom)

    driver.close()
    driver.quit()

    # Scale up or down all the images, then combine and save them
    images = [[scale_image(img, scale) for img in row] for row in images]
    final = combine_images(images)
    timestamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
    final.save('testimg-{}.png'.format(timestamp))


def get_screen_resolution() -> tuple:
    """Return tuple of (width, height) of screen resolution in pixels."""
    root = tkinter.Tk()
    root.withdraw()
    return (root.winfo_screenwidth(), root.winfo_screenheight())


def calc_latitude_shift(screen_height: int, percent_hidden: float) -> float:
    """Return the amount to shift latitude per row of screenshots."""
    return -0.000002051 * screen_height * (1 - percent_hidden)


def calc_longitude_shift(screen_width: int, percent_hidden: float) -> float:
    """Return the amount to shift longitude per column of screenshots."""
    return 0.00000268 * screen_width * (1 - percent_hidden)


def screenshot(screen_width: int, screen_height: int,
               offset_left: float, offset_top: float,
               offset_right: float, offset_bottom: float) -> Image:
    """Return a screenshot of only the pure maps area."""
    x1 = offset_left * screen_width
    y1 = offset_top * screen_height
    x2 = (offset_right * -screen_width) + screen_width
    y2 = (offset_bottom * -screen_height) + screen_height
    image = pyscreenshot.grab(bbox=(x1, y1, x2, y2))
    return image


def scale_image(image: Image, scale: float) -> Image:
    """Scale an Image by a proportion, maintaining aspect ratio."""
    width = round(image.width * scale)
    height = round(image.height * scale)
    image.thumbnail((width, height))
    return image


def combine_images(images: list) -> Image:
    """Return combined image from a grid of identically-sized images.

    images is a 2d list of Image objects. The images should
    be already sorted/arranged when provided to this function.
    """
    imgwidth = images[0][0].width
    imgheight = images[0][0].height
    newsize = (imgwidth * len(images[0]), imgheight * len(images))
    newimage = Image.new('RGB', newsize)

    # Add all the images from the grid to the new, blank image
    for rowindex, row in enumerate(images):
        for colindex, image in enumerate(row):
            location = (colindex * imgwidth, rowindex * imgheight)
            newimage.paste(image, location)

    return newimage
