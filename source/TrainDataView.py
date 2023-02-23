import os

from FilterView import FilterView
from BoxedImageView import BoxedImageView
from CroppedImageView import CroppedImageView

class TrainDataView():
    def __init__(self, main_window) -> None:
        self.boxedImageView = BoxedImageView(main_window.boxedImageLabel)
        self.croppedImageView = CroppedImageView(main_window.croppedImageLabel, main_window.imageInferenceLabel)
        self.filterView = FilterView(main_window.filterGridLayout)

    def setNewImage(self, boxedPath, croppedPath, gt, viewPathBool, currentImageIndex):
        croppedIdx = int(os.path.basename(croppedPath).split('_')[1])
        croppedImg = self.boxedImageView.setNewImage(boxedPath, croppedIdx)
        self.croppedImageView.setNewImage(croppedImg, gt, viewPathBool)
        self.filterView.setImageIndex(currentImageIndex)
    
    def getCroppedImageIndex(self):
        return self.filterView.getImageIndex()
    
    def fileterLogList(self, logList):
        return self.filterView.filter(logList)

    