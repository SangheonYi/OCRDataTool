import cv2
import json
from pathlib import Path, WindowsPath
from PyQt6.QtWidgets import QLabel, QSizePolicy, QWidget, QScrollArea
import numpy as np
from PyQt6.QtGui import QPixmap, QImage, QPalette
from debug_mode import debug_mode

detLabelFileName = 'inspect_inf_result\det_label.log'

class BoxedImageView(QWidget):
    def __init__(self, imageLabel: QLabel, scrollArea: QScrollArea):
        super().__init__()

        self.detLabel = dict()
        self.parseDetLabel()

        self.scaleFactor = 1

        self.imageLabel = imageLabel
        self.imageLabel.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.imageLabel.setScaledContents(True)

        self.scrollArea = scrollArea

        # TODO add scroll
        print('set widget')
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setBackgroundRole(QPalette.ColorRole.Dark)
        self.scrollArea.setWidgetResizable(True)
        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), self.scaleFactor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), self.scaleFactor)

    def parseDetLabel(self):
        with open(detLabelFileName, 'r', encoding='utf-8') as detLabelFile:
            for line in detLabelFile:
                key, val_list = line.replace('converted', 'boxed').strip('\n').split('\t')
                key = str(WindowsPath(key))
                val_list = json.loads(val_list)
                boxes, txts = [], []
                for bno in range(0, len(val_list)):
                    box = val_list[bno]['points']
                    txt = val_list[bno]['transcription']
                    boxes.append(box)
                    txts.append(txt)
                self.detLabel[key] = {
                    'boxes':boxes, 
                    'txts':txts
                }
            if debug_mode:
                print('detlabel size: ', len(self.detLabel.keys()))

    def setNewImage(self, boxedPath, croppedIdx):
        self.scaleFactor = 1
        stream = open(boxedPath, "rb")
        bytes = bytearray(stream.read())
        numpyarray = np.asarray(bytes, dtype=np.uint8)
        bgrImage = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)

        # draw annotation
        points = np.array(self.detLabel[boxedPath]['boxes'][croppedIdx])
        lined_img = bgrImage.copy()
        lined_img = cv2.polylines(lined_img, [points], True, (0, 255, 0), 5)

        newImage = self.convert_cv_qt(lined_img)
        self.imageLabel.setPixmap(newImage)
        self.imageLabel.adjustSize()
        
        # crop image to return
        croppedImg = self.convert_cv_qt(bgrImage[points[0][1]:points[2][1], points[0][0]:points[1][0]])
        return croppedImg

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        return QPixmap.fromImage(convert_to_Qt_format)

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))