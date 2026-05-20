from pathlib import Path

def load_qss(folder):
    folder = Path(folder)
    return "\n".join(
        f.read_text() for f in folder.rglob("*.qss")
    )