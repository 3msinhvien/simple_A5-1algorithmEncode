import tkinter as tk
from tkinter import filedialog, messagebox
from core import a5_1_encrypt_decrypt  # Import từ core.py

class AudioEncryptDecryptApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Encrypt/Decrypt with A5/1 Algorithm")
        self.root.geometry("400x400")  # Thiết lập kích thước cửa sổ

        # Các phần tử giao diện
        self.input_file = None
        self.key = tk.StringVar()
        self.output_filename = tk.StringVar()

        # Thiết lập font chữ
        self.font = ('Arial', 12)

        # Tạo Frame để căn chỉnh giao diện
        self.frame = tk.Frame(root)
        self.frame.pack(padx=20, pady=20)

        # Label và Entry cho file đầu vào
        self.input_label = tk.Label(self.frame, text="Chọn file âm thanh:", font=self.font)
        self.input_label.grid(row=0, column=0, sticky="w", pady=5)
        self.input_button = tk.Button(self.frame, text="Chọn File", command=self.select_input_file, font=self.font)
        self.input_button.grid(row=0, column=1, pady=5)

        # Label và Entry cho key
        self.key_label = tk.Label(self.frame, text="Nhập key:", font=self.font)
        self.key_label.grid(row=1, column=0, sticky="w", pady=5)
        self.key_entry = tk.Entry(self.frame, textvariable=self.key, font=self.font)
        self.key_entry.grid(row=1, column=1, pady=5)

        # Label và Entry cho tên file xuất
        self.output_label = tk.Label(self.frame, text="Nhập tên file xuất:", font=self.font)
        self.output_label.grid(row=2, column=0, sticky="w", pady=5)
        self.output_entry = tk.Entry(self.frame, textvariable=self.output_filename, font=self.font)
        self.output_entry.grid(row=2, column=1, pady=5)

        # Các nút để mã hóa và giải mã
        self.encrypt_button = tk.Button(self.frame, text="Mã hoá", command=self.encrypt_audio, font=self.font)
        self.encrypt_button.grid(row=3, column=0, pady=10, padx=10, sticky="ew")

        self.decrypt_button = tk.Button(self.frame, text="Giải mã", command=self.decrypt_audio, font=self.font)
        self.decrypt_button.grid(row=3, column=1, pady=10, padx=10, sticky="ew")

    def select_input_file(self):
        self.input_file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3 *.ogg")])
        if not self.input_file:
            messagebox.showerror("Error", "Vui lòng chọn file âm thanh.")
    
    def save_output_file(self, audio):
        output_file = self.output_filename.get()
        if not output_file:
            messagebox.showerror("Error", "Vui lòng nhập tên file xuất.")
            return
        if not output_file.endswith(".wav"):
            output_file += ".wav"
        audio.export(output_file, format="wav")
        messagebox.showinfo("Success", f"File đã được lưu thành công: {output_file}")

    def encrypt_audio(self):
        if not self.input_file or not self.key.get():
            messagebox.showerror("Error", "Vui lòng nhập đầy đủ thông tin.")
            return
        try:
            encrypted_audio = a5_1_encrypt_decrypt(self.input_file, self.key.get(), encrypt=True)
            self.save_output_file(encrypted_audio)
        except Exception as e:
            messagebox.showerror("Error", f"Đã xảy ra lỗi: {e}")
    
    def decrypt_audio(self):
        if not self.input_file or not self.key.get():
            messagebox.showerror("Error", "Vui lòng nhập đầy đủ thông tin.")
            return
        try:
            decrypted_audio = a5_1_encrypt_decrypt(self.input_file, self.key.get(), encrypt=False)
            self.save_output_file(decrypted_audio)
        except Exception as e:
            messagebox.showerror("Error", f"Đã xảy ra lỗi: {e}")

# Khởi tạo và chạy giao diện
def run_gui():
    root = tk.Tk()
    app = AudioEncryptDecryptApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()
