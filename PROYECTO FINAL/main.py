import flet as ft
from ui.app_view import main_view

def main(page: ft.Page):
    main_view(page)

if __name__ == "__main__":
    # Compatible con versiones modernas de Flet (1.x)
    ft.run(main)