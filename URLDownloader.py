import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import filedialog, ttk
import requests
import os
import threading
import webbrowser
from PIL import Image, ImageTk

def check_for_update():
    try:
        response = requests.get('https://raw.githubusercontent.com/MooManisLoud/URL-Downloader/main/version.txt')
        latest_version = response.text.strip()
        current_version = 'v0.4'

        if latest_version != current_version:
            if messagebox.askyesno("URL Downloader", "An update is available. Do you want to download it?"):
                webbrowser.open("https://raw.githubusercontent.com/MooManisLoud/URL-Downloader/main/URLDownloader.py")
            else:
                if messagebox.askyesno("URL Downloader", "Are you sure? Not updating can cause issues. Do you want to continue?"):
                    pass
                else:
                    pass

    except requests.exceptions.RequestException as e:
        messagebox.showerror("URL Downloader", "Failed to check for updates. Error: " + str(e))


def choose_download_path():
    download_path = filedialog.askdirectory()
    entry_path.delete(0, tk.END)
    entry_path.insert(tk.END, download_path)

def choose_download_path():
    download_path = filedialog.askdirectory()
    entry_path.delete(0, tk.END)
    entry_path.insert(tk.END, download_path)


def download_file():
    url = entry_url.get()
    download_path = entry_path.get()

    try:
        response = requests.head(url)
        file_size = int(response.headers.get('content-length', 0))

        threshold = 100 * 1024 * 1024
        if file_size > threshold:
            confirm = messagebox.askyesno(
                "URL Downloader",
                "WARNING!\n\nDownloading large file sizes could make URLD unresponsive or crash.\n\nDo you want to continue?"
            )
            if not confirm:
                return
            
        update_thread = threading.Thread(target=check_for_update)
        update_thread.start()    

        download_window = tk.Toplevel(window)
        download_window.title("Download Progress")

        progress_label = tk.Label(download_window, text="Download Progress:")
        progress_label.pack()

        speed_label = tk.Label(download_window, text="Download Speed: ")
        speed_label.pack()

        file_label = tk.Label(download_window, text="File Name: ")
        file_label.pack()

        url_label = tk.Label(download_window, text="URL: ")
        url_label.pack()

        progress_bar = ttk.Progressbar(download_window, length=300, mode='determinate')
        progress_bar.pack()

        def update_progress(count, total, speed):
            progress = int(count / total * 100)
            progress_bar['value'] = progress

            speed_label.config(text=f"Download Speed: {speed} kB/s")

        def download():
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()

                file_name = url.split("/")[-1]
                file_path = os.path.join(download_path, file_name)

                total_size = int(response.headers.get('content-length', 0))
                block_size = 8192

                with open(file_path, 'wb') as file:
                    count = 0
                    for data in response.iter_content(block_size):
                        file.write(data)
                        count += len(data)
                        speed = count // 1024 // 1 

                        if count % (100 * 1024) == 0:
                            download_window.after(10, update_progress, count, total_size, speed)

                messagebox.showinfo("URL Downloader", f"Download completed!\nSaved at: {file_path}")

            except requests.exceptions.RequestException as e:
                messagebox.showerror("URL Downloader", "URLD has encountered an error:\n" + str(e))

            finally:
                download_window.destroy()

        download_thread = threading.Thread(target=download)
        download_thread.start()

    except Exception as e:
        messagebox.showerror("URL Downloader", "URLD has encountered an error:\n" + str(e))


def reset_fields():
    entry_url.delete(0, tk.END)
    entry_path.delete(0, tk.END)

window = tk.Tk()
window.title("URL Downloader")
window.iconbitmap("icons/main.ico")

window_width = 402
window_height = 299
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

url_label = tk.Label(window, text="Enter URL:")
url_label.pack()

entry_url = tk.Entry(window, width=50)
entry_url.pack()

path_label = tk.Label(window, text="Download Path:")
path_label.pack()

entry_path = tk.Entry(window, width=50)
entry_path.pack()

browse_button = tk.Button(window, text="Browse", command=choose_download_path)
browse_button.pack(pady=5)

download_button = tk.Button(window, text="Download", command=download_file)
download_button.pack(pady=5)

reset_button = tk.Button(window, text="Reset", command=reset_fields)
reset_button.pack(pady=5)

discord_icon = Image.open("icons/discord_icon.png")
discord_icon = discord_icon.resize((50, 50))
discord_icon = ImageTk.PhotoImage(discord_icon)

discord_link = tk.Label(window, image=discord_icon, cursor="hand2")
discord_link.pack(side=tk.RIGHT, padx=10)
discord_link.bind("<Button-1>", lambda e: webbrowser.open("https://discord.gg/G9ZzRaNN"))

github_icon = Image.open("icons/github_icon.png")
github_icon = github_icon.resize((50, 50))
github_icon = ImageTk.PhotoImage(github_icon)

github_link = tk.Label(window, image=github_icon, cursor="hand2")
github_link.pack(side=tk.RIGHT)
github_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/MooManisLoud"))

thank_you_label = tk.Label(window, text="\nThank you for using URL Downloader!")
thank_you_label.pack()

window.mainloop()
