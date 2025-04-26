import tempfile
import atexit
import shutil
from pathlib import Path

TEMP_DIR = Path(tempfile.mktemp()) 


@atexit.register
def cleanup():
    shutil.rmtree(TEMP_DIR)
    print(f"Delete tmp dir")
