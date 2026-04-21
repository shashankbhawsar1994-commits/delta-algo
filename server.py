from flask import Flask, request
from main import handle_signal

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)
        print("📥 Raw data:", data)

        signal = data.get("signal")

        if signal:
            handle_signal(signal)
        else:
            print("❌ No signal found")

    except Exception as e:
        print("❌ Error parsing request:", str(e))

    return {"status": "ok"}, 200


if __name__ == '__main__':
    app.run(port=5000)