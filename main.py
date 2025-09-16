from db import main_db
import flet as ft

def main(page: ft.Page):
    pass

if __name__=="__main__":
    main_db.init_db()
    ft.app(target=main)