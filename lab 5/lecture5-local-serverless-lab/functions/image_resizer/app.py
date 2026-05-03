from flask import Flask, request, jsonify
from PIL import Image
from pathlib import Path
import time

app = Flask(__name__)

@app.route("/resize", methods=["POST"])
def resize_image():
    start_time = time.time()
    event = request.get_json()
    file_path = event.get("file_path")
    file_name = event.get("file_name")
    target_width = int(event.get("width", 300))

    if not file_path or not Path(file_path).exists():
        return jsonify({
            "status": "error",
            "message": "File path is missing or file does not exist",
            "received_event": event
        }), 400

    input_path = Path(file_path)
    output_dir = Path("/data/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"resized_{input_path.stem}.png"

    with Image.open(input_path) as img:
        original_size = img.size
        img.thumbnail((target_width, target_width))
        new_size = img.size
        img.save(output_path, format="PNG")

    processing_ms = round((time.time() - start_time) * 1000, 2)

    return jsonify({
        "status": "success",
        "function": "image-resizer",
        "input_file": file_name,
        "output_file": str(output_path),
        "original_size": original_size,
        "new_size": new_size,
        "processing_ms": processing_ms
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
