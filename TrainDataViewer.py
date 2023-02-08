import sys
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtWidgets import QLabel, QSizePolicy
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import numpy as np
import os
import cv2
import json
from pathlib import PureWindowsPath

fileName = "test.jpg"
detLabelFileName = 'det_train.txt'

class BoxedImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.imageLabel = QLabel()
        # self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.imageLabel.setScaledContents(True)
        self.detLabel = dict()
        self.parseDetLabel()
        # TODO add scroll
        # self.scrollArea = QScrollArea()
        # self.scrollArea.setBackgroundRole(QPalette.Dark)
        # self.scrollArea.setWidget(self.imageLabel)
        # self.scrollArea.setVisible(False)

        self.boxedImageLayout = QVBoxLayout()
        self.boxedImageLayout.addWidget(self.imageLabel)

        self.setLayout(self.boxedImageLayout)

    def parseDetLabel(self):
        with open(detLabelFileName, 'r', encoding='utf-8') as detLabelFile:
            for line in detLabelFile:
                key, val_list = line.replace('converted', 'boxed').strip('\n').split('\t')
                key = str(PureWindowsPath(key))
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

    def setNewImage(self, boxedPath, croppedIdx):
        # cv2 image process -> convert QImage by https://stackoverflow.com/questions/71141162/unable-to-display-image-in-my-pyqt-program
        # pilImage = Image.open(boxedPath)
        # qim = ImageQt(pilImage)
        # newImage = QPixmap(boxedPath)
        stream = open(boxedPath, "rb")
        bytes = bytearray(stream.read())
        numpyarray = np.asarray(bytes, dtype=np.uint8)
        bgrImage = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)

        # draw annotation
        points = np.array(self.detLabel[boxedPath]['boxes'][croppedIdx])
        lined_img = cv2.polylines(bgrImage, [points], True, (0, 255, 0), 2)

        newImage = self.convert_cv_qt(lined_img)
        self.imageLabel.setPixmap(newImage)
        self.imageLabel.adjustSize()

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        # p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(convert_to_Qt_format)

class CroppedImageViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.imageLabel = QLabel()
        # self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.imageInferenceLabel = QLabel("please, open inference log file ", self)
        self.imageInferenceLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.imagePaths = ''
        self.imageInferenceText = ''
        # TODO add scroll
        # self.scrollArea = QScrollArea()
        # self.scrollArea.setBackgroundRole(QPalette.Dark)
        # self.scrollArea.setWidget(self.imageLabel)
        # self.scrollArea.setVisible(False)

        self.croppedImageLayout = QVBoxLayout()
        self.croppedImageLayout.addWidget(self.imageLabel)
        self.croppedImageLayout.addWidget(self.imageInferenceLabel)
        self.setLayout(self.croppedImageLayout)

    def setNewImage(self, imagePath, text, viewPathBool):
        self.imageLabel.setPixmap(QPixmap(imagePath))
        self.imageLabel.adjustSize()
        self.imageInferenceText, self.imagePaths = text.split('\n\n')
        self.croppedPath, self.boxedPath = self.imagePaths.strip().split('\n')
        self.imagePathDict = {
            Qt.Key.Key_C.value:self.croppedPath,
            Qt.Key.Key_B.value:self.boxedPath
        }
        self.setNewText(viewPathBool)

    def setNewText(self, viewPathBool):
        text = self.imageInferenceText
        if viewPathBool:
            text = '\n\n'.join([self.imageInferenceText, self.imagePaths])
        self.imageInferenceLabel.setText(text)
    
    def copyToClipboard(self, key):
        QApplication.clipboard().setText(self.imagePathDict[key])
    
    def viewOutSourcing(self):
        print('out sourcing failed TODO add scroll myself')
        # for img_path in self.imagePaths.strip().split('\n'):
        #     if os.path.exists(f"{img_path}"):
        #         # print(f"\"{img_path}\" exist try open image")
        #         # abspath = str(os.path.abspath(img_path)).replace("\\wsl$\Ubuntu-20.04", "Z:")
        #         # abspath = str(os.path.abspath(img_path)).replace("\\wsl$\Ubuntu-20.04", "Z:")
        #         print(str(os.path.abspath(img_path)).replace("\\\\wsl$\\Ubuntu-20.04", "Z:"))
        #         print(f"pwd: {os.popen('cd').read()}, abspath: {os.path.abspath(f'{img_path}')}")
        #         print(f"popen: \"{img_path}\"")
        #         # os.popen(f"cd && \"{abspath}\"")
        #         os.popen(f"echo {img_path} && \"Z:\home\sayi\workspace\OCR\TrainDataPreprocess\PDFPreprocess\cropped\&#65378;어린이 통학로 교통 안전 기본계획&#65379; 용역 중간보고회 결과보고\0_10_.png\"")

class TrainDataViewer(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.boxedImageViewer = BoxedImageViewer()
        self.croppedImageViewer = CroppedImageViewer()
        # self.createActions()
        # self.createMenus()

        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.croppedImageViewer)
        self.mainLayout.addWidget(self.boxedImageViewer)
        self.setLayout(self.mainLayout)

    def setNewImage(self, boxedPath, croppedPath, gt, viewPathBool):
        croppedIdx = int(os.path.basename(croppedPath).split('_')[1])
        self.boxedImageViewer.setNewImage(boxedPath, croppedIdx)
        self.croppedImageViewer.setNewImage(croppedPath, gt, viewPathBool)


if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # boxedImageViewer = BoxedImageViewer()
    # boxedImageViewer.setNewImage(fileName)
    # boxedImageViewer.show()

    croppedImageViewer = CroppedImageViewer()
    croppedImageViewer.setNewImage(fileName, "GT: \nresult")
    croppedImageViewer.show()

    # trainDataViewer = TrainDataViewer()
    # trainDataViewer.setNewImage(fileName, fileName, "GT: \nresult")
    # trainDataViewer.show()
    sys.exit(app.exec())
