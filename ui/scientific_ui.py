import customtkinter as ctk
from ui.calculator_ui import CalculatorUI

class ScientificUI(CalculatorUI):

    def __init__(self, parent, logic):

        super().__init__(parent, logic, width=620, height=555, max_history_chars=34)

        self.fx_menu = None
        self.toggle_state = False
        self.secondary_buttons = {}

        self._build_angle_switch()
        self._build_buttons()


    def _build_angle_switch(self):

        self.angle_switch = ctk.CTkButton(
            self.typing_frame,
            text='DEG',
            width=40,
            height=38,
            fg_color='#262626',
            hover_color='#323232',
            border_width=1,
            border_color='#3C3C3C',
            font=('Jetbrains Mono', 24),
            command=self.toggle_angle
        )
        self.angle_switch.pack(side='right', fill='x', ipadx=4, ipady=6)
        self.angle_switch.configure(cursor='hand2')    


    def _build_buttons(self):

        self.buttons_frame = ctk.CTkFrame(self, fg_color='#1F1F1F')
        self.buttons_frame.grid(row=2, column=0, sticky='nsew', padx=8, pady=(4, 8))

        self.buttons_frame.grid_rowconfigure(0, weight=1)
        self.buttons_frame.grid_columnconfigure(0, weight=1, uniform='group1')
        self.buttons_frame.grid_columnconfigure(1, weight=1, uniform='group1')

        self.basic_frame = ctk.CTkFrame(self.buttons_frame, fg_color='#1F1F1F')
        self.basic_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 1))

        basic_buttons = (
            ('C', 'clear'),
            ('⌫', 'backspace'),
            ('.', 'decimal'),
            ('+', 'operator'),

            ('1', 'number'),
            ('2', 'number'),
            ('3', 'number'),
            ('-', 'operator'),

            ('4', 'number'),
            ('5', 'number'),
            ('6', 'number'),
            ('×', 'operator'),

            ('7', 'number'),
            ('8', 'number'),
            ('9', 'number'),
            ('÷', 'operator'),

            ('0', 'number'),
            ('div', 'operator'),
            ('mod', 'operator'),
            ('=', 'equal')
        )
           
        for i, (symbol, type) in enumerate(basic_buttons):

            if type == 'number':
                button = ctk.CTkButton(
                    self.basic_frame,
                    text=symbol,
                    font=('Jetbrains Mono', 20),
                    fg_color='#3C3C3C',
                    hover_color='#4A4A4A',
                    command=lambda s=symbol: self.handle_symbol(s))
            elif type == 'operator' or type == 'decimal':
                button = ctk.CTkButton(
                    self.basic_frame,
                    text=symbol, 
                    font=('Jetbrains Mono', 20), 
                    fg_color='#262626', 
                    hover_color='#323232', 
                    command=lambda s=symbol: self.handle_symbol(s))
            elif type == 'backspace':
                button = ctk.CTkButton(
                    self.basic_frame, 
                    text=symbol, 
                    font=('Jetbrains Mono', 20), 
                    fg_color='#262626', 
                    hover_color='#C42B2B', 
                    command=lambda s=symbol: self.handle_symbol(s))
            else:
                button = ctk.CTkButton(
                    self.basic_frame, 
                    text=symbol, 
                    font=('Jetbrains Mono', 20), 
                    fg_color='#E07B1A', 
                    hover_color='#FF944D', 
                    command=lambda s=symbol: self.handle_symbol(s))

            button.configure(cursor='hand2')
            button.grid(row=i // 4, column=i % 4, sticky='nsew', padx=2, pady=2)

        for i in range(5): 
            self.basic_frame.grid_rowconfigure(i, weight=1) 
        for j in range(4): 
            self.basic_frame.grid_columnconfigure(j, weight=1)

        self.scientific_frame = ctk.CTkFrame(self.buttons_frame, fg_color='#1F1F1F')
        self.scientific_frame.grid(row=0, column=1, sticky='nsew', padx=(1, 0))

        scientific_buttons = (
        (('(', 'parenthesis'),
         (')', 'parenthesis'),
         ('!', 'function'),
         ('Ans', 'constant')),

        ((('sin', 'sin⁻¹'), 'function'),
         (('cos', 'cos⁻¹'), 'function'),
         (('tan', 'tan⁻¹'), 'function'),
         (('cot', 'cot⁻¹'), 'function')),

        ((('log', 'log₂'), 'function'),
         (('ln', 'a×b'), 'function'),
         (('|x|', '±'), 'function'),
         (('%', '‰'), 'percentage')),

        ((('x²', '√'), 'function'),
         (('x³', '∛'), 'function'),
         (('xʸ', '×10ʸ'), 'function'),
         (('x⁻¹', 'φ'), 'function')),

        (('π', 'constant'),
         ('e', 'constant'),
         ('f(x) ▾', 'functions'),
         ('⇄', 'toggle'))
        )

        self.toggle_state = False
        self.secondary_buttons = {}

        for r, row in enumerate(scientific_buttons):
            for c, btn in enumerate(row):

                labels, type = btn

                if isinstance(labels, tuple):
                    text = labels[0]
                else:
                    text = labels

                button = ctk.CTkButton(
                    self.scientific_frame,
                    text=text,
                    font=('JetBrains Mono', 20),
                    fg_color='#262626' if text != '⇄' else '#3C3C3C',
                    hover_color='#323232' if text != '⇄' else '#4A4A4A',
                    command=lambda l=labels: self._scientific_click(l)
                )
                button.configure(cursor='hand2')
                button.grid(row=r, column=c, sticky='nsew', padx=2, pady=2)

                if text == 'f(x) ▾':
                    self.fx_button = button

                if isinstance(labels, tuple):
                    self.secondary_buttons[button] =  labels


        for r in range(len(scientific_buttons)):
            self.scientific_frame.grid_rowconfigure(r, weight=1)
        for c in range(4):
            self.scientific_frame.grid_columnconfigure(c, weight=1)


    def toggle_angle(self):

        self.logic.toggle_angle_mode()

        if self.logic.angle_mode == 'DEG':
            self.angle_switch.configure(text='DEG')
        else:
            self.angle_switch.configure(text='RAD')


    def toggle_fx_menu(self):

        if self.fx_menu is None or not self.fx_menu.winfo_exists():
            self._open_fx_menu()
        else:
            self._close_fx_menu()


    def toggle_functions(self):

        self.toggle_state = not self.toggle_state

        for button, labels in self.secondary_buttons.items():
            new_button = labels[1] if self.toggle_state else labels[0]
            button.configure(text=new_button) 


    def _scientific_click(self, labels):

        if labels == '⇄':
            self.toggle_functions()
            return

        if labels == 'f(x) ▾':
            self.toggle_fx_menu()
            return

        if isinstance(labels, tuple):
            symbol = labels[1] if self.toggle_state else labels[0]
        else:
            symbol = labels

        self.handle_symbol(symbol)


    def _insert_function(self, function):
            self.handle_symbol(function)
            self._close_fx_menu()


    def _open_fx_menu(self):

        self.fx_menu = ctk.CTkToplevel(self)

        self.fx_menu.overrideredirect(True)

        button_x = self.fx_button.winfo_rootx()
        button_y = self.fx_button.winfo_rooty()
        button_width = self.fx_button.winfo_width()
        button_height = self.fx_button.winfo_height()

        x = button_x + (button_width // 2) - (150 // 2)
        y = button_y + button_height

        self.fx_menu.geometry(f'150x225+{x}+{y}')

        fx_scroll = ctk.CTkScrollableFrame(
            self.fx_menu,
            fg_color='#1F1F1F',
            scrollbar_button_color= '#555555',
            scrollbar_button_hover_color='#666666'
        )
        fx_scroll.pack(fill='both', expand=True, padx=10, pady=10)

        functions = ('round', 'floor', 'ceil', 'trunc', 'frac', 'sign', 'gamma', 'lgamma', 'csc', 'sec',
        'csc⁻¹', 'sec⁻¹', 'sinh', 'cosh', 'tanh', 'csch', 'sech', 'coth', 'sinh⁻¹', 'cosh⁻¹', 'tanh⁻¹',
        'csch⁻¹', 'sech⁻¹', 'coth⁻¹')

        for function in functions:
            button = ctk.CTkButton(
                fx_scroll,
                text=f'{function}(x)',
                fg_color='#1F1F1F',
                hover_color='#323232',
                text_color='#FFFFFF',
                corner_radius=0,
                height=32,
                font=('Jetbrains Mono', 18),
                command=lambda f=function: self._insert_function(f)
            )
            button.pack(fill='x')
            button.configure(cursor='hand2')

        self.winfo_toplevel().bind('<Button-1>', self._handle_toplevel_outside_click, add='+')


    def _close_fx_menu(self):
        if self.fx_menu is not None and self.fx_menu.winfo_exists():
            self.fx_menu.destroy()
            self.fx_menu = None


    def _handle_toplevel_outside_click(self, event):

        if self.fx_menu is None or not self.fx_menu.winfo_exists():
            return

        if event.widget == self.fx_button or str(event.widget).startswith(str(self.fx_button)):
            return

        x, y = event.x_root, event.y_root
        menu_x = self.fx_menu.winfo_rootx()
        menu_y = self.fx_menu.winfo_rooty()
        menu_w = self.fx_menu.winfo_width()
        menu_h = self.fx_menu.winfo_height()

        if not (menu_x <= x <= menu_x + menu_w and menu_y <= y <= menu_y + menu_h):
            self._close_fx_menu()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    