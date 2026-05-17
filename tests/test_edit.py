from urllib.parse import quote


def _edit_url(live_server, folder):
    """Windowsパスをそのまま ?folder= に渡すためURLエンコードする"""
    return f"{live_server.url}/edit?folder={quote(folder, safe='/')}"


def test_images_displayed(page, live_server, score_fixture_folder):
    """fixtureフォルダの画像3枚が一覧表示される"""
    page.goto(_edit_url(live_server, score_fixture_folder))
    page.wait_for_selector(".edit-row")
    assert page.locator(".edit-row").count() == 3


def test_memo_input(page, live_server, score_fixture_folder):
    """各画像のメモ欄に入力できる"""
    page.goto(_edit_url(live_server, score_fixture_folder))
    page.wait_for_selector(".edit-memo")

    page.locator(".edit-memo").first.fill("テストメモ")
    assert page.locator(".edit-memo").first.input_value() == "テストメモ"


def test_generate_html(page, live_server, score_fixture_folder):
    """HTML生成ボタンで /api/generate が走り、完了ステータスが表示される"""
    page.goto(_edit_url(live_server, score_fixture_folder))
    page.wait_for_selector("#generate-btn")

    page.locator("#generate-btn").click()

    page.wait_for_selector("#status-text:has-text('生成完了')", timeout=5000)
    # HTML生成後に「HTMLを開く」ボタンが有効になっている
    assert not page.locator("#open-btn").is_disabled()
