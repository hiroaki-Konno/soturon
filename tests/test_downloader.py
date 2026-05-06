import os

from core.downloader import download


def test_download():
    url = "https://www.youtube.com/watch?v=BXWGrp0XXNo"
    filepath, title = download(url)

    assert title == "レッサーパンダの威嚇"
    assert os.path.isfile(filepath)
