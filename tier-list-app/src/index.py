from tkinterdnd2 import TkinterDnD
from ui.ui import UI


def main():
    window = TkinterDnD.Tk()
    window.title("Tier list Application")
    ui_view = UI(window)
    ui_view.start()

    window.mainloop()


if __name__ == "__main__":
    main()
