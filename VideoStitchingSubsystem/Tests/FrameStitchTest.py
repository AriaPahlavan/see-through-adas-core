import numpy as np

from VideoStitchingSubsystem.MyTests.TestBlending import TestBlending
from VideoStitchingSubsystem.Utils import *
from VideoStitchingSubsystem.VideoStitchingAPIs.FrameStitch import PatchImages

BACK_PATH = "./back.jpg"
FORE_PATH = "./front.jpg"
CHOOSER_WINDOW = "Choose Coordinates"

bgImg = cv2.imread(BACK_PATH, cv2.IMREAD_COLOR)
fgImg = cv2.imread(FORE_PATH, cv2.IMREAD_COLOR)


def showFinal(bg, fg):
    blendedBg = TestBlending(bg, numlayres=2, imgName="bg")
    blendedFg = TestBlending(fg, numlayres=2, imgName="fg")

    blendedFinalImg = blendedBg.stitchedWith(blendedFg).reconstructed()
    cv2.imshow("Blended", blendedFinalImg)
    cv2.imwrite("./blended.jpg", blendedFinalImg)

    finalImg = PatchImages(bg, fg)
    cv2.imshow("stitched_no_blend", finalImg)
    cv2.imwrite("./stitched.jpg", finalImg)

    CloseAllWhenPressed()


def transformPerspective():
    fgHeight, fgWidth, _ = fgImg.shape
    fgImageCoords = np.array([(0, 0),
                              (0, fgHeight),
                              (fgWidth, fgHeight),
                              (fgWidth, 0)])
    y0 = 285
    y1 = 400
    x0 = 447
    x1 = 600
    stitchingCoords = np.array([(x0, y0),
                                (x0, y1),
                                (x1, y1),
                                (x1, y0)])
    homography, _ = cv2.findHomography(fgImageCoords, stitchingCoords, 0)

    bgHeight, bgWidth, _ = bgImg.shape
    projectedIm = cv2.warpPerspective(src=fgImg, M=homography, dsize=(bgWidth, bgHeight))

    showFinal(bgImg, projectedIm)


if __name__ == "__main__":
    transformPerspective()
