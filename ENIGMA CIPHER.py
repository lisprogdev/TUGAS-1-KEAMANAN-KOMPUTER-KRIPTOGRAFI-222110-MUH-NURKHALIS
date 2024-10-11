import tkinter as tk
from tkinter import messagebox, filedialog
class Rotor:
    def __init__(self, mapping):
        self.mapping = mapping
        self.position = 0
    def set_position(self, position):
        self.position = position % len(self.mapping)
    def rotate(self):
        self.position = (self.position + 1) % len(self.mapping)
    def encode(self, char):
        index = (ord(char) - ord('A') + self.position) % 26
        return self.mapping[index]
    def decode(self, char):
        index = self.mapping.index(char)
        return chr((index - self.position) % 26 + ord('A'))
rotor1 = Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ')
rotor2 = Rotor('AJDKSIRUXBLHWTMCQGZNPYFVOE')
rotor3 = Rotor('BDFHJLCPRTXVZNYEIWGAKMUSQO')
original_text = ""
def set_rotor_positions(key):
    positions = [ord(char) - ord('A') for char in key.upper()]
    rotor1.set_position(positions[0])
    rotor2.set_position(positions[1] if len(positions) > 1 else positions[0])
    rotor3.set_position(positions[2] if len(positions) > 2 else positions[0])
def format_ciphertext(ciphertext, group_size=5):
    return ' '.join([ciphertext[i:i+group_size] for i in range(0, len(ciphertext), group_size)])
def enigma_encrypt(teks_asli, key):
    set_rotor_positions(key)
    result = []
    for char in teks_asli.upper():
        if char.isalpha():
            rotor1.rotate()
            rotor2.rotate()
            rotor3.rotate()
            encoded_char = rotor3.encode(rotor2.encode(rotor1.encode(char)))
            result.append(encoded_char)
        else:
            result.append(char)
    return ''.join(result)
def enigma_decrypt(teks_enkripsi, key):
    set_rotor_positions(key)
    result = []
    initial_positions = (rotor1.position, rotor2.position, rotor3.position)
    for char in teks_enkripsi.upper():
        if char.isalpha():
            decoded_char = rotor1.decode(rotor2.decode(rotor3.decode(char)))
            result.append(decoded_char)
            rotor1.rotate()
            rotor2.rotate()
            rotor3.rotate()
        else:
            result.append(char)
    rotor1.position, rotor2.position, rotor3.position = initial_positions
    return ''.join(result)
def encrypt():
    global original_text
    teks_asli = entry_teks.get("1.0", tk.END).strip()
    key = entry_key.get().strip()
    if not teks_asli:
        messagebox.showwarning("Input Error", "Mohon masukkan teks.")
        return
    if not key:
        messagebox.showwarning("Input Error", "Mohon masukkan kunci.")
        return
    original_text = teks_asli
    hasil_enkripsi = enigma_encrypt(teks_asli, key)
    if var_format.get() == 1:
        hasil_enkripsi = format_ciphertext(hasil_enkripsi)
    entry_teks.delete("1.0", tk.END)
    entry_teks.insert(tk.END, hasil_enkripsi)
def decrypt():
    teks_enkripsi = entry_teks.get("1.0", tk.END).strip()
    key = entry_key.get().strip()
    if not teks_enkripsi:
        messagebox.showwarning("Input Error", "Mohon masukkan teks enkripsi.")
        return
    if not key:
        messagebox.showwarning("Input Error", "Mohon masukkan kunci.")
        return
    hasil_dekripsi = enigma_decrypt(teks_enkripsi, key)
    entry_teks.delete("1.0", tk.END)
    entry_teks.insert(tk.END, original_text)
def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as file:
            teks = entry_teks.get("1.0", tk.END)
            file.write(teks)
def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            teks = file.read()
            entry_teks.delete("1.0", tk.END)
            entry_teks.insert(tk.END, teks)
root = tk.Tk()
root.title("Cipher Enigma")
root.configure(bg='black')
frame_teks = tk.Frame(root, bg='black')
frame_teks.pack(pady=10)
label_teks = tk.Label(frame_teks, text="Masukkan teks yang ingin dienkripsi:", bg='black')
label_teks.pack()
entry_teks = tk.Text(frame_teks, width=50, height=10)
entry_teks.pack()
frame_key = tk.Frame(root, bg='black')
frame_key.pack(pady=5)
label_key = tk.Label(frame_key, text="Masukkan Kunci:", bg='black')
label_key.pack(side=tk.LEFT)
entry_key = tk.Entry(frame_key)
entry_key.pack(side=tk.LEFT, padx=5)
button_upload = tk.Button(root, text="Upload Dokumen Teks", command=upload_file)
button_upload.pack(pady=5)
button_save = tk.Button(root, text="Simpan Hasil", command=save_file)
button_save.pack(pady=5)
var_format = tk.IntVar()
check_format = tk.Checkbutton(root, text="Format cipherteks 5-huruf", variable=var_format, bg='black')
check_format.pack(pady=5)
frame_buttons = tk.Frame(root, bg='black')
frame_buttons.pack(pady=5)
button_decrypt = tk.Button(frame_buttons, text="Dekripsi", command=decrypt)
button_decrypt.pack(side=tk.LEFT, padx=(0, 10))
button_encrypt = tk.Button(frame_buttons, text="Enkripsi", command=encrypt)
button_encrypt.pack(side=tk.RIGHT, padx=(10, 0))
root.mainloop()
