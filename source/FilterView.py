from PyQt6.QtWidgets import QGridLayout

class FilterView():
    def __init__(self, filterGridLayout: QGridLayout):
        self.gtInclude = filterGridLayout.itemAtPosition(0, 1).widget()
        self.gtMatch = filterGridLayout.itemAtPosition(1, 1).widget()
        self.pdfInclude = filterGridLayout.itemAtPosition(2, 1).widget()
        self.indexLineEdit = filterGridLayout.itemAtPosition(3, 1).widget()

    def setImageIndex(self, idx):
        self.indexLineEdit.setText(str(idx))

    def getImageIndex(self):
        return int(self.indexLineEdit.text())
    
    def filter(self, logList):
        newLogList = []
        gtIncludeText = self.gtInclude.text()
        gtMatchText = self.gtMatch.text()
        pathIncludeText = self.pdfInclude.text()
        isFiltered = len(gtIncludeText) > 0 or len(gtMatchText) > 0 or len(pathIncludeText) > 0
        if isFiltered:
            for log in logList:
                path = log[0]
                gt = log[1].split('gt:')[-1]
                if (len(gtIncludeText) == 0 or gtIncludeText in gt) \
                and (len(gtMatchText) == 0 or gtMatchText in gt) \
                and (len(pathIncludeText) == 0 or pathIncludeText in path):
                    newLogList.append(log)
            return newLogList, isFiltered
        return logList, isFiltered