from db import main_db
import flet as ft 


def main(page: ft.Page):
    page.title = "ToDO App"
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column(spacing=10)

    def load_task():
        task_list.controls.clear()
        for task_id, task_text in main_db.get_tasks("e"):
            # print(task_id, task_text)
            task_list.controls.append(create_task_row(task_id, task_text))

        page.update()

    def create_task_row(task_id, task_text):
        task_field = ft.TextField(value=task_text, read_only=True, expand=True)

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
            [task_field, enable_button, save_button, delete_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
    

    def add_task(_):
        if task_input.value:
            task = task_input.value
            task_id = main_db.add_task(task)
            task_list.controls.append(
                create_task_row(task_id=task_id, task_text=task)
            )
            task_input.value = ""
            page.update()



    task_input = ft.TextField(label='Введите задачу', read_only=False, expand=True, on_submit=add_task)
    add_button = ft.ElevatedButton("ADD", on_click=add_task)

    # page.add(task_input, add_button)
    page.add(ft.Row([task_input, add_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), task_list)

    load_task()




if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main)
