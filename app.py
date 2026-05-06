import json
import os

from flask import Flask, Response, jsonify, render_template, request, send_file
from flask import stream_with_context

from core.processor import Processor

app = Flask(__name__)
_processor = Processor()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/viewer")
def viewer():
    return render_template("viewer.html")


@app.route("/api/load", methods=["POST"])
def api_load():
    source = (request.json or {}).get("source", "").strip()
    if not source:
        return jsonify({"error": "source が未指定です"}), 400
    try:
        info = _processor.load(source)
        return jsonify({**info, "preview_url": "/api/preview"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/preview")
def api_preview():
    return send_file(os.path.abspath("./tmp/preview.jpg"), mimetype="image/jpeg")


@app.route("/api/start", methods=["POST"])
def api_start():
    data = request.json or {}
    pos1 = tuple(data["pos1"])
    pos2 = tuple(data["pos2"])
    _processor.start(pos1, pos2)
    return jsonify({"ok": True})


@app.route("/api/events")
def api_events():
    def generate():
        for event in _processor.event_stream():
            yield f"data: {json.dumps(event)}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.route("/api/frame/<int:index>")
def api_frame(index):
    path = _processor.get_frame_path(index)
    return send_file(os.path.abspath(path), mimetype="image/jpeg")


@app.route("/api/save", methods=["POST"])
def api_save():
    selected = (request.json or {}).get("selected", [])
    folder = _processor.save_selected(selected)
    return jsonify({"ok": True, "folder": folder})
