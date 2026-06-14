#!/usr/bin/env python3
"""
Punto de entrada de la aplicación Wi‑Fi Password Viewer.
"""
from ui.app import WifiPasswordViewer

if __name__ == "__main__":
    app = WifiPasswordViewer()
    app.mainloop()
