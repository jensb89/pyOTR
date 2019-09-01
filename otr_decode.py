from pyOTR import pyOTR
from Src.decoder import OTRDecoder
import config

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        filename = sys.argv[1]

    pyOTR.DOWNLOADDIR = config.DOWNLOADDIR
    pyOTR.DECODIR = config.DECODIR
    OTRDecoder.USERNAME = config.OTRMAIL
    OTRDecoder.PASSWORD = config.OTRPW

    # Decode single file
    otr = pyOTR(useFile=True, fileName=filename)
    otr.decode()