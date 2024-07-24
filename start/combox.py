from PyQt6.QtWidgets import QComboBox

class CustomComboBox(QComboBox):
    def showPopup(self):
        self.setProperty("popupShown", True)
        self.style().polish(self)
        super().showPopup()

    def hidePopup(self):
        self.setProperty("popupShown", False)
        self.style().polish(self)
        super().hidePopup()