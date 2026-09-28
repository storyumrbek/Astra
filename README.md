# iPhone Calculator for Windows

Dark iPhone-inspired desktop calculator built with Python/Tkinter.

- Basic arithmetic, parentheses, sign toggle, percent, and live preview
- Keyboard input, backspace, copy result, and persistent local history
- Safe AST-based calculator engine; no Python `eval`

Run from source with Python 3.10+: `python app.py`. Run tests: `python -m unittest -v`.
On Windows, `build_windows.bat` builds `dist/iPhoneCalculator.exe`.

GitHub Actions tests the app, builds a portable Windows EXE, uploads a 30-day artifact, and publishes a versioned release after each push to `main`.

Local history stays on the device: `%APPDATA%/iPhoneCalculator/history.json`.
