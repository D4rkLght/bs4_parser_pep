from pathlib import Path

MAIN_DOC_URL = 'https://docs.python.org/3/'
BASE_DIR = Path(__file__).parent
WHATS_NEW_URL = 'https://docs.python.org/3/whatsnew/'
DOWNLOADS_URL = 'https://docs.python.org/3/download.html'
PEP_URL = 'https://peps.python.org/'
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}
