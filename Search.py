""" Flet Job App """

# modules
import flet as ft
import asyncio
import Update

search = Update.Search()

# now create the individual components for the application
class JobEntry(ft.Container):
    def __init__(
        self,
        job_area,
        page:ft.Page,
        col={"xs": 12, "sm": 12, "md": 12, "lg": 12, "xl": 11},
        expand=True,
    ):
        super().__init__(col=col, expand=expand)

        self.flag = 0
        self.job_area = job_area

        self.input_query = ft.TextField(
            border_color="transparent",
            height=50,
            on_submit=lambda e: asyncio.run(self.run_compilation(e, page)),
        )

        self.loader = ft.ProgressBar(
            value=0,
            bar_height=1.25,
            bgcolor="transparent",
            color="#64b687",
        )

        self.grid = ft.GridView(
            expand=True,
            runs_count=5,
            max_extent=350,
            child_aspect_ratio=1,
            spacing=45,
            run_spacing=45,
        )

        self.column = ft.Column(
            horizontal_alignment="center",
            spacing=0,
            controls=[
                ft.Divider(height=20, color="transparent"),
                ft.Container(
                    content=ft.Row(
                        spacing=4,
                        alignment="center",
                        controls=[
                            # title
                            ft.Column(
                                alignment="center",
                                horizontal_alignment="start",
                                controls=[
                                    ft.Text(
                                        "PySearch",
                                        style=ft.TextThemeStyle("headlineMedium"),
                                        weight="bold",
                                    ),
                                ],
                            ),
                            ft.Column(
                                alignment="center",
                                horizontal_alignment="start",
                                controls=[
                                    ft.Text(
                                        "- Search Engine",
                                        style=ft.TextThemeStyle("headlineMedium"),
                                        weight="bold",
                                    ),
                                ],
                            ),
                        ],
                    )
                ),
                ft.Divider(height=20, color="transparent"),
                # text field
                ft.Container(
                    content=self.input_query,
                    height=50,
                    border=ft.border.all(1, "#64b687"),
                    border_radius=6,
                    shadow=ft.BoxShadow(
                        spread_radius=8,
                        blur_radius=16,
                        color=ft.colors.with_opacity(0.25, "black"),
                        offset=(5, 5),
                    ),
                ),
                ft.Divider(height=20, color="transparent"),
                self.loader,
            ],
        )

        self.content = self.column

    # we'll be running the logic via async to make the application smooth for the UX
    async def run_compilation(self, e, page):
        # let's make the app a little more UX friendly
        # await self.remove_results(page)
        await asyncio.gather(self.run_loader(), self.get_data(page))
        await asyncio.sleep(2)
        await self.stop_loader()
        # await self.show_results()

    async def run_loader(self):
        self.loader.value = True
        self.loader.update()

    async def stop_loader(self):
        self.loader.value = 0
        self.loader.update()

    # async def show_results(self):
    #     for container in self.grid.controls[:]:
    #         container.opacity = 1
    #         container.update()
    #         print("inside show_results()")

    # async def remove_results(self, page:ft.Page):
    #     print("inside remove_results")
    #     if self.flag !=0:
    #         self.flag += 1
        

    # let's add some UI to the ssearch compoenent
    def highlight_box(self, e):
        for index, container in enumerate(self.grid.controls[:]):
            if e.control.data != index:
                if e.data == "true":
                    container.opacity = 0.25
                else:
                    container.opacity = 1

                container.update()

    def redirect_to_url(self, e, route):
        e.page.launch_url(route)

    def custom_text(self, title, subtitle):
        return ft.Text(
            title,
            weight="bold",
            size=14,
            overflow=ft.TextOverflow.ELLIPSIS,
            spans=[ft.TextSpan(text=subtitle, style=ft.TextStyle(weight="w300"))],
        )

    # let's work the main logic first then add the UI-based logic later
    # the following async method gets data from a custom API
    async def get_data(self, page: ft.Page):
        temp_list = []
        # now we can loop the JSON data and create a UI for each individual data point
        # res = [1,2,4,5]

        q = self.input_query.value

        probs, idx, path_, res = search.query(q)

        if self.flag != 0:
            page.controls.pop()
        self.flag = 1
        r = ft.Row(wrap=True, scroll="always", expand=True)
        page.add(r)

        for path, prob  in zip(res, sorted(probs[0])[-1::-1]):
            r.controls.append(ft.Container(
                ft.Text(f"{path} probability:{prob}"),
                width=200,
                height=200,
                alignment=ft.alignment.center,
                bgcolor="#64b687",
                border=ft.border.all(1, ft.colors.AMBER_400),
                border_radius=ft.border_radius.all(5),
            ))
        page.update()
        # self.job_area.update()
        # print("inside get_data()")

class JobSearchResult(ft.Container):
    def __init__(
        self,
        page: ft.Page,
        col={"xs": 12, "sm": 12, "md": 12, "lg": 12, "xl": 11},
        alignment=ft.alignment.center,
    ):
        super().__init__(col=col, alignment=alignment)
        self.page = page
        self.height = self.page.height


# create a class called app to gather all application componenets


class App(ft.UserControl):
    def __init__(
        self,
        page: ft.Page,
    ):
        self.page = page
        self.job_result = JobSearchResult(self.page)
        self.job_entry = JobEntry(self.job_result, page)
        self.row = ft.ResponsiveRow(
            alignment="center",
            vertical_alignment="center",
        )
        super().__init__()

    def build(self):
        self.row.controls.append(self.job_entry)
        self.row.controls.append(ft.VerticalDivider(width=25, color="transparent"))
        self.row.controls.append(self.job_result)
        return self.row


def apk(page: ft.Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.bgcolor = "#1f262f"
    page.padding = 35

    theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            thickness=3,
            radius=10,
            main_axis_margin=-20,
            thumb_color="#64b687",
        )
    )

    page.theme = theme

    app = App(page)
    page.add(app)
    page.update()


if __name__ == "__main__":
    ft.app(target=apk)