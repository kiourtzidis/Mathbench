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

        self.top_frame = ctk.CTkFrame(root, fg_color='#1F1F1F', corner_radius=0)
        self.top_frame.pack(side='top', fill='x')

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

        self.root.bind_all('<Control-Key-1>', lambda e: self.switch_mode('Basic'))
        self.root.bind_all('<Control-Key-2>', lambda e: self.switch_mode('Scientific'))
        self.root.bind_all('<Control-Key-3>', lambda e: self.switch_mode('Graph'))
        self.root.bind_all('<Control-Key-4>', lambda e: self.switch_mode('Unit'))
        self.root.bind_all('<Control-Key-5>', lambda e: self.switch_mode('Currency'))
        self.root.bind_all('<Control-Key-6>', lambda e: self.switch_mode('Date'))

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