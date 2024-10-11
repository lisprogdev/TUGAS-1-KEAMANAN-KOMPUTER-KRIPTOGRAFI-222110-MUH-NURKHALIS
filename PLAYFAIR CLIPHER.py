import tkinter as tk
from tkinter import messagebox, filedialog
def create_playfair_table(kunci):
    kunci = kunci.upper().replace('J', 'I')  
    seen = set()
    table = []
    for char in kunci:
        if char not in seen and char.isalpha():
            seen.add(char)
            table.append(char)
    for char in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
        if char not in seen:
            seen.add(char)
            table.append(char)
    return [table[i:i + 5] for i in range(0, 25, 5)]  
def find_position(char, table):
    for i, row in enumerate(table):
        if char in row:
            return i, row.index(char)
    return None
def playfair_encrypt(teks_asli, kunci):
    table = create_playfair_table(kunci)
    teks_asli = teks_asli.upper().replace('J', 'I')
    pairs = []
    i = 0
    while i < len(teks_asli):
        char1 = teks_asli[i]
        if i + 1 < len(teks_asli):
            char2 = teks_asli[i + 1]
            if char1 == char2:
                pairs.append((char1, 'X'))  
                i += 1
            else:
                pairs.append((char1, char2))
                i += 2
        else:
            pairs.append((char1, 'X'))  
            i += 1
    enkripsi = ''
    for char1, char2 in pairs:
        row1, col1 = find_position(char1, table)
        row2, col2 = find_position(char2, table)
        if row1 == row2:  
            enkripsi += table[row1][(col1 + 1) % 5]
            enkripsi += table[row2][(col2 + 1) % 5]
        elif col1 == col2:  
            enkripsi += table[(row1 + 1) % 5][col1]
            enkripsi += table[(row2 + 1) % 5][col2]
        else:  
            enkripsi += table[row1][col2]
            enkripsi += table[row2][col1]
    return enkripsi
def playfair_decrypt(teks_enkripsi, kunci):
    table = create_playfair_table(kunci)
    dekripsi = ''
    pairs = []
    i = 0
    while i < len(teks_enkripsi):
        pairs.append((teks_enkripsi[i], teks_enkripsi[i + 1]))
        i += 2
    for char1, char2 in pairs:
        row1, col1 = find_position(char1, table)
        row2, col2 = find_position(char2, table)
        if row1 == row2:  
            dekripsi += table[row1][(col1 - 1) % 5]
            dekripsi += table[row2][(col2 - 1) % 5]
        elif col1 == col2:  
            dekripsi += table[(row1 - 1) % 5][col1]
            dekripsi += table[(row2 - 1) % 5][col2]
        else:  
            dekripsi += table[row1][col2]
            dekripsi += table[row2][col1]
    return dekripsi
def encrypt():
    teks_asli = entry_teks.get("1.0", tk.END).strip()
    kata_kunci = entry_kunci.get()
    if not teks_asli or not kata_kunci:
        messagebox.showwarning("Input Error", "Mohon masukkan teks dan kata kunci.")
        return
    hasil_enkripsi = playfair_encrypt(teks_asli, kata_kunci)
    entry_teks.delete("1.0", tk.END) 
    entry_teks.insert(tk.END, hasil_enkripsi) 
def decrypt():
    teks_enkripsi = entry_teks.get("1.0", tk.END).strip()
    kata_kunci = entry_kunci.get()
    if not teks_enkripsi or not kata_kunci:
        messagebox.showwarning("Input Error", "Mohon masukkan teks enkripsi dan kata kunci.")
        return
    hasil_dekripsi = playfair_decrypt(teks_enkripsi, kata_kunci)
    entry_teks.delete("1.0", tk.END) 
    entry_teks.insert(tk.END, hasil_dekripsi)
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
            try:
                teks = teks.decode('utf-8')
                entry_teks.delete("1.0", tk.END) 
                entry_teks.insert(tk.END, teks)
            except UnicodeDecodeError:
                messagebox.showwarning("File Error", "File tidak dapat dibaca sebagai teks.")
def display_ciphertext_with_spaces(ciphertext):
    return ' '.join([ciphertext[i:i + 5] for i in range(0, len(ciphertext), 5)])
def show_ciphertext_options():
    ciphertext = entry_teks.get("1.0", tk.END).strip()
    if not ciphertext:
        messagebox.showwarning("Input Error", "Tidak ada cipherteks untuk ditampilkan.")
        return
    options = f"Ciphertext tanpa spasi: {ciphertext}\n\n"
    options += f"Ciphertext dengan kelompok 5-huruf:\n{display_ciphertext_with_spaces(ciphertext)}"
    messagebox.showinfo("Ciphertext Options", options)
root = tk.Tk()
root.title("Playfair Cipher")
root.configure(bg='black')  
frame_teks = tk.Frame(root, bg='black')
frame_teks.pack(pady=10)
label_teks = tk.Label(frame_teks, text="Masukkan teks yang ingin dienkripsi:", bg='black')
label_teks.pack()
entry_teks = tk.Text(frame_teks, width=50, height=10)
entry_teks.pack()
button_upload = tk.Button(root, text="Upload Dokumen", command=upload_file)
button_upload.pack(pady=5)
button_save = tk.Button(root, text="Simpan Hasil", command=save_file)
button_save.pack(pady=5)
button_show_ciphertext = tk.Button(root, text="Tampilkan Ciphertext", command=show_ciphertext_options)
button_show_ciphertext.pack(pady=5)
label_kunci = tk.Label(root, text="Masukkan kata kunci:", bg='black')
label_kunci.pack(pady=5)
entry_kunci = tk.Entry(root, width=50)
entry_kunci.pack(pady=5)
frame_buttons = tk.Frame(root, bg='black')
frame_buttons.pack(pady=5)
button_decrypt = tk.Button(frame_buttons, text="Dekripsi", command=decrypt)
button_decrypt.pack(side=tk.LEFT, padx=(0, 10))
button_encrypt = tk.Button(frame_buttons, text="Enkripsi", command=encrypt)
button_encrypt.pack(side=tk.RIGHT, padx=(10, 0))
root.mainloop()
