from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print(data)  # Log the received data for debugging

    if 'messages' in data:
        for message in data['messages']:
            if 'type' in message and message['type'] == 'image':
                media_url = message['image']['url']
                download_image(media_url, 'customer_image.jpg')
                return jsonify({"media_url": media_url}), 200

    return jsonify({"status": "no image"}), 200

def download_image(media_url, filename='downloaded_image.jpg'):
    response = requests.get(media_url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded image to {filename}")
    else:
        print("Failed to download image")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
