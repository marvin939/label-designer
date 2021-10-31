import os
class properties:
    imageDirectory = os.environ["dataserv"] + "\\misc\\images"
    defaultImage = os.path.join(imageDirectory, "image.png")