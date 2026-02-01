import sys
import os
import traceback
import webbrowser
from app.utils import base_path

# ----------------------------------------
# ----------------------------------------
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")
if sys.stdin is None:
    sys.stdin = open(os.devnull, "r")

# ----------------------------------------
os.chdir(base_path())

try:
    import uvicorn
except Exception:
    traceback.print_exc()
    sys.exit(1)

try:
    webbrowser.open("http://127.0.0.1:8000")

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,

        #CRITICAL FLAGS
        log_config=None,      # disable logging config
        access_log=False,     # disable access logger
        use_colors=False,     # avoid stdout.isatty()
    )

except Exception:
    traceback.print_exc()
    sys.exit(1) 