import os
import sys
from pathlib import Path

if hasattr(sys, '_MEIPASS'):
    pywin32_path = Path(sys._MEIPASS) / 'pywin32_system32' #type: ignore
    if pywin32_path.exists():
        os.environ['PATH'] = str(pywin32_path) + os.pathsep + os.environ.get('PATH', '')
