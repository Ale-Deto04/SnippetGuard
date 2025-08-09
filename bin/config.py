import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()

APP_NAME = "SnippetGuard"
MODEL_PATH = (BASE_DIR / "../model/trained_codebert").resolve()
LABELS_PATH = (BASE_DIR / "../model/labels.json").resolve()
THRESHOLD = 0.6
VERSION = f"{APP_NAME} 1.0"
AUTHOR = "Alessandro De Toffoli"

with open(LABELS_PATH, "r") as f:
	labels = json.load(f)
LABELS = labels
