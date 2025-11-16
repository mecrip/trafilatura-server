from flask import Flask, request, jsonify
import trafilatura

app = Flask(__name__)

@app.route("/extract", methods=["POST"])
def extract():
    data = request.get_json()

    url = data.get("url")
    html = data.get("html")

    # Fetch HTML if URL is provided
    if url and not html:
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            return jsonify({"error": "Unable to fetch URL"}), 400
        html = downloaded

    if not html:
        return jsonify({"error": "Provide 'url' or 'html'"}), 400

    # Extract text in Markdown
    extracted = trafilatura.extract(
        html,
        output_format="markdown",
        include_formatting=True,
        include_comments=False
    )

    if not extracted:
        return jsonify({"error": "Extraction failed"}), 500

    return jsonify({
        "content": extracted,
        "success": True
    })