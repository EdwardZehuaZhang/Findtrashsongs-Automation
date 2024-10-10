import os
import subprocess
import gc
import time
import shutil
import sys

class DualLogger:
    def __init__(self, log_file):
        self.terminal = sys.stdout
        self.log_file = log_file

    def write(self, message):
        self.terminal.write(message)
        self.log_file.write(message)

    def flush(self):
        self.terminal.flush()
        self.log_file.flush()

def run_pipeline():
    with open("pipeline_log.txt", "w") as log_file:
        dual_logger = DualLogger(log_file)
        sys.stdout = dual_logger

        print("Starting description generation...", flush=True)
        description_process = subprocess.Popen([r"D:/Coding Files/GitHub/Findtrashsongs Automation/.venv/Scripts/python.exe", "description.py"],
                                               stdout=log_file, stderr=log_file)
        
        description_process.wait()
        print("Description generation done.", flush=True)

        if description_process.poll() is None:
            description_process.terminate()
        time.sleep(1)
        description_process.kill()
        description_process = None
        
        print("Starting download pipeline...", flush=True)
        download_process = subprocess.Popen([r"D:/Coding Files/GitHub/Findtrashsongs Automation/.venv/Scripts/python.exe", "download.py"],
                                            stdout=log_file, stderr=log_file)
        
        download_process.wait()
        print("Download complete. Shutting down download process and freeing memory...", flush=True)

        if download_process.poll() is None:
            download_process.terminate()
        time.sleep(1)
        download_process.kill()
        download_process = None
        
        print("Starting video editing...", flush=True)
        edit_process = subprocess.Popen([r"D:/Coding Files/GitHub/Findtrashsongs Automation/.venv/Scripts/python.exe", "edit.py"],
                                        stdout=log_file, stderr=log_file)
        
        edit_process.wait()
        print("Video editing done. Shutting down first process and freeing memory...", flush=True)

        if edit_process.poll() is None:
            edit_process.terminate()
        time.sleep(1)
        edit_process.kill()
        edit_process = None
        
        time.sleep(20)
        gc.collect()

        print("Starting caption pipeline...", flush=True)
        caption_process = subprocess.Popen([r"D:/Coding Files/GitHub/Findtrashsongs Automation/.venv/Scripts/python.exe", "caption.py"],
                                           stdout=log_file, stderr=log_file)
        
        caption_process.wait()
        print("Captioning done. Pipeline complete.", flush=True)

        if caption_process.poll() is None:
            caption_process.terminate()
        time.sleep(1)
        caption_process.kill()
        caption_process = None
        
        gc.collect()

        print("Cleaning up unnecessary files...", flush=True)

        output_with_caption_folder = "output_with_caption"
        output_with_caption_file = "output_with_caption.mp4"
        temp_audio_file = "temp_audio.aac"  

        if os.path.exists(output_with_caption_folder):
            shutil.rmtree(output_with_caption_folder)
            print(f"Deleted folder: {output_with_caption_folder}", flush=True)

        if os.path.exists(output_with_caption_file):
            os.remove(output_with_caption_file)
            print(f"Deleted file: {output_with_caption_file}", flush=True)

        if os.path.exists(temp_audio_file):
            os.remove(temp_audio_file)
            print(f"Deleted file: {temp_audio_file}", flush=True)

        print("Cleanup complete.", flush=True)

if __name__ == "__main__":
    run_pipeline()
