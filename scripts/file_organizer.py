"""
File Organizer - Auto-organize files into folders by type, date, or custom rules
No dependencies required - uses Python standard library only
"""
import os
import shutil
from pathlib import Path
from datetime import datetime


FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".heic", ".raw"],
    "Videos": [".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".m4v", ".webm"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf", ".md"],
    "Spreadsheets": [".xlsx", ".xls", ".csv", ".ods", ".numbers"],
    "Presentations": [".pptx", ".ppt", ".odp", ".key"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "Code": [".py", ".js", ".ts", ".html", ".css", ".java", ".cpp", ".c", ".go", ".rs"],
    "Executables": [".exe", ".msi", ".dmg", ".deb", ".rpm", ".sh", ".bat"],
    "Data": [".json", ".xml", ".yaml", ".yml", ".sql", ".db", ".sqlite"],
}


def organize_by_type(source_folder: str, dest_folder: str = None, dry_run: bool = False) -> dict:
    """
    Move files into subfolders based on file type.
    If dest_folder is None, organizes in place.
    Set dry_run=True to preview without moving files.
    """
    source = Path(source_folder)
    dest = Path(dest_folder) if dest_folder else source
    moved = {}

    for file in source.iterdir():
        if not file.is_file():
            continue
        category = _get_category(file.suffix.lower())
        target_dir = dest / category
        target_path = target_dir / file.name

        if not dry_run:
            target_dir.mkdir(parents=True, exist_ok=True)
            target_path = _safe_path(target_path)
            shutil.move(str(file), str(target_path))

        moved.setdefault(category, []).append(file.name)
        print(f"  {'[DRY RUN] ' if dry_run else ''}в†’ {category}/{file.name}")

    summary = {cat: len(files) for cat, files in moved.items()}
    print(f"\nSummary: {sum(summary.values())} files organized")
    return summary


def organize_by_date(source_folder: str, dest_folder: str = None, fmt: str = "%Y/%m") -> dict:
    """
    Move files into Year/Month subfolders based on modification date.
    fmt examples: "%Y/%m" в†’ 2024/05, "%Y" в†’ 2024, "%Y/%m/%d" в†’ 2024/05/20
    """
    source = Path(source_folder)
    dest = Path(dest_folder) if dest_folder else source
    moved = {}

    for file in source.iterdir():
        if not file.is_file():
            continue
        mtime = datetime.fromtimestamp(file.stat().st_mtime)
        folder_name = mtime.strftime(fmt)
        target_dir = dest / folder_name
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = _safe_path(target_dir / file.name)
        shutil.move(str(file), str(target_path))
        moved.setdefault(folder_name, []).append(file.name)
        print(f"  в†’ {folder_name}/{file.name}")

    return {k: len(v) for k, v in moved.items()}


def rename_bulk(folder: str, prefix: str = "", suffix: str = "", counter_start: int = 1) -> list:
    """
    Rename all files in a folder with a prefix, suffix, and sequential number.
    Example: prefix="photo_", suffix="" в†’ photo_001.jpg, photo_002.jpg
    """
    files = sorted(Path(folder).iterdir())
    renamed = []
    for i, file in enumerate(files, start=counter_start):
        if not file.is_file():
            continue
        new_name = f"{prefix}{i:03d}{suffix}{file.suffix}"
        new_path = file.parent / new_name
        file.rename(new_path)
        renamed.append((file.name, new_name))
        print(f"  {file.name} в†’ {new_name}")
    return renamed


def _get_category(ext: str) -> str:
    for category, extensions in FILE_TYPES.items():
        if ext in extensions:
            return category
    return "Other"


def _safe_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem, suffix = path.stem, path.suffix
    counter = 1
    while path.exists():
        path = path.parent / f"{stem}_{counter}{suffix}"
        counter += 1
    return path


if __name__ == "__main__":
    print("File Organizer - Examples:")
    print()
    print("1. Organize Desktop by file type:")
    print("   organize_by_type(r'C:\\Users\\You\\Desktop')")
    print()
    print("2. Preview first (no actual moving):")
    print("   organize_by_type('Downloads', dry_run=True)")
    print()
    print("3. Organize photos by date:")
    print("   organize_by_date('My Photos', fmt='%Y/%m')")
    print()
    print("4. Rename files sequentially:")
    print("   rename_bulk('photos', prefix='vacation_2024_')")
