'''main mapping functionality'''

import logging as log
import os

from quickbase.const import FDIR

def scan_dir(base_dir: str):
    """Return (files, empty_dirs) relative to base_dir."""
    file_paths = []
    empty_dirs = []
    for root, dirs, filenames in os.walk(base_dir):
        rel_root = os.path.relpath(root, base_dir)
        rel_root = "." if rel_root == "." else rel_root
        for name in filenames:
            file_paths.append(name if rel_root == "." else os.path.join(rel_root, name))
        if not dirs and not filenames:
            empty_dirs.append(rel_root)
    return file_paths, empty_dirs


if __name__ == "__main__":
    file_paths, empty_dirs = scan_dir(FDIR)
    log.info("START")
    for path in file_paths:
        log.info("< %s", path)
    log.info("EMPTY DIRS")
    for path in empty_dirs:
        log.info("! %s", path)
