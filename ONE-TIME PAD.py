import tkinter as tk
from tkinter import messagebox, filedialog
import random
import string
def generate_random_key(length):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))
def one_time_pad_encrypt(plain_text, key):
    encrypted_text = []
    for pt_char, key_char in zip(plain_text.upper(), key):
        if pt_char.isalpha():
            encrypted_char = chr((ord(pt_char) - ord('A') + ord(key_char) - ord('A')) % 26 + ord('A'))
            encrypted_text.append(encrypted_char)
        else:
            encrypted_text.append(pt_char)
    return ''.join(encrypted_text)
def one_time_pad_decrypt(encrypted_text, key):
    decrypted_text = []
    for enc_char, key_char in zip(encrypted_text.upper(), key):
        if enc_char.isalpha():
            decrypted_char = chr((ord(enc_char) - ord('A') - (ord(key_char) - ord('A'))) % 26 + ord('A'))
            decrypted_text.append(decrypted_char)
        else:
            decrypted_text.append(enc_char)
    return ''.join(decrypted_text)
def encrypt():
    teks_asli = entry_teks.get("1.0", tk.END).strip()
    if not teks_asli:
        messagebox.showwarning("Input Error", "Mohon masukkan teks.")
        return
    key = entry_key.get().strip()
    if len(key) < len(teks_asli):
        messagebox.showwarning("Key Error", "Kunci harus sepanjang atau lebih panjang dari teks.")
        return
    hasil_enkripsi = one_time_pad_encrypt(teks_asli, key)
    entry_teks.delete("1.0", tk.END)
    entry_teks.insert(tk.END, f"{hasil_enkripsi}")
def decrypt():
    teks_enkripsi = entry_teks.get("1.0", tk.END).strip()
    if not teks_enkripsi:
        messagebox.showwarning("Input Error", "Mohon masukkan teks enkripsi.")
        return
    key = entry_key.get().strip()
    if len(key) < len(teks_enkripsi):
        messagebox.showwarning("Key Error", "Kunci harus sepanjang atau lebih panjang dari ciphertext.")
        return
    hasil_dekripsi = one_time_pad_decrypt(teks_enkripsi, key)
    entry_teks.delete("1.0", tk.END)
    entry_teks.insert(tk.END, f"{hasil_dekripsi}")
def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as file:
            teks = entry_teks.get("1.0", tk.END)
            file.write(teks)
def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
    if file_path:
        with open(file_path, 'rb') as file:
            teks = file.read()
            entry_teks.delete("1.0", tk.END) 
            entry_teks.insert(tk.END, teks.decode('utf-8', errors='ignore'))  
def upload_key_file():
    key_file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if key_file_path:
        with open(key_file_path, 'r', encoding='utf-8') as file:
            key = file.read().strip()
            entry_key.delete(0, tk.END)
            entry_key.insert(0, key)
root = tk.Tk()
root.title("One-Time Pad Cipher")
root.configure(bg='black')
frame_teks = tk.Frame(root, bg='black')
frame_teks.pack(pady=10)
label_teks = tk.Label(frame_teks, text="Masukkan teks yang ingin dienkripsi:", bg='black')
label_teks.pack()
entry_teks = tk.Text(frame_teks, width=50, height=10)
entry_teks.pack()
frame_key = tk.Frame(root, bg='black')
frame_key.pack(pady=10)
label_key = tk.Label(frame_key, text="Masukkan kunci:", bg='black')
label_key.pack()
entry_key = tk.Entry(frame_key, width=50)
entry_key.pack()
button_upload = tk.Button(root, text="Upload Dokumen", command=upload_file)
button_upload.pack(pady=5)
button_save = tk.Button(root, text="Simpan Hasil", command=save_file)
button_save.pack(pady=5)
button_upload_key = tk.Button(root, text="Upload Kunci dari File", command=upload_key_file)
button_upload_key.pack(pady=5)
frame_buttons = tk.Frame(root, bg='black')
frame_buttons.pack(pady=5)
button_decrypt = tk.Button(frame_buttons, text="Dekripsi", command=decrypt)
button_decrypt.pack(side=tk.LEFT, padx=(0, 10))
button_encrypt = tk.Button(frame_buttons, text="Enkripsi", command=encrypt)
button_encrypt.pack(side=tk.RIGHT, padx=(10, 0))
root.mainloop()
