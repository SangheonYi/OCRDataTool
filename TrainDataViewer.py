import sys
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtWidgets import QLabel, QSizePolicy
from PyQt6.QtGui import QPixmap, QImage
from PIL import Image
import os

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
        newImage = QPixmap(imagePath)
        self.imageLabel.setPixmap(newImage)
        self.imageLabel.adjustSize()

class CroppedImageViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.imageLabel = QLabel()
        # self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.imageInferenceLabel = QLabel("please, open inference log file ", self)
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
        self.setNewText(viewPathBool)

    def setNewText(self, viewPathBool):
        text = self.imageInferenceText
        if viewPathBool:
            text = '\n\n'.join([self.imageInferenceText, self.imagePaths])
        self.imageInferenceLabel.setText(text)
    
    def viewOutSourcing(self):
        for img_path in self.imagePaths.strip().split('\n'):
            print(img_path)
            if os.path.exists(img_path):
                print(f"\"{img_path}\"")
                os.popen(f"cd \"{os.path.dirname(img_path)}\" && \"{os.path.basename(img_path)}\"")
        

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
