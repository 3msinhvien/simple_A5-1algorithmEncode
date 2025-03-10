import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from a5_1_core import A5_1, process_audio_file

class A5_1_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("A5/1 Audio Encryption/Decryption Tool")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        
        # Set application icon if available
        try:
            self.root.iconbitmap("lock_icon.ico")
        except:
            pass
        
        # Variables
        self.input_file_path = tk.StringVar()
        self.output_file_path = tk.StringVar()
        self.key_var = tk.StringVar()
        self.mode_var = tk.StringVar(value="encrypt")
        self.key_option_var = tk.StringVar(value="auto")
        self.status_var = tk.StringVar(value="Ready")
        
        # Create the main frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create and place widgets
        self.create_widgets()
        
        # Configure style
        self.configure_style()
    
    def configure_style(self):
        """Configure the style of the application"""
        style = ttk.Style()
        
        # Configure TButton
        style.configure("TButton", font=("Arial", 10), padding=5)
        
        # Configure TLabel
        style.configure("TLabel", font=("Arial", 10))
        
        # Configure Title
        style.configure("Title.TLabel", font=("Arial", 14, "bold"))
        
        # Configure Status
        style.configure("Status.TLabel", font=("Arial", 10, "italic"))
    
    def create_widgets(self):
        """Create all widgets for the GUI"""
        # Title
        title_label = ttk.Label(
            self.main_frame, 
            text="A5/1 Audio Encryption/Decryption Tool", 
            style="Title.TLabel"
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Input file section
        input_label = ttk.Label(self.main_frame, text="Input Audio File (.wav):")
        input_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        input_entry = ttk.Entry(self.main_frame, textvariable=self.input_file_path, width=50)
        input_entry.grid(row=1, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        input_button = ttk.Button(self.main_frame, text="Browse...", command=self.browse_input_file)
        input_button.grid(row=1, column=2, sticky=tk.W, pady=5)
        
        # Output file section
        output_label = ttk.Label(self.main_frame, text="Output Audio File:")
        output_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        output_entry = ttk.Entry(self.main_frame, textvariable=self.output_file_path, width=50)
        output_entry.grid(row=2, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        output_button = ttk.Button(self.main_frame, text="Browse...", command=self.browse_output_file)
        output_button.grid(row=2, column=2, sticky=tk.W, pady=5)
        
        # Mode selection
        mode_label = ttk.Label(self.main_frame, text="Operation Mode:")
        mode_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        
        mode_frame = ttk.Frame(self.main_frame)
        mode_frame.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        encrypt_radio = ttk.Radiobutton(
            mode_frame, 
            text="Encrypt", 
            variable=self.mode_var, 
            value="encrypt",
            command=self.update_output_filename
        )
        encrypt_radio.pack(side=tk.LEFT, padx=(0, 10))
        
        decrypt_radio = ttk.Radiobutton(
            mode_frame, 
            text="Decrypt", 
            variable=self.mode_var, 
            value="decrypt",
            command=self.update_output_filename
        )
        decrypt_radio.pack(side=tk.LEFT)
        
        # Key options
        key_option_label = ttk.Label(self.main_frame, text="Key Option:")
        key_option_label.grid(row=4, column=0, sticky=tk.W, pady=5)
        
        key_option_frame = ttk.Frame(self.main_frame)
        key_option_frame.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        auto_radio = ttk.Radiobutton(
            key_option_frame, 
            text="Generate Automatically", 
            variable=self.key_option_var, 
            value="auto",
            command=self.toggle_key_entry
        )
        auto_radio.pack(side=tk.LEFT, padx=(0, 10))
        
        manual_radio = ttk.Radiobutton(
            key_option_frame, 
            text="Enter Manually", 
            variable=self.key_option_var, 
            value="manual",
            command=self.toggle_key_entry
        )
        manual_radio.pack(side=tk.LEFT)
        
        # Key entry
        key_label = ttk.Label(self.main_frame, text="Key (16 hex chars):")
        key_label.grid(row=5, column=0, sticky=tk.W, pady=5)
        
        self.key_entry = ttk.Entry(self.main_frame, textvariable=self.key_var, width=50, state="disabled")
        self.key_entry.grid(row=5, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        self.generate_key_button = ttk.Button(
            self.main_frame, 
            text="Generate", 
            command=self.generate_key
        )
        self.generate_key_button.grid(row=5, column=2, sticky=tk.W, pady=5)
        
        # Execute button
        execute_button = ttk.Button(
            self.main_frame, 
            text="Execute", 
            command=self.execute_operation,
            style="TButton"
        )
        execute_button.grid(row=6, column=0, columnspan=3, pady=20)
        
        # Status bar
        status_frame = ttk.Frame(self.main_frame)
        status_frame.grid(row=7, column=0, columnspan=3, sticky=tk.W+tk.E, pady=(10, 0))
        
        status_label = ttk.Label(status_frame, text="Status:", anchor=tk.W)
        status_label.pack(side=tk.LEFT, padx=(0, 5))
        
        status_value = ttk.Label(status_frame, textvariable=self.status_var, style="Status.TLabel", anchor=tk.W)
        status_value.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Result text area
        result_label = ttk.Label(self.main_frame, text="Results:")
        result_label.grid(row=8, column=0, sticky=tk.NW, pady=(10, 5))
        
        self.result_text = tk.Text(self.main_frame, height=8, width=60, wrap=tk.WORD)
        self.result_text.grid(row=9, column=0, columnspan=3, sticky=tk.W+tk.E+tk.N+tk.S, pady=(0, 10))
        
        # Add scrollbar to result text
        result_scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        result_scrollbar.grid(row=9, column=3, sticky=tk.N+tk.S)
        self.result_text.config(yscrollcommand=result_scrollbar.set)
        
        # Configure grid weights
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(9, weight=1)
    
    def toggle_key_entry(self):
        """Toggle the key entry field based on the key option"""
        if self.key_option_var.get() == "auto":
            self.key_entry.config(state="disabled")
            self.generate_key_button.config(state="normal")
        else:
            self.key_entry.config(state="normal")
            self.generate_key_button.config(state="disabled")
    
    def browse_input_file(self):
        """Open file dialog to select input file"""
        file_path = filedialog.askopenfilename(
            title="Select Input Audio File",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )
        if file_path:
            self.input_file_path.set(file_path)
            
            # Auto-suggest output file name
            if not self.output_file_path.get():
                self.update_output_filename()
    
    def update_output_filename(self):
        """Update output filename when mode changes or input file changes"""
        input_file = self.input_file_path.get()
        if input_file:
            input_name = os.path.basename(input_file)
            input_base = os.path.splitext(input_name)[0]
            mode = self.mode_var.get()
            
            # Set appropriate suffix based on mode
            if mode == "encrypt":
                # If the input filename contains "_decrypted", remove it
                if "_decrypted" in input_base:
                    input_base = input_base.replace("_decrypted", "")
                output_name = f"{input_base}_encrypted.wav"
            else:  # decrypt
                # If the input filename contains "_encrypted", remove it
                if "_encrypted" in input_base:
                    input_base = input_base.replace("_encrypted", "")
                output_name = f"{input_base}_decrypted.wav"
                
            output_dir = os.path.dirname(input_file)
            self.output_file_path.set(os.path.join(output_dir, output_name))
    
    def browse_output_file(self):
        """Open file dialog to select output file"""
        file_path = filedialog.asksaveasfilename(
            title="Save Output Audio File",
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )
        if file_path:
            self.output_file_path.set(file_path)
    
    def generate_key(self):
        """Generate a random key and display it"""
        cipher = A5_1()
        key_str = cipher.get_key_as_string()
        self.key_var.set(key_str)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Generated key: {key_str}\n")
        self.result_text.insert(tk.END, "IMPORTANT: Save this key for decryption later!\n")
    
    def execute_operation(self):
        """Execute the encryption/decryption operation"""
        # Validate input
        input_file = self.input_file_path.get()
        output_file = self.output_file_path.get()
        mode = self.mode_var.get()
        
        if not input_file:
            messagebox.showerror("Error", "Please select an input file.")
            return
        
        if not output_file:
            messagebox.showerror("Error", "Please specify an output file.")
            return
        
        if not os.path.exists(input_file):
            messagebox.showerror("Error", "Input file does not exist.")
            return
        
        if not input_file.lower().endswith('.wav'):
            messagebox.showerror("Error", "Input file must be a .wav file.")
            return
        
        # Create cipher with key
        try:
            cipher = A5_1()
            
            if self.key_option_var.get() == "manual":
                key_str = self.key_var.get()
                if not key_str:
                    messagebox.showerror("Error", "Please enter a key.")
                    return
                cipher.set_key_from_string(key_str)
            else:
                # If auto but no key generated yet
                if not self.key_var.get():
                    self.generate_key()
                cipher.set_key_from_string(self.key_var.get())
            
            # Update status
            self.status_var.set(f"Processing... ({mode})")
            self.root.update_idletasks()
            
            # Process the file
            success, message = process_audio_file(input_file, output_file, cipher, mode)
            
            # Update result
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, message + "\n")
            
            if success:
                self.result_text.insert(tk.END, f"Key used: {cipher.get_key_as_string()}\n")
                if mode == "encrypt":
                    self.result_text.insert(tk.END, "IMPORTANT: Save this key for decryption later!\n")
                self.status_var.set("Completed successfully")
                messagebox.showinfo("Success", f"File {mode}ed successfully!")
            else:
                self.status_var.set("Failed")
                messagebox.showerror("Error", message)
            
        except Exception as e:
            self.status_var.set("Error")
            error_message = f"An error occurred: {str(e)}"
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, error_message)
            messagebox.showerror("Error", error_message)

def main():
    root = tk.Tk()
    app = A5_1_GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()