import time
from PyQt5 import QtWidgets, QtCore, QtGui


class InputOverlay(QtWidgets.QWidget):
    input_received = QtCore.pyqtSignal(str)
    key_group_timeout = 1.0  # seconds to reset the buffer

    def __init__(self):
        super().__init__()
        self.buffer = []
        self.last_time = None

        # QSettings (uses registry on Windows)
        self.settings = QtCore.QSettings("MyCompany", "KeyVisualizer")
        self._load_settings()

        # Wire up input signal
        self.input_received.connect(self.on_input)

        # Window flags: frameless, always-on-top, tool window
        flags = (
            QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.Tool
        )
        self.setWindowFlags(flags)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

        # Fullscreen overlay
        screen = QtWidgets.QApplication.primaryScreen().geometry()
        self.setGeometry(screen)

        # Label for key groups
        self.label = QtWidgets.QLabel("", self)
        self._apply_label_style()
        self._position_label()

    def _load_settings(self):
        self.color     = QtGui.QColor(self.settings.value("color", "#FFFFFF"))
        self.font_size = int(self.settings.value("font_size", 32))
        self.margin_x  = int(self.settings.value("margin_x", 20))
        self.margin_y  = int(self.settings.value("margin_y", 60))

    def _save_settings(self):
        self.settings.setValue("color",     self.color.name())
        self.settings.setValue("font_size", self.font_size)
        self.settings.setValue("margin_x",  self.margin_x)
        self.settings.setValue("margin_y",  self.margin_y)

    def _apply_label_style(self):
        font = QtGui.QFont("Consolas", self.font_size, QtGui.QFont.Bold)
        self.label.setFont(font)
        rgba = f"rgba({self.color.red()}, {self.color.green()}, {self.color.blue()}, 200)"
        self.label.setStyleSheet(f"color: {rgba};")
        self.label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)

    def _position_label(self):
        screen = QtWidgets.QApplication.primaryScreen().geometry()
        w = screen.width() - 2 * self.margin_x
        h = self.font_size + 10
        x = self.margin_x
        y = screen.height() - self.margin_y - h
        self.label.setGeometry(x, y, w, h)

    def apply_new_settings(self):
        self._save_settings()
        self._apply_label_style()
        self._position_label()

    def on_input(self, name: str):
        now = time.monotonic()
        if self.last_time is None or (now - self.last_time) > self.key_group_timeout:
            self.buffer = [name]
        else:
            self.buffer.append(name)
        self.last_time = now

        # if every entry is length‐1, treat as “text mode” and concatenate
        if all(len(item) == 1 for item in self.buffer):
            display = "".join(self.buffer)
        else:
            display = ", ".join(self.buffer)

        self.label.setText(display)

    def show(self):
        super().show()
        # re-apply style/position each time
        self._apply_label_style()
        self._position_label()
