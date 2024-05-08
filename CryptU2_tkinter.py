import tkinter as tk
from tkinter import messagebox, Entry, Label, Button, StringVar, Text
from cryptography.fernet import Fernet

class FernetApp:
    def __init__(self, master):
        self.master = master
        master.title("CryptU - Fernet Encryption")

        self.operation_var = StringVar()
        self.message_var = StringVar()

        Label(master, text="Choose Operation:").grid(row=0, column=0, columnspan=2)
        Button(master, text="Encrypt", command=lambda: self.get_operation('E')).grid(row=1, column=0)
        Button(master, text="Decrypt", command=lambda: self.get_operation('D')).grid(row=1, column=1)

        Label(master, text="Enter Message:").grid(row=2, column=0, columnspan=2)
        Entry(master, textvariable=self.message_var).grid(row=3, column=0, columnspan=2)

        self.result_text = Text(master, height=5, width=40)
        self.result_text.grid(row=4, column=0, columnspan=2)

        Button(master, text="Submit", command=self.perform_operation).grid(row=5, column=0, columnspan=2)
        Button(master, text="Reset", command=self.reset_fields).grid(row=6, column=0, columnspan=2)

        # Generate a random secret key for Fernet encryption
        self.secret_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.secret_key)

    def fernet_encrypt(self, plain_text):
        encrypted_text = self.cipher_suite.encrypt(plain_text.encode())
        return encrypted_text.decode()

    def fernet_decrypt(self, cipher_text):
        decrypted_text = self.cipher_suite.decrypt(cipher_text.encode())
        return decrypted_text.decode()

    def get_operation(self, operation):
        self.operation_var.set(operation)

    def perform_operation(self):
        operation = self.operation_var.get()
        message = self.message_var.get()

        if not operation or not message:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if operation == 'E':
            cipher_text = self.fernet_encrypt(message)
            self.result_text.delete(1.0, tk.END) 
            self.result_text.insert(tk.END, f"{cipher_text}\nKey: {self.secret_key.decode()}")
        elif operation == 'D':
            try:
                decrypted_text = self.fernet_decrypt(message)
                self.result_text.delete(1.0, tk.END)  
                self.result_text.insert(tk.END, f"{decrypted_text}")
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

    def reset_fields(self):
        self.operation_var.set('')
        self.message_var.set('')
        self.result_text.delete(1.0, tk.END)  

if __name__ == "__main__":
    root = tk.Tk()
    app = FernetApp(root)
    root.mainloop()
