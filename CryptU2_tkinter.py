import tkinter as tk
from tkinter import messagebox, Entry, Label, Button, StringVar, Text
from cryptography.fernet import Fernet
import base64

class FernetApp:
    def __init__(self, master):
        self.master = master
        master.title("CryptU")

        self.operation_var = StringVar()
        self.message_var = StringVar()
        self.key_var = StringVar()

        Label(master, text="CryptU", font=("Helvetica", 24, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

        Label(master, text="Choose Operation:").grid(row=1, column=0, columnspan=2)
        Button(master, text="Encrypt", command=lambda: self.get_operation('E')).grid(row=2, column=0)
        Button(master, text="Decrypt", command=lambda: self.get_operation('D')).grid(row=2, column=1)

        Label(master, text="Enter Message:").grid(row=3, column=0, columnspan=2)
        Entry(master, textvariable=self.message_var).grid(row=4, column=0, columnspan=2)

        Label(master, text="Enter Key:").grid(row=5, column=0, columnspan=2)
        Entry(master, textvariable=self.key_var).grid(row=6, column=0, columnspan=2)

        self.result_text = Text(master, height=5, width=40)
        self.result_text.grid(row=7, column=0, columnspan=2)

        Button(master, text="Submit", command=self.perform_operation).grid(row=8, column=0, columnspan=2)
        Button(master, text="Reset", command=self.reset_fields).grid(row=9, column=0, columnspan=2)

    def encode_key(self, key):
        key_bytes = key.encode()
        padded_key = key_bytes.ljust(32, b'=')
        encoded_key = base64.urlsafe_b64encode(padded_key)
        return encoded_key

    def validate_key(self, key):
        try:
            encoded_key = self.encode_key(key)
            return encoded_key
        except Exception as e:
            raise ValueError("Invalid key format")

    def fernet_encrypt(self, plain_text, key):
        cipher_suite = Fernet(key)
        encrypted_text = cipher_suite.encrypt(plain_text.encode())
        return encrypted_text.decode()

    def fernet_decrypt(self, cipher_text, key):
        cipher_suite = Fernet(key)
        decrypted_text = cipher_suite.decrypt(cipher_text.encode())
        return decrypted_text.decode()

    def get_operation(self, operation):
        self.operation_var.set(operation)

    def perform_operation(self):
        operation = self.operation_var.get()
        message = self.message_var.get()
        key = self.key_var.get()

        if not operation or not message or not key:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            validated_key = self.validate_key(key)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        if operation == 'E':
            cipher_text = self.fernet_encrypt(message, validated_key)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"{cipher_text}\nKey: {key}")
        elif operation == 'D':
            try:
                decrypted_text = self.fernet_decrypt(message, validated_key)
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, f"{decrypted_text}")
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

    def reset_fields(self):
        self.operation_var.set('')
        self.message_var.set('')
        self.key_var.set('')
        self.result_text.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = FernetApp(root)
    root.mainloop()
