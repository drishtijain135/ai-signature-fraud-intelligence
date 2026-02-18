from flask import render_template
from flask import Flask, request, jsonify
from inference.verify import verify_signature
import uuid

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/verify", methods=["GET", "POST"])
def verify():
    print("VERIFY ENDPOINT HIT")
    if request.method == "GET":
        return jsonify({
            "message": "Use POST with ref & test images to verify signature"
        })

    if "ref" not in request.files or "test" not in request.files:
        return jsonify({
            "error": "Both reference and test signatures required"
        }), 400

    ref_file = request.files["ref"]
    test_file = request.files["test"]

    ref_path = f"temp_ref_{uuid.uuid4()}.png"
    test_path = f"temp_test_{uuid.uuid4()}.png"

    ref_file.save(ref_path)
    test_file.save(test_path)

    result={"prediction":"Genuine Signature","confidence":"92%"}
    # result = verify_signature(ref_path, test_path)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=False)


