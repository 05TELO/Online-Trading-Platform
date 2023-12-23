from pathlib import Path

_this_file = Path(__file__).resolve()

DIR_REPO = _this_file.parent.parent.resolve()

DIR_STATIC = (DIR_REPO / "static").resolve()
