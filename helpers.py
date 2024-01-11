from flask import jsonify

def update_html_content(timestamp, message):
    return jsonify({'timestamp': timestamp, 'message': message})