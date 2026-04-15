'''main mapping functionality'''

import csv
from datetime import datetime
import logging as log
import os

from quickbase.const import FDIR

def extract(base_dir: str):
    """Return (files, _) relative to base_dir."""
    file_paths = []
    empty_dirs = []
    for root, dirs, filenames in os.walk(base_dir):
        rel_root = os.path.relpath(root, base_dir)
        rel_root = "." if rel_root == "." else rel_root
        for name in filenames:
            file_paths.append(name if rel_root == "." else os.path.join(rel_root, name))
        if not dirs and not filenames:
            empty_dirs.append(rel_root)

    # for path in file_paths:
    #     log.info("< %s", path)
    # log.info("EMPTY DIRS")
    # for path in empty_dirs:
    #     log.info("! %s", path)
    log.info("# %3d files", len(file_paths))
    log.info("# %3d empty dirs", len(empty_dirs))

    return file_paths, empty_dirs

def write_map_csv(csv_path: str, file_paths: list[str]):
    """Write a CSV with columns: path, agreement, type, filename."""
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["path", "agreement", "type", "filename"],
        )
        writer.writeheader()
        for path in file_paths:
            parts = path.split(os.sep)
            agreement = parts[0] if len(parts) >= 2 else ""
            doc_type = parts[1] if len(parts) >= 2 else ""
            filename = parts[-1] if parts else ""
            writer.writerow(
                {
                    "path": path,
                    "agreement": agreement,
                    "type": doc_type,
                    "filename": filename,
                }
            )

if __name__ == "__main__":
    f_paths, _ = extract(FDIR)
    log.info("START")

    out_dir = os.path.join(".", "data")
    os.makedirs(out_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path = os.path.join(out_dir, f"map-{timestamp}.csv")

    write_map_csv(out_path, f_paths)

    log.info("WROTE CSV %s", out_path)
    log.info("END")
