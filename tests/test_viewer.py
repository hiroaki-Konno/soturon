import json

SSE_EVENTS = [
    {"type": "frame_added", "index": 0},
    {"type": "frame_added", "index": 1},
    {"type": "frame_added", "index": 2},
    {"type": "trimming_done", "total": 3},
    {"type": "comparison_start"},
    {"type": "frame_classified", "index": 0, "is_peak": True, "distance": None},
    {"type": "frame_classified", "index": 1, "is_peak": False, "distance": 0.2},
    {"type": "frame_classified", "index": 2, "is_peak": True, "distance": 0.8},
    {"type": "comparison_done"},
    {"type": "stream_end"},
]


def _mock_viewer(page, dummy_jpeg):
    """
    EventSourceをJSで差し替えてネットワーク接続をなくし、
    フレーム画像だけroute()でモックする。
    """
    events_json = json.dumps(SSE_EVENTS)
    page.add_init_script(f"""
        const _events = {events_json};
        window.EventSource = class {{
            constructor(url) {{
                this._onmessage = null;
                this._onerror   = null;
                setTimeout(() => {{
                    _events.forEach(ev => {{
                        if (this._onmessage) {{
                            this._onmessage({{ data: JSON.stringify(ev) }});
                        }}
                    }});
                }}, 50);
            }}
            close() {{}}
            set onmessage(fn) {{ this._onmessage = fn; }}
            get onmessage()   {{ return this._onmessage; }}
            set onerror(fn)   {{ this._onerror = fn; }}
            get onerror()     {{ return this._onerror; }}
        }};
    """)
    page.route(
        "/api/frame/**",
        lambda route: route.fulfill(
            status=200,
            headers={"Content-Type": "image/jpeg"},
            body=dummy_jpeg,
        ),
    )


def test_frames_displayed(page, live_server, dummy_jpeg):
    """ピーク検出結果を踏まえたフレーム画像が表示される"""
    _mock_viewer(page, dummy_jpeg)
    page.goto(live_server.url + "/viewer")
    page.wait_for_selector(".thumb-item", timeout=5000)

    assert page.locator(".thumb-item").count() == 3

    # ピークフレーム(0)に .peak クラスが付いている
    thumb0_class = page.locator("#thumb-0").get_attribute("class")
    assert "peak" in thumb0_class

    # 非ピークフレーム(1)に .non-peak クラスが付いている
    thumb1_class = page.locator("#thumb-1").get_attribute("class")
    assert "non-peak" in thumb1_class


def test_toggle_selection(page, live_server, dummy_jpeg):
    """toggle-btn でフレームの選択/解除ができる"""
    _mock_viewer(page, dummy_jpeg)
    page.goto(live_server.url + "/viewer")
    page.wait_for_selector("#save-btn:not([disabled])", timeout=5000)

    # フレーム0はピークで初期選択済み → toggle-btnで解除
    page.locator("#thumb-0").click()
    assert "selected" in page.locator("#thumb-0").get_attribute("class")
    page.locator("#toggle-btn").click()
    assert "selected" not in page.locator("#thumb-0").get_attribute("class")

    # 再度クリックで選択に戻る
    page.locator("#toggle-btn").click()
    assert "selected" in page.locator("#thumb-0").get_attribute("class")


def test_save_button_enabled_after_sse(page, live_server, dummy_jpeg):
    """comparison_done 受信後に保存ボタンが有効になる"""
    _mock_viewer(page, dummy_jpeg)
    page.goto(live_server.url + "/viewer")
    page.wait_for_selector("#save-btn:not([disabled])", timeout=5000)


def test_save_sends_selected_indices(page, live_server, dummy_jpeg):
    """保存ボタンクリックでチェック済みフレームのindexが /api/save に渡される"""
    _mock_viewer(page, dummy_jpeg)
    page.goto(live_server.url + "/viewer")
    page.wait_for_selector("#save-btn:not([disabled])", timeout=5000)

    # リクエストのPOSTデータを直接キャプチャする
    with page.expect_request("**/api/save") as req_info:
        page.locator("#save-btn").click()

    body = json.loads(req_info.value.post_data)
    selected = body["selected"]
    # ピークフレーム(0, 2)が選択に含まれている
    assert 0 in selected
    assert 2 in selected
    # 非ピークフレーム(1)は含まれていない
    assert 1 not in selected
