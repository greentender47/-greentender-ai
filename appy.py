from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)  # Allow requests from frontend

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    prompt = data.get('prompt', '')

    # Custom prompt you can improve later
    system_prompt = f"Act as a GeM tender assistant. Search results for: {prompt}. Respond with 3 fake demo bids having fields: title, department, deadline, and PDF link. Also add a one-line explanation."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You return structured bid data as JSON."},
                {"role": "user", "content": system_prompt}
            ],
            temperature=0.6
        )

        content = response['choices'][0]['message']['content']
        # You must format the OpenAI response as proper JSON from the prompt
        # Below is a sample hardcoded fallback to simulate output
        fallback = {
            "explanation": "Here are 3 demo bids based on your search:",
            "bids": [
                {
                    "title": "Supply of School Furniture",
                    "department": "Ministry of Education",
                    "deadline": "2025-06-30",
                    "pdf": "https://example.com/furniture_bid.pdf"
                },
                {
                    "title": "Laptop Procurement for Rajasthan",
                    "department": "IT Department",
                    "deadline": "2025-07-10",
                    "pdf": "https://example.com/laptop_bid.pdf"
                },
                {
                    "title": "Stationery Items for KVS",
                    "department": "Kendriya Vidyalaya Sangathan",
                    "deadline": "2025-07-20",
                    "pdf": "https://example.com/stationery_bid.pdf"
                }
            ]
        }

        return jsonify(fallback)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/explain-pdf', methods=['POST'])
def explain_pdf():
    data = request.get_json()
    pdf_url = data.get('pdf_url', '')

    try:
        # In real case, you would fetch & read the PDF contents here.
        # For now, we simulate response
        explanation = f"This is a dummy explanation of the PDF at: {pdf_url}"
        return jsonify({"explanation": explanation})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
