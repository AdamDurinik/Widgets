import sys
import threading
from pathlib import Path
from PyQt5 import QtWidgets,  QtGui
from pynput.keyboard import Listener as KListener, Key, KeyCode
from pynput.mouse import Listener as MListener
from InputOverlay import InputOverlay
from SettingsDialog import SettingsDialog

# ------------------------------------------------------------
# Listeners for keyboard and mouse
# ------------------------------------------------------------
def listen_keyboard(overlay: InputOverlay):
    modifiers = set()
    MODIFIER_KEYS = {
        Key.ctrl_l: "CTRL",
        Key.ctrl_r: "CTRL",
        Key.shift:  "SHIFT",
        Key.shift_r:"SHIFT",
        Key.alt_l:   "ALT",
        Key.alt_r:   "ALT",
        Key.cmd:     "META",
        Key.cmd_r:   "META",
    }
    ORDER = ["CTRL", "ALT", "SHIFT", "META"]

    def on_press(key):
        # track modifiers
        if key in MODIFIER_KEYS:
            modifiers.add(MODIFIER_KEYS[key])
            return

        # spacebar as real space
        if key == Key.space and not modifiers:
            overlay.input_received.emit(" ")
            return

        # printable vs. special
        if isinstance(key, Key):
            base = key.name.upper()
        elif isinstance(key, KeyCode) and key.char and key.char.isprintable():
            base = key.char.upper()
        elif isinstance(key, KeyCode) and hasattr(key, "vk") and 32 <= key.vk <= 126:
            base = chr(key.vk).upper()
        else:
            base = str(key).split('.')[-1].upper()

        if modifiers:
            combo = "+".join(sorted(modifiers, key=lambda m: ORDER.index(m)) + [base])
            overlay.input_received.emit(combo)
        else:
            overlay.input_received.emit(base)

    def on_release(key):
        if key in MODIFIER_KEYS:
            modifiers.discard(MODIFIER_KEYS[key])

    with KListener(on_press=on_press, on_release=on_release):
        threading.Event().wait()

def listen_mouse(overlay: InputOverlay):
    def on_click(x, y, button, pressed):
        if pressed:
            btn = str(button).split('.')[-1].upper()
            overlay.input_received.emit(f"{btn}_CLICK")
    with MListener(on_click=on_click):
        threading.Event().wait()

# ------------------------------------------------------------
# Main: app, overlay, tray, threads
# ------------------------------------------------------------
def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    overlay = InputOverlay()
    overlay.show()

    threading.Thread(target=listen_keyboard, args=(overlay,), daemon=True).start()
    threading.Thread(target=listen_mouse,   args=(overlay,), daemon=True).start()

    icon_path = Path(__file__).parent / "alt.png"
    tray = QtWidgets.QSystemTrayIcon(QtGui.QIcon(str(icon_path)), app)
    tray.setToolTip("KeyVisualizer")
    tray.setVisible(True)

    menu = QtWidgets.QMenu()
    menu.addAction("Settings…", lambda: SettingsDialog(overlay).exec_())
    menu.addSeparator()
    menu.addAction("Exit", app.quit)
    tray.setContextMenu(menu)

    tray.activated.connect(
        lambda reason: SettingsDialog(overlay).exec_()
        if reason == QtWidgets.QSystemTrayIcon.DoubleClick
        else None
    )

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
