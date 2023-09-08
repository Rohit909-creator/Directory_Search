import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rich import print
from rich.markdown import Markdown
from rich.prompt import Prompt
import keyboard
import Update



search = Update.Search()

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
        if keyboard.is_pressed('s') and keyboard.is_pressed('e'):
            q = Prompt.ask("Description")
            print(f"[green]Searching:[/green] [bold red]{q}[/bold red].....")

            probs, idx, path_ = search.query(q)
            print(f"[green]Got the path to your folder:[/green][cyan]{path_}[/cyan] [green]confidence:[/green][cyan]{probs[0][idx]}[/cyan]")
            #after you are done with searching
            print(f"[blue]Watching {path} for new folders...[/blue]")

    def on_moved(self, event):
        if event.is_directory:
            # print(self.folder_path)
            if event.src_path == self.folder_path:
                folder_name = event.dest_path
                print(f"New folder Modified: {folder_name}")
                # os.system(f"python main.py {folder_name}")                
                markdown_text = f"""
# File Descripter

- Provide Description about the file you are uploading in the directory {folder_name}.
- Do not provide few word description.
- Make sure the description is accurate.

"""
                
                markdown = Markdown(markdown_text)

                print(markdown)

                inp = Prompt.ask("Description")

                print(f"input: [bold green]{inp}[/bold green]!")

                with open(f"{folder_name}\Description.txt",'w') as f:
                    f.write(inp)

                embs = search.get_embedding(inp)

                search.update(embs, f"{folder_name}\Description.txt")
                os.system("cls")
                intro = f"""
                # Directory Search
- Press 'SE' at the sametime for searching
- when you create a new folder the program will automatically detect and ask you for its description
"""

                markdown = Markdown(intro)
                print(markdown)
                print(f"[blue]Watching {path} for new folders...[/blue]")
                

# Create an observer object that will watch a given path
path = "C:\\Users\\ROHIT FRANCIS" # Change this to your desired path
observer = Observer()
observer.schedule(FolderHandler(), path, recursive=True)


intro = f"""
# Directory Search
- Press 'SE' at the sametime for searching
- when you create a new folder the program will automatically detect and ask you for its description
"""

markdown = Markdown(intro)
print(markdown)

# Start the observer thread
observer.start()
print(f"[blue]Watching {path} for new folders...[/blue]")


# Keep the program running until Ctrl+C is pressed
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

# Wait for the observer thread to finish
observer.join()

