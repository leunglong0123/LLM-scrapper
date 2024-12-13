from flask import Flask, request, jsonify
from controller.instagram_scrap import InstagramScraperController

app = Flask(__name__)

controller = InstagramScraperController()


@app.route('/api/scrape_instagram_post', methods=['POST'])
def scrape_instagram_post():
    """
    Endpoint to scrape an Instagram post.

    Request JSON structure:
    {
        "post_url": "string",
        "trace_id": "string"
    }

    Returns:
        JSON containing the extracted post data or an error message.
    """
    try:
        # Parse JSON request
        data = request.get_json()
        if not data or 'post_url' not in data or 'trace_id' not in data:
            return jsonify({"error": "Invalid request. 'post_url' and 'trace_id' are required."}), 400

        post_url = data['post_url']
        trace_id = data['trace_id']

        # Scrape the Instagram post
        extracted_data = controller.scrape_instagram_post(post_url, trace_id)

        # Return extracted data as JSON response
        return jsonify({"status": "success", "data": extracted_data.to_dict()}), 200

    except Exception as e:
        # Handle errors
        return jsonify({"status": "error", "message": str(e)}), 500


# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
