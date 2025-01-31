import os
from flask import Flask, jsonify, request
import requests

# إعداد تطبيق Flask
app = Flask(__name__)

# إعداد API URLs و Tokens من البيئة
openai_api_url = "https://api.openai.com/v1/completions"  # رابط OpenAI API
gemini_api_url = "https://gemini-api-url.com"  # ضع رابط Gemini الفعلي هنا
huggingface_api_url = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"  # رابط Hugging Face API

# تحميل التوكنات من البيئة
openai_token = os.getenv("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")
huggingface_token = os.getenv("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")
gemini_token = os.getenv("AIzaSyAcUUmslv9NRNh_ozfcO9GesEWyx2Dnkr8")

# دالة للتفاعل مع OpenAI API
def get_openai_response(prompt):
    headers = {
        "Authorization": f"Bearer {openai_token}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "text-davinci-003",  # أو أي نموذج آخر من OpenAI
        "prompt": prompt,
        "max_tokens": 150
    }
    response = requests.post(openai_api_url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to get response from OpenAI API, status code: {response.status_code}", "response": response.text}

# دالة للتفاعل مع Gemini API
def get_gemini_response(query):
    headers = {
        "Authorization": f"Bearer {gemini_token}"
    }
    data = {
        "query": query
    }
    response = requests.post(gemini_api_url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to get response from Gemini API, status code: {response.status_code}", "response": response.text}

# دالة للتفاعل مع Hugging Face API
def get_huggingface_response(inputs):
    headers = {
        "Authorization": f"Bearer {huggingface_token}"
    }
    response = requests.post(huggingface_api_url, headers=headers, json={"inputs": inputs})
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to get response from Hugging Face API, status code: {response.status_code}", "response": response.text}

# نقطة النهاية لواجهة المستخدم
@app.route('/')
def home():
    return "Welcome to the AI APIs Integration!"

# نقطة النهاية لـ OpenAI
@app.route('/api/openai', methods=['POST'])
def openai_api():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    result = get_openai_response(prompt)
    return jsonify(result)

# نقطة النهاية لـ Gemini
@app.route('/api/gemini', methods=['POST'])
def gemini_api():
    data = request.get_json()
    query = data.get("query")
    if not query:
        return jsonify({"error": "Query is required"}), 400
    result = get_gemini_response(query)
    return jsonify(result)

# نقطة النهاية لـ Hugging Face
@app.route('/api/huggingface', methods=['POST'])
def huggingface_api():
    data = request.get_json()
    inputs = data.get("inputs")
    if not inputs:
        return jsonify({"error": "Inputs are required"}), 400
    result = get_huggingface_response(inputs)
    return jsonify(result)
