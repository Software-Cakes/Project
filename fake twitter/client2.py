import requests

BASE_URL = 'http://localhost:5000'

def get_notes():
    response = requests.get(f'{BASE_URL}/notes')
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': 'Failed to fetch notes'}


def create_note_public(nickname, content):
    data = {'nickname': nickname, 'content': content, 'public': True}
    response = requests.post(f'{BASE_URL}/notes', json=data)
    if response.status_code == 200:
        return {'message': 'Note created successfully'}
    else:
        return {'error': 'Failed to create note'}


def create_note_private(sender, receiver, content):
    data = {'sender': sender, 'receiver': receiver, 'content': content, 'public': False}
    response = requests.post(f'{BASE_URL}/notes', json=data)
    if response.status_code == 200:
        return {'message': 'Note sent privately successfully'}
    else:
        return {'error': 'Failed to send private note'}


if __name__ == '__main__':
    # Prompt user to enter a nickname
    nickname = input("Enter your nickname: ")

    # Retrieve and display all existing notes
    print("Existing Notes:")
    notes = get_notes()
    for note in notes:
        print(f"{note['nickname']}: {note['content']}")
    print()  # Add a line break

    while True:
        choice = input("Do you want to (1) post a public note or (2) send a private note? Enter 1 or 2: ")

        if choice == '1':
            # Public note
            content = input("Enter your note: ")
            print(create_note_public(nickname, content))
        elif choice == '2':
            # Private note
            receiver = input("Enter the receiver's nickname: ")
            content = input("Enter your private note: ")
            print(create_note_private(nickname, receiver, content))
        else:
            print("Invalid choice. Please enter 1 or 2.")
