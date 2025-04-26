from pathlib import Path

from utils.temp_dir import TEMP_DIR


def get_best_filename(id) -> Path:
    work_dir = TEMP_DIR / str(id)

    if not work_dir.exists():
        return None
    
    best_files = list(work_dir.glob('*'))
    print(best_files)
    if len(best_files) != 1:
        return None
    
    return best_files[0]

