from PyQt6.QtWidgets import QLabel, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

class CroppedImageView():
    def __init__(self, imageLabel:QLabel, imageInferenceLabel :QLabel):

        self.imageLabel = imageLabel
        # self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.imageInferenceLabel = imageInferenceLabel
        self.imageInferenceLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.imagePaths = ''
        self.imageInferenceText = ''

        # TODO add scroll
        # self.scrollArea = QScrollArea()
        # self.scrollArea.setBackgroundRole(QPalette.Dark)
        # self.scrollArea.setWidget(self.imageLabel)
        # self.scrollArea.setVisible(False)

    # def setNewImage(self, imagePath, text, viewPathBool):
    def setNewImage(self, croppedImg, text, viewPathBool):
        self.imageLabel.setPixmap(croppedImg)
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
