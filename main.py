import flet as ft


def main(page: ft.Page):
    page.title = "Заметки"


    tasks = []
    view_mode = {"value": "all"}
    sidebar_open = {"value": True}

    tasks_view = ft.Column()



    def toggle_sidebar(e):
        sidebar_open["value"] = not sidebar_open["value"]

        sidebar.width = 200 if sidebar_open["value"] else 0
        sidebar.opacity = 1 if sidebar_open["value"] else 0

        page.update()


    def render_tasks():
        tasks_view.controls.clear()

        for i, task in enumerate(tasks):
            if view_mode["value"] == "favorites" and not task["fav"]:
                continue

            star_icon = ft.Icons.STAR if task["fav"] else ft.Icons.STAR_BORDER

            def toggle_fav(e, index=i):
                tasks[index]["fav"] = not tasks[index]["fav"]
                render_tasks()
                page.update()

            tasks_view.controls.append(
                ft.Container(
                    padding=10,
                    margin=5,
                    border_radius=10,
                    bgcolor=ft.Colors.BLUE_GREY_50,
                    content=ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(task["title"], weight=ft.FontWeight.BOLD),
                                    ft.Text(task["text"], opacity=0.7),
                                ],
                                expand=True,
                            ),
                            ft.IconButton(icon=star_icon, on_click=toggle_fav),
                        ],
                    ),
                )
            )


    title_input = ft.TextField(hint_text="Оглавление")
    text_input = ft.TextField(hint_text="Текст", multiline=True)

    def add_clicked(e):
        if not title_input.value.strip():
            return

        tasks.append({
            "title": title_input.value,
            "text": text_input.value,
            "fav": False
        })

        title_input.value = ""
        text_input.value = ""

        render_tasks()
        page.update()


    def set_all(e):
        view_mode["value"] = "all"
        render_tasks()
        page.update()

    def set_favorites(e):
        view_mode["value"] = "favorites"
        render_tasks()
        page.update()


    sidebar = ft.Container(
        width=200,
        bgcolor=ft.Colors.BLUE_GREY_100,
        animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
        content=ft.Column(
            [
                ft.Text("Меню"),
                ft.TextButton("Все заметки", on_click=set_all),
                ft.TextButton("Избранное", on_click=set_favorites),
            ]
        ),
    )


    menu_button = ft.IconButton(icon=ft.Icons.MENU, on_click=toggle_sidebar)

    add_panel = ft.Column(
        controls=[
            title_input,
            text_input,
            ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=add_clicked),
        ],
    )

    header = ft.Row(
        controls=[
            menu_button,
            ft.Text("Мои заметки", size=20, weight=ft.FontWeight.BOLD),
        ],
    )

    main_column = ft.Column(
        controls=[
            header,
            add_panel,
            tasks_view,
        ],
        expand=True,
    )

    page.add(
        ft.Row(
            controls=[sidebar, main_column],
            expand=True,
        )
    )

    render_tasks()


ft.run(main)