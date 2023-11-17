from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def get_completion(model="gpt-3.5-turbo"):
    try:
        user_input = request.json.get("input")
        client = openai.OpenAI(api_key='API_KEY')
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": user_input}],
        )
        response = completion.choices[0].message.content
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
