import customtkinter as ctk
from app import App

def main():

    root = ctk.CTk()
    root.title('Mathbench')

    App(root)
    root.mainloop()

if __name__ == '__main__':
    main() 