from flask import Flask, request, jsonify
from inference.verify import verify_signature

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "AI Signature Fraud Backend Running"

@app.route("/verify", methods=["POST"])
def verify():
    if "ref" not in request.files or "test" not in request.files:
        return jsonify({"error": "Both reference and test signatures required"}), 400

    ref_file = request.files["ref"]
    test_file = request.files["test"]

    ref_path = "temp_ref.png"
    test_path = "temp_test.png"

    ref_file.save(ref_path)
    test_file.save(test_path)

    result = verify_signature(ref_path, test_path)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)

