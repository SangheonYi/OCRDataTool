import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QLabel, QSizePolicy, QScrollArea, QMessageBox, QMainWindow, QMenu, QAction
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter

fileName = "test.jpg"

class BoxedImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
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
        self.imageLabel.setPixmap(QPixmap(imagePath))
        self.imageLabel.adjustSize()

class CroppedImageViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setScaledContents(True)
        self.imageInferenceLabel = QLabel("please, open inference log file ", self)

        # TODO add scroll
        # self.scrollArea = QScrollArea()
        # self.scrollArea.setBackgroundRole(QPalette.Dark)
        # self.scrollArea.setWidget(self.imageLabel)
        # self.scrollArea.setVisible(False)

        self.croppedImageLayout = QVBoxLayout()
        self.croppedImageLayout.addWidget(self.imageLabel)
        self.croppedImageLayout.addWidget(self.imageInferenceLabel)
        self.setLayout(self.croppedImageLayout)

    def setNewImage(self, imagePath, gt):
        self.imageLabel.setPixmap(QPixmap(imagePath))
        self.imageLabel.adjustSize()
        self.imageInferenceLabel.setText(gt)

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

    def setNewImage(self, boxedPath, croppedPath, gt):
        self.boxedImageViewer.setNewImage(boxedPath)
        self.croppedImageViewer.setNewImage(croppedPath, gt)

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

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
    sys.exit(app.exec_())
