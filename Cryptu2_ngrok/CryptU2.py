import logging
from flask import Flask, render_template, request
from pyngrok import ngrok
from cryptography.fernet import Fernet

app = Flask(__name__)
ngrok.set_auth_token("YOUR_AUTH_TOKEN")

# Generate a secret key for AES encryption when the application starts
SECRET_KEY = Fernet.generate_key()
cipher_suite = Fernet(SECRET_KEY)

# Function to perform AES encryption
def aes_encrypt(plain_text):
    encrypted_text = cipher_suite.encrypt(plain_text.encode())
    return encrypted_text.decode()

# Function to perform AES decryption
def aes_decrypt(cipher_text):
    decrypted_text = cipher_suite.decrypt(cipher_text.encode())
    return decrypted_text.decode()

# Route for the index page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        operation = request.form.get('operation')
        key = request.form.get('key')
        message = request.form.get('message')

        # Validate inputs
        if not all([operation, message]):
            return render_template('index.html', error_message='Please fill in all fields.')

        # Perform operation
        if operation == 'E':
            cipher_text = aes_encrypt(message)
            result = f"Ciphertext: {cipher_text}"
        else:
            decrypted_text = aes_decrypt(message)
            result = f"Decrypted text: {decrypted_text}"

        return render_template('index.html', result=result)

    return render_template('index.html', error_message=None)

if __name__ == '__main__':
    public_url = ngrok.connect(name='flask').public_url
    print(" * ngrok URL: " + public_url + " *")
    app.run(host='0.0.0.0', port=80)
