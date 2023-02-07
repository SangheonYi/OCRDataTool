from PyQt6.QtWidgets import QMainWindow, QMenu, QFileDialog
from TrainDataViewer import TrainDataViewer
from PyQt6.QtGui import QAction
from pathlib import Path
from PyQt6.QtCore import pyqtSlot, Qt
fileName = "test.jpg"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scaleFactor = 0.0
        self.logList = []
        self.currentImageIndex = -1
        self.viewPathBool = False

        self.trainDataViewer = TrainDataViewer()
        self.setCentralWidget(self.trainDataViewer)

        self.createActions()
        self.createMenus()
        self.setWindowTitle("Image Viewer")
        self.resize(1900, 1600)
    @pyqtSlot()
    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open logfile", ".", filter="inference *.log")
        if fileName:
            with open(fileName, 'r', encoding='utf-8') as logFile:
                rawLogList = logFile.readlines()
                for idx in range(len(rawLogList) // 5):
                    log4Lines =  rawLogList[5 * idx : 5 * (idx + 1)]
                    croppedPath = log4Lines[0][:-1].split('path: ')[1]
                    logGt = ''.join(log4Lines[1:])
                    self.logList.append((croppedPath, logGt))
            self.nextImage()
            self.scaleFactor = 1.0

            self.fitToWindowAct.setEnabled(True)
            self.updateActions()

    def createMenus(self):
        self.fileMenu = QMenu("File", self)
        self.fileMenu.addAction(self.openAct)

        self.viewMenu = QMenu("View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)

    def createActions(self):
        self.openAct = QAction("Open...", self, shortcut="Ctrl+O", triggered=self.open)
        self.nextImageAct = QAction("Next image", self, shortcut="Right", triggered=self.nextImage)
        self.prevImageAct = QAction("Previous image", self, shortcut="Left", triggered=self.prevImage)
        self.zoomInAct = QAction("Zoom In (25%)", self, shortcut="Ctrl++", enabled=False, triggered=self.zoomIn)
        self.zoomOutAct = QAction("Zoom Out (25%)", self, shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)
        self.normalSizeAct = QAction("Normal Size", self, shortcut="Ctrl+S", enabled=False, triggered=self.normalSize)
        self.fitToWindowAct = QAction("Fit to Window", self, enabled=False, checkable=True, shortcut="Ctrl+F",
                                      triggered=self.fitToWindow)

    def keyPressEvent(self, event):
        key=event.key()
        if key==Qt.Key.Key_Right.value:
            self.nextImage()
        elif key==Qt.Key.Key_Left.value:
            self.prevImage()
        if key==Qt.Key.Key_P.value:
            self.viewPathBool = not self.viewPathBool
            self.trainDataViewer.croppedImageViewer.setNewText(self.viewPathBool)
        else:
            print(event)

    # trigger methods
    def openImage(self):
        croppedPath, gt = self.logList[self.currentImageIndex]
        croppedPath = Path(croppedPath)
        boxedPageIdx = int(Path(croppedPath).stem.split('_')[0])
        boxedDir = Path(str(croppedPath.parent).replace('cropped', 'boxed'))
        boxedPath = sorted([str(itered_path) for itered_path in boxedDir.iterdir()])[boxedPageIdx] # sort key 지정 안 해서 멋대로 정렬되면 페이지 잘못 매핑될 수
        croppedPath = str(croppedPath)
        gt = '\n'.join([gt, croppedPath, boxedPath])
        self.trainDataViewer.setNewImage(boxedPath, croppedPath, gt, self.viewPathBool)

    def nextImage(self):
        if self.currentImageIndex + 1 < len(self.logList):
            self.currentImageIndex += 1
            print("next img", self.currentImageIndex)
            self.openImage()

    def prevImage(self):
        if self.currentImageIndex - 1 >= 0:
            self.currentImageIndex -= 1
            print("prev img", self.currentImageIndex)
            self.openImage()

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.scaleFactor = 1.0

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        # self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

        self.updateActions()

    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        # self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        # self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        # self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

    def adjustScrollBar(self, scrollBar, factor):
        print('todo')
        # scrollBar.setValue(int(factor * scrollBar.value()
                            #    + ((factor - 1) * scrollBar.pageStep() / 2)))

if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    imageViewer = MainWindow()
    imageViewer.show()
    sys.exit(app.exec())