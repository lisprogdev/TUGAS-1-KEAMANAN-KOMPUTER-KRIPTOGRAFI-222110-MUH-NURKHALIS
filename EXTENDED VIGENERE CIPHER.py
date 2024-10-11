import tkinter as tk
from tkinter import messagebox, filedialog
def extended_vigenere_encrypt(teks_asli, kata_kunci):
    teks_enkripsi = []
    kata_kunci_diulang = (kata_kunci * (len(teks_asli) // len(kata_kunci) + 1))[:len(teks_asli)]
    for t_char, k_char in zip(teks_asli, kata_kunci_diulang):
        shift = (ord(t_char) + ord(k_char)) % 256
        teks_enkripsi.append(shift)
    return teks_enkripsi
def extended_vigenere_decrypt(teks_enkripsi, kata_kunci):
    teks_dekripsi = ""
    kata_kunci_diulang = (kata_kunci * (len(teks_enkripsi) // len(kata_kunci) + 1))[:len(teks_enkripsi)]
    for e_char, k_char in zip(teks_enkripsi, kata_kunci_diulang):
        shift = (e_char - ord(k_char)) % 256
        teks_dekripsi += chr(shift)
    return teks_dekripsi
def encrypt():
    teks_asli = entry_teks.get("1.0", tk.END).strip()
    kata_kunci = entry_kunci.get()
    if not teks_asli or not kata_kunci:
        messagebox.showwarning("Input Error", "Mohon masukkan teks dan kata kunci.")
        return
    hasil_enkripsi = extended_vigenere_encrypt(teks_asli, kata_kunci)
    entry_teks.delete("1.0", tk.END) 
    entry_teks.insert(tk.END, ', '.join(map(str, hasil_enkripsi)))  
def decrypt():
    teks_enkripsi = entry_teks.get("1.0", tk.END).strip()
    kata_kunci = entry_kunci.get()
    if not teks_enkripsi or not kata_kunci:
        messagebox.showwarning("Input Error", "Mohon masukkan teks enkripsi dan kata kunci.")
        return
    try:
        teks_enkripsi_list = list(map(int, teks_enkripsi.split(', ')))
        hasil_dekripsi = extended_vigenere_decrypt(teks_enkripsi_list, kata_kunci)
        entry_teks.delete("1.0", tk.END) 
        entry_teks.insert(tk.END, hasil_dekripsi)
    except ValueError:
        messagebox.showerror("Input Error", "Format enkripsi tidak valid. Pastikan input numerik dipisahkan dengan koma.")
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
            entry_teks.insert(tk.END, teks.decode(errors='ignore'))  
def encrypt_file():
    file_path = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
    if file_path:
        kata_kunci = entry_kunci.get()
        if not kata_kunci:
            messagebox.showwarning("Input Error", "Mohon masukkan kata kunci.")
            return
        with open(file_path, 'rb') as file:
            data = file.read()
            hasil_enkripsi = extended_vigenere_encrypt(data.decode(errors='ignore'), kata_kunci)
            entry_teks.delete("1.0", tk.END)
            entry_teks.insert(tk.END, ', '.join(map(str, hasil_enkripsi)))
def decrypt_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        kata_kunci = entry_kunci.get()
        if not kata_kunci:
            messagebox.showwarning("Input Error", "Mohon masukkan kata kunci.")
            return
        with open(file_path, 'r', encoding='utf-8') as file:
            teks_enkripsi = file.read().strip()
            try:
                teks_enkripsi_list = list(map(int, teks_enkripsi.split(', ')))
                hasil_dekripsi = extended_vigenere_decrypt(teks_enkripsi_list, kata_kunci)
                entry_teks.delete("1.0", tk.END)
                entry_teks.insert(tk.END, hasil_dekripsi)
            except ValueError:
                messagebox.showerror("Input Error", "Format enkripsi tidak valid. Pastikan input numerik dipisahkan dengan koma.")
root = tk.Tk()
root.title("Extended Vigenère Cipher")
root.configure(bg='black')  
frame_teks = tk.Frame(root, bg='black')
frame_teks.pack(pady=10)
label_teks = tk.Label(frame_teks, text="Masukkan teks yang ingin dienkripsi:", bg='black')
label_teks.pack()
entry_teks = tk.Text(frame_teks, width=50, height=10)
entry_teks.pack()
button_upload = tk.Button(root, text="Upload Dokumen Teks", command=upload_file)
button_upload.pack(pady=5)
button_save = tk.Button(root, text="Simpan Hasil", command=save_file)
button_save.pack(pady=5)
label_kunci = tk.Label(root, text="Masukkan kata kunci:", bg='black')
label_kunci.pack(pady=5)
entry_kunci = tk.Entry(root, width=50)
entry_kunci.pack(pady=5)
frame_buttons = tk.Frame(root, bg='black')
frame_buttons.pack(pady=5)
button_encrypt_numeric = tk.Button(frame_buttons, text="Enkripsi ke Numerik", command=encrypt)
button_encrypt_numeric.pack(side=tk.LEFT, padx=(0, 10))
button_decrypt = tk.Button(frame_buttons, text="Dekripsi", command=decrypt)
button_decrypt.pack(side=tk.LEFT, padx=(0, 10))
button_encrypt_file = tk.Button(frame_buttons, text="Enkripsi File", command=encrypt_file)
button_encrypt_file.pack(side=tk.LEFT, padx=(0, 10))
button_decrypt_file = tk.Button(frame_buttons, text="Dekripsi File", command=decrypt_file)
button_decrypt_file.pack(side=tk.LEFT, padx=(0, 10))
root.mainloop()
