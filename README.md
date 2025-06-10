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

---

## TaskTimer

A modern, dark-themed task tracker with billing-friendly features. Track time per task, pause/resume work sessions, and reorder tasks dynamically. Perfect for freelancers or consultants billing by time.

### Features

* **Custom task creation** with optional timers
* **Start / Pause / Reset** per-task timers
* **Drag-and-drop reordering**
* **Edit & delete tasks** easily
* **Persistent state** saved to `tasks.json`
* **Modern dark UI** with rounded buttons and fonts (via `customtkinter`)

### Installation

```bash
pip install customtkinter
```

### Usage

```bash
python Main.py
```

* Create tasks and track time.
* Drag tasks to reorder them.
* Timer states and durations are saved automatically.

---

### License

MIT © Adam Ďuriník
