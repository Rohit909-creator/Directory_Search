import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FolderHandler(FileSystemEventHandler):
    # This class handles the creation of new folders
    def __init__(self)->None:
        super().__init__()
        self.folder_path = None

    def on_created(self, event):
        # This method is called when a new folder is created
        if event.is_directory:

            # If the event is a directory, get its name
            folder_name = event.src_path
            print(f"New folder created: {folder_name}")
            self.folder_path = event.src_path
            

    def on_modified(self, event):
        pass

    def on_moved(self, event):
        if event.is_directory:
            # print(self.folder_path)
            if event.src_path == self.folder_path:
                folder_name = event.dest_path
                print(f"New folder Modified: {folder_name}")
                os.system(f"python main.py {folder_name}")                


# Create an observer object that will watch a given path
path = "C:\\Users\\ROHIT FRANCIS" # Change this to your desired path
observer = Observer()
observer.schedule(FolderHandler(), path, recursive=True)

# Start the observer thread
observer.start()
print(f"Watching {path} for new folders...")

# Keep the program running until Ctrl+C is pressed
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

# Wait for the observer thread to finish
observer.join()

