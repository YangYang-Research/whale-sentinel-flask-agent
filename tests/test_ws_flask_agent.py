from whale_sentinel_flask_agent import WhaleSentinelFlaskAgent
from flask import Flask, request, jsonify

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True, port=3000)