import os
class properties:
    #imageDirectory = os.environ["dataserv"] + "\\misc\\images"  # dataserv is somewhere in the Y: drive.
    #defaultImage = os.path.join(imageDirectory, "image.png")
    imageDirectory = ""
    defaultImage = ""
    

if "dataserv" not in os.environ.keys():
    imageDirectory = r"..\dataserv_test\misc\images"  # dataserv is somewhere in the Y: drive.
else:
    imageDirectory = os.environ["dataserv"] + "\\misc\\images"  # for testing.

defaultImage = os.path.join(imageDirectory, "image.png")