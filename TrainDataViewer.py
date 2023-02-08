import sys
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtWidgets import QLabel, QSizePolicy
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import numpy
import os
import cv2

fileName = "test.jpg"

class BoxedImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.imageLabel = QLabel()
        # self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.imageLabel.setScaledContents(True)

        # TODO add scroll
        # self.scrollArea = QScrollArea()
        # self.scrollArea.setBackgroundRole(QPalette.Dark)
        # self.scrollArea.setWidget(self.imageLabel)
        # self.scrollArea.setVisible(False)

        self.boxedImageLayout = QVBoxLayout()
        self.boxedImageLayout.addWidget(self.imageLabel)

        self.setLayout(self.boxedImageLayout)

    def setNewImage(self, imagePath):
        # cv2 image process -> convert QImage by https://stackoverflow.com/questions/71141162/unable-to-display-image-in-my-pyqt-program
        # pilImage = Image.open(imagePath)
        # qim = ImageQt(pilImage)
        # newImage = QPixmap(imagePath)
        stream = open(imagePath, "rb")
        bytes = bytearray(stream.read())
        numpyarray = numpy.asarray(bytes, dtype=numpy.uint8)
        bgrImage = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
        newImage = self.convert_cv_qt(bgrImage)
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
        self.boxedImageViewer.setNewImage(boxedPath)
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
