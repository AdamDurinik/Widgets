from PyQt5 import QtWidgets, QtGui
import InputOverlay as InputOverlay

class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, overlay: InputOverlay.InputOverlay):
        super().__init__(overlay)
        self.overlay = overlay
        self.setWindowTitle("KeyVisualizer Settings")
        self.setModal(True)

        layout = QtWidgets.QFormLayout(self)

        self.spin_size = QtWidgets.QSpinBox()
        self.spin_size.setRange(8, 200)
        self.spin_size.setValue(self.overlay.font_size)
        layout.addRow("Font Size:", self.spin_size)

        self.spin_x = QtWidgets.QSpinBox()
        self.spin_x.setRange(0, 500)
        self.spin_x.setValue(self.overlay.margin_x)
        layout.addRow("Horizontal Margin:", self.spin_x)

        self.spin_y = QtWidgets.QSpinBox()
        self.spin_y.setRange(0, 500)
        self.spin_y.setValue(self.overlay.margin_y)
        layout.addRow("Vertical Margin:", self.spin_y)

        self.btn_color = QtWidgets.QPushButton()
        self._update_color_button()
        self.btn_color.clicked.connect(self.choose_color)
        layout.addRow("Font Color:", self.btn_color)

        btns = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addRow(btns)

    def _update_color_button(self):
        c = self.overlay.color
        pix = QtGui.QPixmap(16, 16)
        pix.fill(c)
        self.btn_color.setIcon(QtGui.QIcon(pix))
        self.btn_color.setText(c.name())

    def choose_color(self):
        c = QtWidgets.QColorDialog.getColor(self.overlay.color, self, "Choose Font Color")
        if c.isValid():
            self.overlay.color = c
            self._update_color_button()

    def accept(self):
        self.overlay.font_size = self.spin_size.value()
        self.overlay.margin_x  = self.spin_x.value()
        self.overlay.margin_y  = self.spin_y.value()
        self.overlay.apply_new_settings()
        super().accept()
