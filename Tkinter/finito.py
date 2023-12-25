import sys
import tkinter as tk
from tkinter import messagebox, Entry, Label, Button, StringVar, Text

class VigenereApp:
    def __init__(self, master):
        self.master = master
        master.title("CryptU")

        self.operation_var = StringVar()
        self.key_var = StringVar()
        self.message_var = StringVar()

        Label(master, text="Choose Operation:").grid(row=0, column=0, columnspan=2)
        Button(master, text="Encrypt", command=lambda: self.get_operation('E')).grid(row=1, column=0)
        Button(master, text="Decrypt", command=lambda: self.get_operation('D')).grid(row=1, column=1)

        Label(master, text="Enter Key:").grid(row=2, column=0, columnspan=2)
        Entry(master, textvariable=self.key_var).grid(row=3, column=0, columnspan=2)

        Label(master, text="Enter Message:").grid(row=4, column=0, columnspan=2)
        Entry(master, textvariable=self.message_var).grid(row=5, column=0, columnspan=2)

        self.result_text = Text(master, height=5, width=40)
        self.result_text.grid(row=6, column=0, columnspan=2)

        Button(master, text="Submit", command=self.perform_operation).grid(row=7, column=0, columnspan=2)
        Button(master, text="Reset", command=self.reset_fields).grid(row=8, column=0, columnspan=2)

    def vigenere_encrypt(self, plain_text, key):
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

    def vigenere_decrypt(self, cipher_text, key):
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

    def get_operation(self, operation):
        self.operation_var.set(operation)

    def perform_operation(self):
        operation = self.operation_var.get()
        key = self.key_var.get()
        message = self.message_var.get()

        if not operation or not key or not message:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if operation == 'E':
            cipher_text = self.vigenere_encrypt(message, key)
            self.result_text.delete(1.0, tk.END) 
            self.result_text.insert(tk.END, f"Ciphertext: {cipher_text}")
        elif operation == 'D':
            decrypted_text = self.vigenere_decrypt(message, key)
            self.result_text.delete(1.0, tk.END)  
            self.result_text.insert(tk.END, f"Decrypted text: {decrypted_text}")

    def reset_fields(self):
        self.operation_var.set('')
        self.key_var.set('')
        self.message_var.set('')
        self.result_text.delete(1.0, tk.END)  

if __name__ == "__main__":
    root = tk.Tk()
    app = VigenereApp(root)
    root.mainloop()
