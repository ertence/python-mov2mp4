import os
import ffmpeg
import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import messagebox
import threading

class VideoConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MOV to MP4 Converter")
        self.root.geometry("600x400")
        self.root.configure(padx=20, pady=20)
        
        # Style configuration
        self.style = ttk.Style()
        self.style.configure('Custom.TButton', padding=10)
        self.style.configure('Custom.TFrame', padding=10)
        
        # Main frame
        self.main_frame = ttk.Frame(root, style='Custom.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            self.main_frame, 
            text="MOV to MP4 Converter",
            font=('Helvetica', 16, 'bold')
        )
        title_label.pack(pady=20)
        
        # File selection frame
        self.file_frame = ttk.Frame(self.main_frame)
        self.file_frame.pack(fill=tk.X, pady=10)
        
        self.file_path = tk.StringVar()
        self.file_entry = ttk.Entry(
            self.file_frame, 
            textvariable=self.file_path,
            width=50
        )
        self.file_entry.pack(side=tk.LEFT, padx=5)
        
        self.browse_button = ttk.Button(
            self.file_frame,
            text="Browse",
            command=self.browse_file,
            style='Custom.TButton'
        )
        self.browse_button.pack(side=tk.LEFT, padx=5)
        
        # Progress frame
        self.progress_frame = ttk.Frame(self.main_frame)
        self.progress_frame.pack(fill=tk.X, pady=20)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate'
        )
        self.progress_bar.pack(fill=tk.X)
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to convert")
        self.status_label = ttk.Label(
            self.main_frame,
            textvariable=self.status_var,
            font=('Helvetica', 10)
        )
        self.status_label.pack(pady=10)
        
        # Convert button
        self.convert_button = ttk.Button(
            self.main_frame,
            text="Convert to MP4",
            command=self.start_conversion,
            style='Custom.TButton'
        )
        self.convert_button.pack(pady=20)
        
        # Help text
        help_text = "1. Click 'Browse' to select a .mov file\n2. Click 'Convert to MP4' to start conversion"
        help_label = ttk.Label(
            self.main_frame,
            text=help_text,
            font=('Helvetica', 9),
            justify=tk.LEFT
        )
        help_label.pack(pady=20)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("MOV files", "*.mov"), ("All files", "*.*")]
        )
        if file_path:
            self.file_path.set(file_path)

    def start_conversion(self):
        input_path = self.file_path.get()
        if not input_path:
            messagebox.showerror("Error", "Please select a file first!")
            return
        
        if not input_path.lower().endswith('.mov'):
            messagebox.showerror("Error", "Please select a .mov file!")
            return
        
        self.convert_button.configure(state='disabled')
        self.progress_var.set(0)
        self.status_var.set("Converting...")
        
        # Start conversion in a separate thread
        thread = threading.Thread(target=self.convert_file, args=(input_path,))
        thread.daemon = True
        thread.start()

    def convert_file(self, input_path):
        try:
            filename = os.path.splitext(input_path)[0]
            output_path = f"{filename}.mp4"
            
            # Run the ffmpeg conversion
            stream = ffmpeg.input(input_path)
            stream = ffmpeg.output(stream, output_path, vcodec='libx264', acodec='aac')
            
            # Start conversion
            self.progress_var.set(20)
            ffmpeg.run(stream, overwrite_output=True, capture_stdout=True, capture_stderr=True)
            self.progress_var.set(100)
            
            self.status_var.set("Conversion completed successfully!")
            messagebox.showinfo("Success", f"File converted successfully!\nSaved as: {output_path}")
            
        except ffmpeg.Error as e:
            error_message = f"FFmpeg error:\n{e.stderr.decode('utf8')}"
            self.status_var.set("Conversion failed!")
            messagebox.showerror("Error", error_message)
            
        except Exception as e:
            self.status_var.set("Conversion failed!")
            messagebox.showerror("Error", str(e))
            
        finally:
            self.convert_button.configure(state='normal')
            self.progress_var.set(0)

def convert_mov_to_mp4(input_path):
    """Convert a .mov file to .mp4 format using ffmpeg"""
    try:
        filename = os.path.splitext(input_path)[0]
        output_path = f"{filename}.mp4"
        
        stream = ffmpeg.input(input_path)
        stream = ffmpeg.output(stream, output_path, vcodec='libx264', acodec='aac')
        ffmpeg.run(stream, overwrite_output=True, capture_stdout=True, capture_stderr=True)
        
        print(f"Successfully converted {input_path} to {output_path}")
        return True
    except ffmpeg.Error as e:
        print(f"Error converting {input_path}:")
        print(f"stdout: {e.stdout.decode('utf8')}")
        print(f"stderr: {e.stderr.decode('utf8')}")
        return False
    except Exception as e:
        print(f"Error converting {input_path}: {str(e)}")
        return False

if __name__ == "__main__":
    import sys
    
    # If command line arguments are provided, use CLI mode
    if len(sys.argv) > 1:
        mov_file = sys.argv[1]
        if not os.path.exists(mov_file):
            print(f"Error: File {mov_file} does not exist")
            sys.exit(1)
        
        if not mov_file.lower().endswith('.mov'):
            print("Error: Input file must be a .mov file")
            sys.exit(1)
        
        convert_mov_to_mp4(mov_file)
    # Otherwise, launch GUI
    else:
        root = tk.Tk()
        app = VideoConverterGUI(root)
        root.mainloop()
