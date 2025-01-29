from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/lookup_nickname', methods=['POST'])
def lookup_nickname():
    # Get UID from the request payload
    uid = request.json.get('uid')
    if not uid:
        return jsonify({"error": "UID is required"}), 400

    # Create a session to maintain cookies
    session = requests.Session()

    # Get CSRF token
    csrf_url = 'https://uidtopup.com/api/auth/csrf'
    csrf_headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,id;q=0.8',
        'content-type': 'application/json',
        'referer': 'https://uidtopup.com/login',
    }
    csrf_response = session.get(csrf_url, headers=csrf_headers)
    csrf_token = csrf_response.json().get('csrfToken')

    # Login with credentials
    login_url = 'https://uidtopup.com/api/auth/callback/credentials'
    login_headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,id;q=0.8',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://uidtopup.com',
        'referer': 'https://uidtopup.com/login'
    }
    login_data = {
        'email': 'merokuku8@gmail.com',
        'password': 'GDC3@tVeNwAeJ',
        'redirect': 'false',
        'callbackUrl': '/',
        'csrfToken': csrf_token,
        'json': 'true'
    }
    session.post(login_url, headers=login_headers, data=login_data)

    # Nickname lookup
    nickname_url = f'https://uidtopup.com/api/data/ff-bd-nickname?uid={uid}'
    nickname_headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,id;q=0.8',
        'origin': 'https://uidtopup.com',
        'referer': 'https://uidtopup.com/product/1/free-fire-[bd-server]',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
    }
    nickname_response = session.post(nickname_url, headers=nickname_headers)

    return jsonify({
        "status": nickname_response.status_code,
        "nickname": nickname_response.text
    })

if __name__ == '__main__':
    app.run(debug=True)
