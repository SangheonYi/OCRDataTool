import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit
from PyQt6.QtWidgets import QLabel, QSizePolicy
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import numpy as np
import os
import cv2
import json
from pathlib import Path

fileName = "test.jpg"
detLabelFileName = 'det_train.txt'
detLabelFileName = 'det_label.log'

class BoxedImageView(QWidget):
    def __init__(self, imageLabel: QLabel):
        super().__init__()

        self.imageLabel = imageLabel
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

    def parseDetLabel(self):
        with open(detLabelFileName, 'r', encoding='utf-8') as detLabelFile:
            for line in detLabelFile:
                key, val_list = line.replace('converted', 'boxed').strip('\n').split('\t')
                ## for debug
                wsl_path = Path("Z:\home\sayi\workspace\OCR\TrainDataPreprocess\PDFPreprocess\\")
                key = str(wsl_path.joinpath(key))
                # key = str(key)
                ## for debug
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
        # p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(convert_to_Qt_format)

class CroppedImageView():
    def __init__(self, imageLabel:QLabel, imageInferenceLabel :QLabel, indexLineEdit: QLineEdit):

        self.imageLabel = imageLabel
        # self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.imageInferenceLabel = imageInferenceLabel
        self.imageInferenceLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.imagePaths = ''
        self.imageInferenceText = ''

        self.indexLineEdit = indexLineEdit
        # TODO add scroll
        # self.scrollArea = QScrollArea()
        # self.scrollArea.setBackgroundRole(QPalette.Dark)
        # self.scrollArea.setWidget(self.imageLabel)
        # self.scrollArea.setVisible(False)

        # self.croppedImageLayout = QVBoxLayout()
        # self.croppedImageLayout.addWidget(self.imageLabel)
        # self.croppedImageLayout.addWidget(self.imageInferenceLabel)
        # self.setLayout(self.croppedImageLayout)

    # def setNewImage(self, imagePath, text, viewPathBool):
    def setNewImage(self, croppedImg, text, viewPathBool):
        self.imageLabel.setPixmap(croppedImg)
        # self.imageLabel.setPixmap(QPixmap(imagePath))
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

    def setImageIndex(self, idx):
        self.indexLineEdit.setText(str(idx))
    
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

class TrainDataView():
    def __init__(self, main_window) -> None:
        self.boxedImageView = BoxedImageView(main_window.boxedImageLabel)
        self.croppedImageView = CroppedImageView(main_window.croppedImageLabel, main_window.imageInferenceLabel, main_window.imageIndexLineEdit)

    def setNewImage(self, boxedPath, croppedPath, gt, viewPathBool, currentImageIndex):
        croppedIdx = int(os.path.basename(croppedPath).split('_')[1])
        croppedImg = self.boxedImageView.setNewImage(boxedPath, croppedIdx)
        self.croppedImageView.setNewImage(croppedImg, gt, viewPathBool)
        self.croppedImageView.setImageIndex(currentImageIndex)

if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # boxedImageView = BoxedImageView()
    # boxedImageView.setNewImage(fileName)
    # boxedImageView.show()

    croppedImageView = CroppedImageView()
    croppedImageView.setNewImage(fileName, "GT: \nresult")
    croppedImageView.show()

    # trainDataView = TrainDataView()
    # trainDataView.setNewImage(fileName, fileName, "GT: \nresult")
    # trainDataView.show()
    sys.exit(app.exec())