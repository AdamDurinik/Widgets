# Widgets

A collection of small desktop widgets.

## KeyVisualizer

A transparent, click-through overlay that shows your keyboard and mouse inputs in real time.
Group key sequences into “phrases” (resets after a configurable timeout), and automatically switch to plain text mode when you’re typing.

### Features

* **Global key & mouse hooks** (via `pynput`)
* **Transparent, always-on-top overlay** (via PyQt5)
* **Input grouping** with timeout (default 1 s)
* **Text mode**: concatenates single-character inputs cleanly
* **Systray icon** with a settings dialog for color, size & position
* **Settings persistence** in Windows registry (via QSettings)

### Installation

1. Clone this repo

   ```bash
   git clone https://github.com/AdamDurinik/Widgets.git
   cd Widgets
   ```
2. Install dependencies

   ```bash
   pip install PyQt5 pynput
   ```

### Usage

```bash
python key_visualizer.py
```

* The overlay appears immediately.
* Locate the tray icon (hidden under the up-arrow by default).
* Right-click → **Settings…** to adjust font color, size, and position.
* Changes are saved automatically to the registry.

### License

MIT © Adam Ďuriník
