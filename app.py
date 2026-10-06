import customtkinter as ctk
from ui.basic_ui import BasicUI
from ui.scientific_ui import ScientificUI
from ui.graph_ui import GraphUI
from ui.unit_ui import UnitUI
from ui.currency_ui import CurrencyUI
from ui.date_ui import DateUI
from logic.calculator_logic import CalculatorLogic
from logic.graph_logic import GraphLogic
from logic.unit_logic import UnitLogic
from logic.currency_logic import CurrencyLogic
from logic.date_logic import DateLogic

BINDINGS = {
    'Global': (
        ('Ctrl+1 … 6', 'Switch mode'),
        ('Ctrl+H', 'Show this window'),
        ('Esc', 'Close this window')
    ),
    'Basic / Scientific': (
        ('Enter', 'Calculate'),
        ('Backspace', 'Delete last token'),
        ('Ctrl+Backspace', 'Clear entry'),
        ('Ctrl+L', 'Clear history'),
        ('Ctrl+Shift+D', 'Toggle DEG / RAD (Scientific)')
    ),
    'Graph': (
        ('Enter', 'Plot function'),
        ('Backspace', 'Delete last token'),
        ('Ctrl+Backspace', 'Clear entry'),
        ('Ctrl+L', 'Clear functions'),
        ('Ctrl+R', 'Recenter view'),
        ('Ctrl+I', 'Show intercepts'),
        ('Ctrl+J', 'Show intersections'),
        ('Ctrl+Equal / Ctrl+Plus', 'Zoom in'),
        ('Ctrl+Minus', 'Zoom out')
    ),
    'Unit': (
        ('Backspace', 'Delete last token'),
        ('Ctrl+Backspace', 'Clear entry'),
        ('Ctrl+S', 'Swap units')
    ),
    'Currency': (
        ('Backspace', 'Delete last token'),
        ('Ctrl+Backspace', 'Clear entry'),
        ('Ctrl+S', 'Swap currencies'),
        ('Ctrl+R', 'Refresh rates')
    ),
}

class App:

    def __init__(self, root):

        self.root = root

        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')
        self.root.configure(bg='#121212')

        self.calculator_logic = CalculatorLogic()
        self.graph_logic = GraphLogic()
        self.unit_logic = UnitLogic()
        self.currency_logic = CurrencyLogic()
        self.date_logic = DateLogic()

        self.bindings_popup = None

        self.top_frame = ctk.CTkFrame(root, fg_color='#1F1F1F', corner_radius=0)
        self.top_frame.pack(side='top', fill='x')

        self.help_button = ctk.CTkButton(
                self.top_frame,
                text=' ?',
                width=28,
                height=28,
                font=('Jetbrains Mono', 14),
                anchor='center',
                border_width=1,
                fg_color='#242424',
                hover_color='#2D2D2D',
                text_color='#FFFFFF',
                border_color='#333333',
                command=self.show_shortcuts
            )
        self.help_button.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)

        self.help_button.configure(cursor='hand2')

        self.selected_mode = ctk.StringVar(value='Basic')

        self.mode_frame = ctk.CTkFrame(root, fg_color='#2E2E2E', corner_radius=0)
        self.mode_frame.pack(side='top', fill='both', expand=True)

        self.windows = {
            'Basic': BasicUI(self.mode_frame, self.calculator_logic),
            'Scientific': ScientificUI(self.mode_frame, self.calculator_logic),
            'Graph': GraphUI(self.mode_frame, self.graph_logic),
            'Unit': UnitUI(self.mode_frame, self.unit_logic),
            'Currency': CurrencyUI(self.mode_frame, self.currency_logic),
            'Date': DateUI(self.mode_frame, self.date_logic)
        }

        self.mode_selector = ctk.CTkComboBox(
            self.top_frame,
            values=list(self.windows.keys()),
            variable=self.selected_mode,
            width=200,
            state='readonly',
            border_width=1,
            text_color='#FFFFFF',
            fg_color='#2A2A2A',
            button_color='#3A3A3A',
            button_hover_color='#444444',
            dropdown_fg_color='#2A2A2A',
            dropdown_text_color='#FFFFFF',
            command=self.switch_mode
        )
        self.mode_selector.pack(pady=10)

        self.mode_selector.bind('<Enter>', lambda e: e.widget.configure(cursor='arrow'))
        self.mode_selector.bind('<Leave>', lambda e: e.widget.configure(cursor='arrow'))

        for number, mode in enumerate(self.windows, start=1):
            self.root.bind_all(f'<Control-Key-{number}>', lambda e, m=mode: self.switch_mode(m))

        self.root.bind_all('<Control-h>', lambda e: self.show_shortcuts())

        self.current_window = self.windows['Basic']
        self.current_window.pack(fill='both')

        self.root.geometry(f'{self.current_window.width}x{self.current_window.height}')
        self.root.resizable(False, False)


    def switch_mode(self, window):

        if self.current_window == self.windows[window]:
            return

        self.current_window.pack_forget()
        self.current_window = self.windows[window]
        self.current_window.pack(fill='both')

        width = self.current_window.width
        height = self.current_window.height
        self.root.geometry(f'{width}x{height}')

        self.mode_selector.set(window)

        self.root.resizable(width=False, height=False)


    def show_shortcuts(self):

        if self.bindings_popup is not None and self.bindings_popup.winfo_exists():
            self.bindings_popup.lift()
            self.bindings_popup.focus()
            return

        popup = ctk.CTkToplevel(self.root, fg_color='#1F1F1F')

        popup.title('Keyboard Shortcuts')

        x = self.root.winfo_x() + (self.root.winfo_width() - 360) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 320) // 2

        popup.geometry(f'360x320+{x}+{y}')

        popup.resizable(False, False)
        popup.transient(self.root)

        popup.bind('<Escape>', lambda e: popup.destroy())

        scroll = ctk.CTkScrollableFrame(
            popup,
            fg_color='#1F1F1F',
            scrollbar_button_color='#555555',
            scrollbar_button_hover_color='#666666'
        )
        scroll.pack(fill='both', expand=True, padx=8, pady=8)
        scroll.grid_columnconfigure(0, weight=0)
        scroll.grid_columnconfigure(1, weight=1)

        row = 0
        for section, bindings in BINDINGS.items():

            header = ctk.CTkLabel(
                scroll,
                text=section,
                font=('Jetbrains Mono', 13, 'bold'),
                text_color='#777777'
            )
            header.grid(row=row, column=0, columnspan=2, sticky='w', pady=(10, 4))
            row += 1

            for keys, description in bindings:
                key_label = ctk.CTkLabel(
                    scroll,
                    text=keys,
                    font=('Jetbrains Mono', 12),
                    text_color='#FFFFFF',
                    fg_color='#2E2E2E',
                    corner_radius=4
                )
                key_label.grid(row=row, column=0, sticky='w', padx=(0, 12), pady=2, ipadx=4)

                description_label = ctk.CTkLabel(
                    scroll,
                    text=description,
                    font=('Jetbrains Mono', 12),
                    text_color='#CCCCCC',
                    anchor='center'
                )
                description_label.grid(row=row, column=1, sticky='ew', pady=2)
                row += 1

        self.bindings_popup = popup
        popup.after(100, popup.focus)