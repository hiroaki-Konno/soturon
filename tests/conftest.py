import threading
from types import SimpleNamespace

import cv2
import numpy as np
import pytest
from werkzeug.serving import make_server

import app as flask_module


@pytest.fixture(scope="session")
def app():
    flask_module.app.config["TESTING"] = True
    return flask_module.app


@pytest.fixture(scope="session")
def live_server(app):
    """Windowsのmultiprocessing制約を回避するスレッドベースのサーバー"""
    server = make_server("127.0.0.1", 0, app)
    port = server.socket.getsockname()[1]
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    yield SimpleNamespace(url=f"http://127.0.0.1:{port}")
    server.shutdown()


@pytest.fixture(scope="session")
def dummy_jpeg():
    """viewerのフレーム画像モック用: 50x100のグレーJPEGバイト列"""
    img = np.ones((50, 100, 3), dtype=np.uint8) * 200
    _, buf = cv2.imencode(".jpg", img)
    return bytes(buf)


@pytest.fixture(scope="session")
def score_fixture_folder(tmp_path_factory):
    """editページ用: ダミー画像3枚入りのtmpフォルダ"""
    folder = tmp_path_factory.mktemp("score_test")
    img = np.ones((100, 200, 3), dtype=np.uint8) * 200
    for i in range(1, 4):
        cv2.imwrite(str(folder / f"img_{i:03d}.jpg"), img)
    return str(folder)
