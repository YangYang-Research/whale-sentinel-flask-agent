from whale_sentinel_flask_agent import WhaleSentinelFlaskAgent
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Create this folder
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit to 16 MB

ws_agent = WhaleSentinelFlaskAgent()

@app.route("/api/v1/search", methods=["POST"])
@ws_agent.whale_sentinel_agent_protection()
def search():
    """
    Search endpoint
    """
    # This is a placeholder for the actual search logic
    search_query = request.json.get("query")
    if not search_query:
        return jsonify({"error": "Query parameter is required"}), 400
    # Perform the search operation here
    response = {
        "query": search_query,
        "results": [
            {"id": 1, "name": "Result 1"},
            {"id": 2, "name": "Result 2"},
            {"id": 3, "name": "Result 3"},
        ],
    }
    return jsonify(response)    

@app.route("/api/v2/search", methods=["GET"])
@ws_agent.whale_sentinel_agent_protection()
def search_v2():
    """
    Search endpoint with query parameter
    """
    search_query = request.args.get("query")
    if not search_query:
        return jsonify({"error": "Query parameter is required"}), 400
    # Perform the search operation here
    response = {
        "query": search_query,
        "results": [
            {"id": 1, "name": "Result 1"},
            {"id": 2, "name": "Result 2"},
            {"id": 3, "name": "Result 3"},
        ],
    }
    return jsonify(response)

@app.route('/upload', methods=['POST'])
@ws_agent.whale_sentinel_agent_protection()
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']

    if file.filename == '':
        return "No selected file", 400

    filename = secure_filename(file.filename)

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return f"File {filename} uploaded successfully"

if __name__ == '__main__':
    app.run(debug=True, port=3001)
