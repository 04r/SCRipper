import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import subprocess
import threading
import os
from pathlib import Path

class SoundCloudDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SoundCloud Downloader")
        self.root.geometry("800x800")
        self.root.resizable(True, True)
        
        # Set modern color scheme
        self.bg_color = "#1e1e1e"
        self.fg_color = "#ffffff"
        self.accent_color = "#ff5500"
        self.secondary_bg = "#2d2d2d"
        self.input_bg = "#3d3d3d"
        
        # Configure root window
        self.root.configure(bg=self.bg_color)
        
        # Path to scdl executable
        self.scdl_path = r"C:\Users\kojia\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts\scdl.exe"
        
        # Default download folder
        self.download_folder = str(Path.home() / "Downloads" / "SoundCloud")
        
        # Configure styles
        self.setup_styles()
        
        # Create GUI elements
        self.create_widgets()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors for different widgets
        style.configure("TFrame", background=self.bg_color)
        style.configure("TLabel", background=self.bg_color, foreground=self.fg_color, 
                       font=("Segoe UI", 10))
        style.configure("Title.TLabel", background=self.bg_color, foreground=self.accent_color, 
                       font=("Segoe UI", 24, "bold"))
        style.configure("Subtitle.TLabel", background=self.bg_color, foreground="#aaaaaa", 
                       font=("Segoe UI", 9))
        
        # Entry style
        style.configure("TEntry", fieldbackground=self.input_bg, foreground=self.fg_color,
                       borderwidth=0, relief="flat", insertcolor=self.fg_color)
        style.map("TEntry", 
                 fieldbackground=[("focus", self.input_bg)],
                 bordercolor=[("focus", self.input_bg)],
                 lightcolor=[("focus", self.input_bg)],
                 darkcolor=[("focus", self.input_bg)])
        
        # Button styles
        style.configure("Accent.TButton", background=self.accent_color, foreground="white",
                       borderwidth=0, focuscolor="none", font=("Segoe UI", 11, "bold"),
                       padding=(20, 10))
        style.map("Accent.TButton",
                 background=[("active", "#ff6a1a"), ("pressed", "#cc4400")])
        
        style.configure("TButton", background=self.secondary_bg, foreground=self.fg_color,
                       borderwidth=0, focuscolor="none", font=("Segoe UI", 9),
                       padding=(10, 5))
        style.map("TButton",
                 background=[("active", "#3d3d3d"), ("pressed", "#2d2d2d")])
        
        # Radiobutton style
        style.configure("TRadiobutton", background=self.bg_color, foreground=self.fg_color,
                       font=("Segoe UI", 10), indicatorcolor=self.accent_color)
        style.map("TRadiobutton",
                 background=[("active", self.bg_color)],
                 foreground=[("active", self.accent_color)])
        
        # Checkbutton style
        style.configure("TCheckbutton", background=self.secondary_bg, foreground=self.fg_color,
                       font=("Segoe UI", 10))
        style.map("TCheckbutton",
                 background=[("active", self.secondary_bg)],
                 foreground=[("active", self.accent_color)])
        
        # LabelFrame style
        style.configure("TLabelframe", background=self.bg_color, foreground=self.fg_color,
                       borderwidth=1, relief="solid", bordercolor=self.secondary_bg)
        style.configure("TLabelframe.Label", background=self.bg_color, 
                       foreground=self.accent_color, font=("Segoe UI", 11, "bold"))
        
    def create_widgets(self):
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Header section
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        header_frame.columnconfigure(0, weight=1)
        
        title_label = ttk.Label(header_frame, text="🎵 SoundCloud Downloader", 
                                style="Title.TLabel")
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        subtitle_label = ttk.Label(header_frame, 
                                   text="Download your favorite tracks and playlists", 
                                   style="Subtitle.TLabel")
        subtitle_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        # Download type selection
        type_frame = ttk.LabelFrame(main_frame, text="Download Type", padding="15")
        type_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        type_frame.columnconfigure(1, weight=1)
        
        self.download_type = tk.StringVar(value="track")
        
        track_radio = ttk.Radiobutton(type_frame, text="🎵 Single Track", 
                                     variable=self.download_type, value="track",
                                     command=self.update_url_placeholder)
        track_radio.grid(row=0, column=0, sticky=tk.W, padx=(0, 30), pady=5)
        
        playlist_radio = ttk.Radiobutton(type_frame, text="📀 Playlist/Album", 
                                        variable=self.download_type, value="playlist",
                                        command=self.update_url_placeholder)
        playlist_radio.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        likes_radio = ttk.Radiobutton(type_frame, text="❤️ Likes", 
                                     variable=self.download_type, value="likes",
                                     command=self.update_url_placeholder)
        likes_radio.grid(row=0, column=2, sticky=tk.W, padx=(30, 0), pady=5)
        
        # URL input section
        url_frame = ttk.Frame(main_frame)
        url_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        url_frame.columnconfigure(0, weight=1)
        
        url_label = ttk.Label(url_frame, text="SoundCloud URL")
        url_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # Create a container frame for the entry with custom border
        url_entry_container = tk.Frame(url_frame, bg=self.secondary_bg, bd=1)
        url_entry_container.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.url_entry = ttk.Entry(url_entry_container, font=("Segoe UI", 10))
        self.url_entry.pack(fill=tk.BOTH, expand=True, ipady=8, padx=1, pady=1)
        self.update_url_placeholder()
        
        # Download folder section
        folder_frame = ttk.Frame(main_frame)
        folder_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        folder_frame.columnconfigure(0, weight=1)
        
        folder_label = ttk.Label(folder_frame, text="Download Folder")
        folder_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        folder_input_frame = ttk.Frame(folder_frame)
        folder_input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        folder_input_frame.columnconfigure(0, weight=1)
        
        # Create a container frame for the folder entry with custom border
        folder_entry_container = tk.Frame(folder_input_frame, bg=self.secondary_bg, bd=1)
        folder_entry_container.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        folder_entry_container.columnconfigure(0, weight=1)
        
        self.folder_entry = ttk.Entry(folder_entry_container, font=("Segoe UI", 10))
        self.folder_entry.insert(0, self.download_folder)
        self.folder_entry.pack(fill=tk.BOTH, expand=True, ipady=8, padx=1, pady=1)
        
        browse_btn = ttk.Button(folder_input_frame, text="📁 Browse", 
                               command=self.browse_folder)
        browse_btn.grid(row=0, column=1)
        
        # Options section
        options_frame = ttk.LabelFrame(main_frame, text="Download Options", padding="15")
        options_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        options_frame.columnconfigure(0, weight=1)
        options_frame.columnconfigure(1, weight=1)
        
        # Create a grid for checkboxes
        self.mp3_only_var = tk.BooleanVar(value=True)
        mp3_check = ttk.Checkbutton(options_frame, text="Convert to MP3", 
                                    variable=self.mp3_only_var)
        mp3_check.grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        
        self.continue_var = tk.BooleanVar(value=True)
        continue_check = ttk.Checkbutton(options_frame, 
                                        text="Continue on error", 
                                        variable=self.continue_var)
        continue_check.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        
        self.force_var = tk.BooleanVar(value=True)
        force_check = ttk.Checkbutton(options_frame, 
                                     text="Overwrite existing files", 
                                     variable=self.force_var)
        force_check.grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        
        self.metadata_var = tk.BooleanVar(value=True)
        metadata_check = ttk.Checkbutton(options_frame, 
                                        text="Add metadata tags", 
                                        variable=self.metadata_var)
        metadata_check.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Download button
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, pady=(10, 15))
        
        self.download_btn = ttk.Button(button_frame, text="⬇ Download", 
                                       style="Accent.TButton",
                                       command=self.start_download)
        self.download_btn.pack()
        
        # Output section
        output_label = ttk.Label(main_frame, text="Output Log")
        output_label.grid(row=6, column=0, sticky=tk.W, pady=(0, 5))
        
        # Create a frame for the text widget with custom styling
        output_container = tk.Frame(main_frame, bg=self.input_bg, relief="flat", bd=0)
        output_container.grid(row=7, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.output_text = scrolledtext.ScrolledText(
            output_container, 
            height=18, 
            wrap=tk.WORD,
            bg=self.input_bg,
            fg=self.fg_color,
            font=("Consolas", 9),
            relief="flat",
            borderwidth=10,
            state='disabled'
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for colored output
        self.output_text.tag_config("error", foreground="#ff4444")
        self.output_text.tag_config("success", foreground="#44ff44")
        self.output_text.tag_config("info", foreground="#4488ff")
        self.output_text.tag_config("warning", foreground="#ffaa00")
        
        # Make the output text expandable
        main_frame.rowconfigure(7, weight=1)
        
        # Bottom button frame
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=8, column=0, pady=(5, 0))
        
        self.open_folder_btn = ttk.Button(bottom_frame, text="📂 Open Download Folder", 
                                          command=self.open_download_folder)
        self.open_folder_btn.pack()
        
    def update_url_placeholder(self):
        # Clear current text
        current_text = self.url_entry.get()
        if current_text.startswith("e.g."):
            self.url_entry.delete(0, tk.END)
        
        # Set placeholder based on download type
        download_type = self.download_type.get()
        if download_type == "track":
            placeholder = "e.g. https://soundcloud.com/artist/track-name"
        elif download_type == "playlist":
            placeholder = "e.g. https://soundcloud.com/artist/sets/playlist-name"
        else:  # likes
            placeholder = "e.g. https://soundcloud.com/username/likes"
        
        # Only set placeholder if field is empty
        if not self.url_entry.get():
            self.url_entry.insert(0, placeholder)
            self.url_entry.config(foreground="#888888")
        
        # Bind events for placeholder behavior
        self.url_entry.bind("<FocusIn>", self.on_entry_focus_in)
        self.url_entry.bind("<FocusOut>", self.on_entry_focus_out)
    
    def on_entry_focus_in(self, event):
        if self.url_entry.get().startswith("e.g."):
            self.url_entry.delete(0, tk.END)
            self.url_entry.config(foreground=self.fg_color)
    
    def on_entry_focus_out(self, event):
        if not self.url_entry.get():
            self.update_url_placeholder()
    
    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.folder_entry.get())
        if folder:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)
            self.download_folder = folder
    
    def append_output(self, text, tag=None):
        self.output_text.config(state='normal')
        if tag:
            self.output_text.insert(tk.END, text + "\n", tag)
        else:
            self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)
        self.output_text.config(state='disabled')
        self.root.update_idletasks()
    
    def start_download(self):
        url = self.url_entry.get().strip()
        
        # Check if URL is valid (not placeholder)
        if not url or url.startswith("e.g."):
            messagebox.showwarning("Warning", "Please enter a valid SoundCloud URL!")
            return
        
        # Disable download button during download
        self.download_btn.config(state='disabled', text="⏳ Downloading...")
        
        # Clear output
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state='disabled')
        
        # Start download in a separate thread
        thread = threading.Thread(target=self.download_track, args=(url,))
        thread.daemon = True
        thread.start()
    
    def download_track(self, url):
        try:
            # Build command based on download type
            download_type = self.download_type.get()
            
            if download_type == "track":
                cmd = [self.scdl_path, "-l", url]
            elif download_type == "playlist":
                cmd = [self.scdl_path, "-l", url]
            else:  # likes
                cmd = [self.scdl_path, "-l", url]
            
            # Add options
            if self.mp3_only_var.get():
                cmd.append("--onlymp3")
            if self.continue_var.get():
                cmd.append("-c")
            if self.force_var.get():
                cmd.append("-f")
            
            # Add name format to avoid numbered naming (01, 02, etc.)
            # scdl uses {uploader} for artist name and {title} for track title
            cmd.extend(["--name-format", "{uploader} - {title}"])
            
            # Add download path
            download_path = self.folder_entry.get().strip()
            if download_path:
                # Create folder if it doesn't exist
                os.makedirs(download_path, exist_ok=True)
                cmd.extend(["--path", download_path])
            
            self.append_output("=" * 70, "info")
            type_emoji = "🎵" if download_type == "track" else "📀" if download_type == "playlist" else "❤️"
            self.append_output(f"{type_emoji} Starting download ({download_type})...", "info")
            self.append_output(f"Command: {' '.join(cmd)}", "info")
            self.append_output("=" * 70, "info")
            self.append_output("")
            
            # Run the command
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Read output line by line
            for line in process.stdout:
                line = line.strip()
                if line:
                    # Color code based on content
                    if "error" in line.lower() or "failed" in line.lower():
                        self.append_output(f"❌ {line}", "error")
                    elif "warning" in line.lower():
                        self.append_output(f"⚠️ {line}", "warning")
                    elif "downloaded" in line.lower() or "complete" in line.lower():
                        self.append_output(f"✅ {line}", "success")
                    elif "downloading" in line.lower():
                        self.append_output(f"⬇️ {line}", "info")
                    else:
                        self.append_output(line)
            
            process.wait()
            
            self.append_output("")
            self.append_output("=" * 70, "info")
            if process.returncode == 0:
                self.append_output("✅ Download completed successfully!", "success")
            else:
                self.append_output(f"❌ Process exited with code {process.returncode}", "error")
            self.append_output("=" * 70, "info")
                
        except FileNotFoundError:
            self.append_output("❌ Error: scdl.exe not found!", "error")
            self.append_output(f"Please verify the path: {self.scdl_path}", "error")
        except Exception as e:
            self.append_output(f"❌ Error: {str(e)}", "error")
        finally:
            # Re-enable download button
            self.download_btn.config(state='normal', text="⬇ Download")
    
    def open_download_folder(self):
        folder = self.folder_entry.get().strip()
        if os.path.exists(folder):
            os.startfile(folder)
        else:
            messagebox.showwarning("Warning", "Download folder does not exist!")

def main():
    root = tk.Tk()
    app = SoundCloudDownloaderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()