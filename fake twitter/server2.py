from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy database to store notes
notes_db = []


@app.route('/notes', methods=['GET'])
def get_notes():
    return jsonify(notes_db)


@app.route('/notes', methods=['POST'])
def create_note():
    data = request.json
    nickname = data.get('nickname')
    content = data.get('content')
    is_public = data.get('public', True)

    if nickname and content:
        if is_public:
            notes_db.append({'nickname': nickname, 'content': content, 'public': True})
            return jsonify({'message': 'Public note created successfully'})
        else:
            receiver = data.get('receiver')
            if receiver:
                notes_db.append({'nickname': nickname, 'content': content, 'receiver': receiver, 'public': False})
                return jsonify({'message': 'Private note sent successfully'})
            else:
                return jsonify({'error': 'Receiver nickname is required for private notes'}), 400
    else:
        return jsonify({'error': 'Nickname or content is missing'}), 400


if __name__ == '__main__':
    app.run(debug=True)
    