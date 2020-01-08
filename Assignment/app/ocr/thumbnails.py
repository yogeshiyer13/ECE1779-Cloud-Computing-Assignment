from wand.image import Image

def thumbnails(path, thumbnails_path):
    with Image(filename=path) as img:
        with img.clone() as thumb:
            size = thumb.width if thumb.width < thumb.height else thumb.height
            thumb.crop(width=size, height=size, gravity='center')
            thumb.resize(256,256)
            thumb.save(filename=thumbnails_path)
    