from pathlib import Path
import os

FILE_PATH = Path(__file__).joinpath("..", "..", "..", "lessons").resolve()

START_DATE = "2024-01-01"
END_DATE = "2025-04-01"

os.environ['MY_VARIABLE'] = 'value'
