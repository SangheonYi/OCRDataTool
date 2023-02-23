from PyQt6.QtWidgets import QMainWindow, QMenu, QFileDialog
from TrainDataView import TrainDataView
from PyQt6.QtGui import QAction
from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6 import uic
from pathlib import Path
from ocr_data_ui import Ui_MainWindow
from debug_mode import debug_mode

# form_class = uic.loadUiType("ocr_data_tool.ui")[0]
cache_file_name = 'dataTool.cache'
# class MainWindow(QMainWindow, form_class):
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.scaleFactor = 0.0
        self.logList = []
        self.notFilteredLogList = []
        self.currentImageIndex = -1
        self.viewPathBool = False
        self.trainDataView = TrainDataView(self)
        self.setCentralWidget(self.imageTopSplitter)
        self.imageTopSplitter.setSizes([800, 1200])
        self.croppedImageSplitter.setSizes([350, 500, 150])

        self.createActions()
        self.createMenus()
        self.setWindowTitle("Image View")
        self.resize(2000, 1000)

    @pyqtSlot()
    def openInfResult(self):
        if debug_mode:
            fileName = 'inspect_inf_result\parsed_inf.log'
        else:
            fileName, _ = QFileDialog.getOpenFileName(self, "Open logfile", ".", filter="inference *.log")
        if fileName:
            with open(fileName, 'r', encoding='utf-8') as logFile:
                rawLogList = logFile.readlines()
                for idx in range(len(rawLogList) // 5):
                    log4Lines =  rawLogList[5 * idx : 5 * (idx + 1)]
                    croppedPath = log4Lines[0][:-1].split('path: ')[1]
                    logGt = ''.join(log4Lines[1:])
                    self.logList.append((croppedPath, logGt))
                self.notFilteredLogList = self.logList.copy()
            if Path(cache_file_name).exists():
                with open(cache_file_name, 'r', encoding='utf-8') as cache_file:
                    cached_idx = int(cache_file.readline())
                    if cached_idx >= len(self.logList):
                        cached_idx = len(self.logList) -1 
                    self.currentImageIndex = cached_idx - 1
            self.nextImage()
            self.scaleFactor = 1.0

    def createMenus(self):
        self.fileMenu = QMenu("File", self)
        self.fileMenu.addAction(self.openAct)
        # TODO
        # self.fileMenu.addAction(self.openDetLabel)

        self.viewMenu = QMenu("View", self)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)

    def createActions(self):
        self.openAct = QAction("Open inference result", self, shortcut="Ctrl+O", triggered=self.openInfResult)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_Right.value:
            self.nextImage()
        elif key == Qt.Key.Key_Left.value:
            self.prevImage()
        elif key == Qt.Key.Key_O.value:
            self.trainDataView.croppedImageView.viewOutSourcing()
        elif key == Qt.Key.Key_P.value:
            self.viewPathBool = not self.viewPathBool
            self.trainDataView.croppedImageView.setNewText(self.viewPathBool)
        elif key in [Qt.Key.Key_C.value, Qt.Key.Key_B.value]:
            self.trainDataView.croppedImageView.copyToClipboard(key)
        elif key == Qt.Key.Key_Return.value or key == Qt.Key.Key_Enter.value: # enter or num pad enter
            self.dataFilter()
        else:
            print(event)

    def closeEvent(self, event) -> None:
        with open(cache_file_name, 'w', encoding='utf-8') as cache_file:
            cache_file.write(str(self.currentImageIndex))
        return super().closeEvent(event)
    
    # trigger methods
    def openImage(self):
        croppedPath, gt = self.logList[self.currentImageIndex]
        croppedPath = Path(croppedPath)
        boxedPageIdx = int(Path(croppedPath).stem.split('_')[0])
        boxedDir = Path(str(croppedPath.parent).replace('cropped', 'boxed'))
        ## for debug
        # wsl_path = Path("Z:\home\sayi\workspace\OCR\TrainDataPreprocess\PDFPreprocess\\")
        # boxedDir = wsl_path / Path(str(croppedPath.parent).replace('cropped', 'boxed'))
        ### for debug 

        boxedPath = sorted([str(itered_path) for itered_path in boxedDir.iterdir()])[boxedPageIdx] # sort key 지정 안 해서 멋대로 정렬되면 페이지 잘못 매핑될 수
        croppedPath = str(croppedPath)
        gt = '\n'.join([gt, croppedPath, boxedPath])
        self.trainDataView.setNewImage(boxedPath, croppedPath, gt, self.viewPathBool, self.currentImageIndex)

    def nextImage(self):
        if self.currentImageIndex + 1 < len(self.logList):
            self.currentImageIndex += 1
        else:
            self.currentImageIndex = 0
        print("next img", self.currentImageIndex, len(self.logList))
        self.openImage()

    def prevImage(self):
        if self.currentImageIndex > 0:
            self.currentImageIndex -= 1
        else:
            self.currentImageIndex = len(self.logList) - 1
        print("prev img", self.currentImageIndex, len(self.logList))
        self.openImage()

    def dataFilter(self):
        self.logList, isFiltered = self.trainDataView.fileterLogList(self.notFilteredLogList)
        self.currentImageIndex = -1 if isFiltered else self.trainDataView.getCroppedImageIndex() - 1
        self.nextImage()

if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    imageView = MainWindow()
    imageView.show()
    sys.exit(app.exec())