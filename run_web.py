import threading
import webbrowser

from app import app
from core.logger import setup_logger

PORT = 5000


def main():
    setup_logger()
    url = f"http://localhost:{PORT}"
    threading.Timer(1.5, lambda: webbrowser.open(url)).start()
    app.run(host="127.0.0.1", port=PORT, debug=False, threaded=True)


if __name__ == "__main__":
    main()
