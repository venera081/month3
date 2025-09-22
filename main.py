from db import main_db
import flet as ft 


def main(page: ft.Page):
    page.title = "ToDO App"
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column(spacing=10)

    filter_type = "all"

    def load_task():
        task_list.controls.clear()
        tasks = main_db.get_tasks()

        if filter_type == "completed":
            tasks = [(task_id, task_text, completed) for task_id, task_text, completed in tasks if completed == 1]
        elif filter_type == "uncompleted":
            tasks = [(task_id, task_text, completed) for task_id, task_text, completed in tasks if completed == 0]

        for task_id, task_text, completed in tasks:
            # print(task_id, task_text)
            task_list.controls.append(create_task_row(task_id, task_text, completed))

        page.update()

    def create_task_row(task_id, task_text, completed):
        task_field = ft.TextField(value=task_text, read_only=True, expand=True)

        task_checkbox = ft.Checkbox(value=bool(completed), on_change=lambda e: toggle_task(task_id, e.control.value)) 

        def enable_edit(_):
            task_field.read_only = False
            task_field.update()
        
        enable_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=enable_edit, tooltip='Редактировать')

        def save_task(_):
            main_db.update_task(task_id, task_field.value)
            page.update()

        save_button = ft.IconButton(icon=ft.Icons.SAVE_ALT_ROUNDED, tooltip="Сохранить", on_click=save_task, icon_color=ft.Colors.GREEN)

        def delete_task(_):
            main_db.delete_task(task_id)
            page.update()

            if delete_task:
                task_field.value = ""
                load_task()

        
        delete_button = ft.IconButton(icon=ft.Icons.DELETE, tooltip="Удалить", on_click=delete_task, icon_color=ft.Colors.RED)


        return ft.Row(
            [task_checkbox, task_field, enable_button, save_button, delete_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
    

    def add_task(_):
        if task_input.value:
            task = task_input.value
            task_id = main_db.add_task(task)
            task_list.controls.append(
                create_task_row(task_id=task_id, task_text=task, completed=None)
            )
            task_input.value = ""
            page.update()



    task_input = ft.TextField(label='Введите задачу', read_only=False, expand=True, on_submit=add_task)
    add_button = ft.ElevatedButton("ADD", on_click=add_task)

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_task()

    def toggle_task(task_id, is_completed):
        main_db.update_task(task_id, completed=int(is_completed))
        load_task()

    filter_buttons = ft.Row(controls=[
        ft.ElevatedButton("Все", on_click=lambda e: set_filter('all')),
        ft.ElevatedButton("Выполненные", on_click=lambda e: set_filter("completed")),
        ft.ElevatedButton("Невыполненные", on_click=lambda e: set_filter("uncompleted"))
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    # page.add(task_input, add_button)
    page.add(ft.Row([task_input, add_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), filter_buttons, task_list)

    load_task()




if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main)

    