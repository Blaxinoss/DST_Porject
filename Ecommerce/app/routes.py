from app.scrapper import scrape_hardware, scrape_sigma, scrape_kimostore
from flask import Blueprint, request, jsonify
import logging

main = Blueprint('main', __name__)

@main.route('/search', methods=['POST'])
def search():
    try:
        request_data = request.json
        query = request_data.get('query', '')
        print(f"Received query: {query}")

        sigmaResults = scrape_sigma(query)
        hardwareResults = scrape_hardware(query)
        kimoResults = scrape_kimostore(query)


        if sigmaResults is None or hardwareResults is None or kimoResults is None:
            raise ValueError("Failed to retrieve data from scraping functions.")

        results = {
            "sigma": sigmaResults,
            "hardware": hardwareResults,
            "kimo": kimoResults,
        }

        return jsonify(results)
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return jsonify({"error": "Failed to process request"}), 500
