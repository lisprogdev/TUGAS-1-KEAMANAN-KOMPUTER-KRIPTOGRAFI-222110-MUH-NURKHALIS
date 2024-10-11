import tkinter as tk
from tkinter import messagebox, filedialog
import os
def vigenere_encrypt(teks_asli, kata_kunci):
    teks_enkripsi = ""
    kata_kunci_diulang = (kata_kunci * (len(teks_asli) // len(kata_kunci) + 1))[:len(teks_asli)]
    for t_char, k_char in zip(teks_asli, kata_kunci_diulang):
        if t_char.isalpha():
            shift = (ord(t_char.upper()) - ord('A') + ord(k_char.upper()) - ord('A')) % 26
            huruf_enkripsi = chr(shift + ord('A'))
            teks_enkripsi += huruf_enkripsi
        else:
            teks_enkripsi += t_char
    return teks_enkripsi
def vigenere_decrypt(teks_enkripsi, kata_kunci):
    teks_dekripsi = ""
    kata_kunci_diulang = (kata_kunci * (len(teks_enkripsi) // len(kata_kunci) + 1))[:len(teks_enkripsi)]
    for e_char, k_char in zip(teks_enkripsi, kata_kunci_diulang):
        if e_char.isalpha():
            shift = (ord(e_char.upper()) - ord('A') - (ord(k_char.upper()) - ord('A'))) % 26
            huruf_dekripsi = chr(shift + ord('A'))
            teks_dekripsi += huruf_dekripsi
        else:
            teks_dekripsi += e_char
    return teks_dekripsi
def encrypt():
    teks_asli = entry_teks.get("1.0", tk.END).strip()
    kata_kunci = entry_kunci.get()
    if not teks_asli or not kata_kunci:
        messagebox.showwarning("Input Error", "Mohon masukkan teks dan kata kunci.")
        return
    hasil_enkripsi = vigenere_encrypt(teks_asli, kata_kunci)
    entry_teks.delete("1.0", tk.END) 
    entry_teks.insert(tk.END, hasil_enkripsi) 
    cipherteks_kelompok = ' '.join([hasil_enkripsi[i:i+5] for i in range(0, len(hasil_enkripsi), 5)])
    label_cipherteks.config(text=f"Cipherteks (5-huruf): {cipherteks_kelompok}")
def decrypt():
    teks_enkripsi = entry_teks.get("1.0", tk.END).strip()
    kata_kunci = entry_kunci.get()
    if not teks_enkripsi or not kata_kunci:
        messagebox.showwarning("Input Error", "Mohon masukkan teks enkripsi dan kata kunci.")
        return
    hasil_dekripsi = vigenere_decrypt(teks_enkripsi, kata_kunci)
    entry_teks.delete("1.0", tk.END) 
    entry_teks.insert(tk.END, hasil_dekripsi)
def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as file:
            teks = entry_teks.get("1.0", tk.END)
            file.write(teks)
def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
    if file_path:
        with open(file_path, 'rb') as file:
            content = file.read()
            try:
                teks = content.decode('utf-8')
                entry_teks.delete("1.0", tk.END) 
                entry_teks.insert(tk.END, teks)  
            except UnicodeDecodeError:
                messagebox.showwarning("File Error", "File tidak dapat dibaca sebagai teks.")
root = tk.Tk()
root.title("Vigenère Cipher")
root.configure(bg='black')  
frame_teks = tk.Frame(root, bg='black')
frame_teks.pack(pady=10)
label_teks = tk.Label(frame_teks, text="Masukkan teks yang ingin dienkripsi:", bg='black', fg='white')  
label_teks.pack()
entry_teks = tk.Text(frame_teks, width=50, height=10)
entry_teks.pack()
button_upload = tk.Button(root, text="Upload Dokumen", command=upload_file)
button_upload.pack(pady=5)
button_save = tk.Button(root, text="Simpan Hasil", command=save_file)
button_save.pack(pady=5)
label_kunci = tk.Label(root, text="Masukkan kata kunci:", bg='black', fg='white')  
label_kunci.pack(pady=5)
entry_kunci = tk.Entry(root, width=50)
entry_kunci.pack(pady=5)
frame_buttons = tk.Frame(root, bg='black')
frame_buttons.pack(pady=5)
button_decrypt = tk.Button(frame_buttons, text="Dekripsi", command=decrypt)
button_decrypt.pack(side=tk.LEFT, padx=(0, 10))
button_encrypt = tk.Button(frame_buttons, text="Enkripsi", command=encrypt)
button_encrypt.pack(side=tk.RIGHT, padx=(10, 0))
label_cipherteks = tk.Label(root, text="", bg='black', fg='white') 
label_cipherteks.pack(pady=5)
root.mainloop()
