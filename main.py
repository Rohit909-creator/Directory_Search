import flet as ft
from flet import (
    Column,
    Row,
    Container,
    Page,
    UserControl,
    colors,
    Text,
    TextField,
    icons,
    IconButton,
    ElevatedButton,
    alignment,
    FontWeight,
    TextAlign
)
import sys
import Update

search = Update.Search()

# print(sys.argv)


def main(page: ft.page):

    page.title = "DirectorySort"

    def click(p):

        entries2 = Row(controls = [Text(value = f" {textfield.value}")])

        c2 = Container(content=entries2,
                    bgcolor=colors.BLACK54,
                    height=50,
                    width=350,
                    border_radius=20,
                    )
        # textfield.value = m(textfield.value).stringToMorse()
        
        with open(f"{' '.join(sys.argv[1:])}\Description.txt",'w') as f:
            f.write(textfield.value)

        embs = search.get_embedding(textfield.value)

        search.update(embs, f"{' '.join(sys.argv[1:])}\Description.txt")

        page.add(c2)
        page.update()
    # s = ft.Stack(controls=[c2],)
    page.window_width = 500
    page.window_height = 500
    textfield = TextField(width=350, border_radius=20)
    addbtn = ElevatedButton(text="Send", on_click=click)

    entries = ft.Row(controls=[textfield, addbtn])

    c = Container(content=entries,
                bgcolor=colors.BLACK87,
                width=500,
                height=50,
                border_radius=20)
    
    # img = ft.Image(src="C:\\Users\\ROHIT FRANCIS\\Downloads\\morse code.png", width=500,height=400,border_radius=20)
    
    page.add(c)
    # page.add(img)
    # l = ft.LabelPosition(value='hey')
    # page.add(l)
app = ft.app(target=main)


