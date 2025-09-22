import flet as ft
from db import main_db


def main(page: ft.Page):
    page.title = "ToDo App"
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column(spacing=10)
    error_text = ft.Text(value="", color=ft.Colors.RED)
    filter_type = "all"

    task_input = ft.TextField(label="Введите задачу", expand=True)
    add_button = ft.ElevatedButton(text="ADD")

    def on_task_input_change(e):
        if len(e.control.value) > 100:
            error_text.value = "Не должно быть больше 100 символов!"
            add_button.disabled = True
        else:
            error_text.value = ""
            add_button.disabled = False
        page.update()

    task_input.on_change = on_task_input_change

    def add_task(_):
        text = task_input.value.strip()
        if len(text) > 100:
            error_text.value = "Не должно быть больше 100 символов!"
            page.update()
            return
        if text == "":
            error_text.value = "Введите текст задачи!"
            page.update()
            return
        task_id = main_db.add_task(text)
        task_list.controls.append(create_task_row(task_id, text, 0))
        task_input.value = ""
        error_text.value = ""
        add_button.disabled = False
        page.update()

    add_button.on_click = add_task
    task_input.on_submit = add_task

    def toggle_task(task_id, is_completed):
        main_db.update_task(task_id, completed=int(is_completed))
        load_tasks()

    def create_task_row(task_id, task_text, completed):
        checkbox = ft.Checkbox(value=bool(completed), on_change=lambda e: toggle_task(task_id, e.control.value))
        task_field = ft.TextField(value=task_text, read_only=True, expand=True)

        def enable_edit(_):
            task_field.read_only = False
            page.update()

        def save_task(_):
            if len(task_field.value.strip()) > 100:
                error_text.value = "Текст задачи не может быть длиннее 100 символов!"
                page.update()
                return
            main_db.update_task(task_id, task_field.value.strip())
            task_field.read_only = True
            error_text.value = ""
            page.update()

        def delete_task(_):
            main_db.delete_task(task_id)
            load_tasks()

        return ft.Row([
            checkbox,
            task_field,
            ft.IconButton(ft.Icons.EDIT, on_click=enable_edit),
            ft.IconButton(ft.Icons.SAVE_ALT_ROUNDED, on_click=save_task, icon_color=ft.Colors.GREEN),
            ft.IconButton(ft.Icons.DELETE, on_click=delete_task, icon_color=ft.Colors.RED),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def load_tasks():
        task_list.controls.clear()
        tasks = main_db.get_tasks()

        if filter_type == "completed":
            filtered = [t for t in tasks if t[2] == 1]
        elif filter_type == "uncompleted":
            filtered = [t for t in tasks if t[2] == 0]
        else:
            filtered = tasks

        for task_id, task_text, completed in filtered:
            task_list.controls.append(create_task_row(task_id, task_text, completed))
        page.update()

    def set_filter(value):
        nonlocal filter_type
        filter_type = value
        load_tasks()

    filter_buttons = ft.Row([
        ft.ElevatedButton("Все", on_click=lambda e: set_filter("all")),
        ft.ElevatedButton("Выполненные", on_click=lambda e: set_filter("completed")),
        ft.ElevatedButton("Невыполненные", on_click=lambda e: set_filter("uncompleted")),
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    page.add(
        ft.Row([task_input, add_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        error_text,
        filter_buttons,
        task_list
    )

    load_tasks()


if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main)
