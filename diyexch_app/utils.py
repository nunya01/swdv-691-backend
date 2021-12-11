from django.core.files import File
from pathlib import Path
from PIL import Image
from io import BytesIO

image_types = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "gif": "GIF",
    "tif": "TIFF",
    "tiff": "TIFF",
}


def image_resize(image, width, height):
    """ Resizes images with Pillow if they are too large
        Args:
            image <obj>: the eimage to be resized
            width <int>: pixels width
            height <int>: pixels height
    """

    img = Image.open(image)
    # Save the exif info
    exif = img.info.get('exif')
    # check if either the width or height is greater than the max
    if img.width > width or img.height > height:
        output_size = (width, height)
        # Create a new resized version of the image with Pillow that keeps aspect ration
        img.thumbnail(output_size)
        img_filename = Path(image.file.name).name
        # Spilt the filename on “.” to get the file extension only
        img_suffix = Path(image.file.name).name.split(".")[-1]
        # Use the file extension to determine the file type from the image_types dictionary
        img_format = image_types[img_suffix]
        buffer = BytesIO()
        # Re-add exif if needed
        if exif is not None:
            img.save(buffer, format=img_format, exif=exif)
        else:
            img.save(buffer, format=img_format)
        # Wrap the buffer in File object
        file_object = File(buffer)
        image.save(img_filename, file_object)