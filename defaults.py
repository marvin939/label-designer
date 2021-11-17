import os
class properties:
    imageDirectory = os.environ["dataserv"] + "\\misc\\images"  # dataserv is somewhere in the Y: drive.
    defaultImage = os.path.join(imageDirectory, "image.png")