from pyOTR import pyOTR
from Src.videoTools import VideoTool, Cut
import config

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        filename = sys.argv[1]

    pyOTR.DOWNLOADDIR = config.DOWNLOADDIR
    pyOTR.DECODIR = config.DECODIR
    Cut.frameOffset = config.frameOffset
    Cut.CUTDIR = config.CUTDIR
    #VideoTool.BinDirectory = "Bin/Mac/"

    # Only cut single already decodeotrd file
    otr = pyOTR(useFile=True, fileName=filename)
    otr.cut()