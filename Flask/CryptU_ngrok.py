import logging
from flask import Flask, render_template, request
from pyngrok import ngrok


app = Flask(__name__)
ngrok.set_auth_token("your_auth_token")

def vigenere_encrypt(plain_text, key):
    encrypted_text = ''
    key_repeated = (key * (len(plain_text) // len(key))) + key[:len(plain_text) % len(key)]

    for i in range(len(plain_text)):
        if plain_text[i].isalpha():
            shift = ord(key_repeated[i].upper()) - ord('A')
            if plain_text[i].isupper():
                encrypted_text += chr((ord(plain_text[i]) + shift - ord('A')) % 26 + ord('A'))
            else:
                encrypted_text += chr((ord(plain_text[i]) + shift - ord('a')) % 26 + ord('a'))
        else:
            encrypted_text += plain_text[i]

    return encrypted_text

def vigenere_decrypt(cipher_text, key):
    decrypted_text = ''
    key_repeated = (key * (len(cipher_text) // len(key))) + key[:len(cipher_text) % len(key)]

    for i in range(len(cipher_text)):
        if cipher_text[i].isalpha():
            shift = ord(key_repeated[i].upper()) - ord('A')
            if cipher_text[i].isupper():
                decrypted_text += chr((ord(cipher_text[i]) - shift - ord('A')) % 26 + ord('A'))
            else:
                decrypted_text += chr((ord(cipher_text[i]) - shift - ord('a')) % 26 + ord('a'))
        else:
            decrypted_text += cipher_text[i]

    return decrypted_text

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        operation = request.form.get('operation')
        key = request.form.get('key')
        message = request.form.get('message')

        if not operation or not key or not message:
            return render_template('index.html', error_message='Please fill in all fields.')

        if operation == 'E':
            cipher_text = vigenere_encrypt(message, key)
            result = f"Ciphertext: {cipher_text}"
        elif operation == 'D':
            decrypted_text = vigenere_decrypt(message, key)
            result = f"Decrypted text: {decrypted_text}"

        return render_template('index.html', result=result)

    return render_template('index.html', error_message=None)

if __name__ == '__main__':
	public_url = ngrok.connect(name='flask').public_url
	print(" * ngrok URL: " + public_url + " *")
	app.run(host='0.0.0.0', port=80)