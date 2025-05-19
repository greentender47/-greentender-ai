from flask import Flask, request, jsonify
import openai
import PyPDF2
import requests
from io import BytesIO

app = Flask(__name__)
openai.api_key = "YOUR_OPENAI_API_KEY"  # यहाँ अपनी OpenAI API key लगाओ

@app.route('/ask', methods=['POST'])
def ask():
    prompt = request.json.get('prompt', '')
    response = {
        "explanation": f"Results for your search: {prompt}",
        "bids": [
            {
                "title": "Laptop Supply to Ministry of Defence",
                "department": "Ministry of Defence",
                "deadline": "2025-05-28",
                "pdf": "https://example.com/tender.pdf"
            },
            {
                "title": "Computer Procurement - NIC",
                "department": "Ministry of Electronics & IT",
                "deadline": "2025-06-01",
                "pdf": "https://example.com/nic.pdf"
            }
        ]
    }
    return jsonify(response)

@app.route('/explain-pdf', methods=['POST'])
def explain_pdf():
    pdf_url = request.json.get('pdf_url', '')
    try:
        response = requests.get(pdf_url)
        reader = PyPDF2.PdfReader(BytesIO(response.content))
        text = ""
        for page in reader.pages:
            text += page.extract_text()

        explanation = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Summarize the following tender document."},
                {"role": "user", "content": text[:2000]}
            ]
        )
        summary = explanation.choices[0].message['content']
        return jsonify({"explanation": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
