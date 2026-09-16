import customtkinter as ctk

class CalculatorUI(ctk.CTkFrame):

    def __init__(self, parent, logic, width, height, max_history_chars):

        super().__init__(parent, fg_color='#1F1F1F')

        self.logic = logic
        self.width = width
        self.height = height
        self.max_history_chars = max_history_chars

        self.grid_rowconfigure(0, weight=5)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_history()
        self._build_display()

        self.winfo_toplevel().bind('<Button-1>', self._handle_entry_outside_click, add='+')


    def _build_history(self):

        self.history_frame = ctk.CTkFrame(self, fg_color='#3C3C3C')
        self.history_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=(8, 4))
        self.history_frame.grid_rowconfigure(0, weight=0)
        self.history_frame.grid_rowconfigure(1, weight=1)
        self.history_frame.grid_columnconfigure(0, weight=1)

        self.clear_history_button = ctk.CTkButton(
            self.history_frame,
            text='Clear History',
            height=28,
            fg_color='#2A2A2A',
            hover_color='#323232',
            font=('Jetbrains Mono', 14),
            command=self.history_clear
        )
        self.clear_history_button.grid(row=0, column=0, sticky='nsew', padx=4, pady=(4, 2))
        self.clear_history_button.configure(cursor='hand2')

        self.history_scroll = ctk.CTkScrollableFrame(
            self.history_frame,
            fg_color='#3C3C3C',
            scrollbar_button_color='#5A5A5A',
            scrollbar_button_hover_color='#6A6A6A'
        )
        self.history_scroll.grid(row=1, column=0, sticky='nsew', padx=10, pady=4)


    def _build_display(self):

        self.typing_frame = ctk.CTkFrame(self, fg_color='#1F1F1F', height=40)
        self.typing_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=4)

        self.typing_entry = ctk.CTkEntry(
            self.typing_frame,
            font=('Jetbrains Mono', 24),
            fg_color='#2E2E2E',
            width=514,
            height=50,
            corner_radius=8,
            border_width=1,
            border_color='#3C3C3C'
        )
        self.typing_entry.pack(side='left', fill='x', ipadx=6, pady=2)

        self.typing_entry.bind('<KeyRelease>', self._handle_key_release)
        self.typing_entry.bind('<BackSpace>', self._handle_backspace)
        self.typing_entry.bind('<Return>', self._handle_enter)


    def handle_symbol(self, symbol):

        if symbol == 'C':
            self.logic.clear()

        elif symbol == '⌫':
            self.logic.backspace()

        elif symbol == '=':
            original_input = self.logic.raw_input

            expression, result = self.logic.calculate()
            if expression:
                self.add_history_item(original_input, expression, result)

        elif symbol == '±':
            self.logic.negate()

        elif symbol == 'a×b':
            self.logic.factorize()

        else:
            self.logic.append(symbol)

        self.update_typing_display()


    def update_typing_display(self, invalid=False):

        self.typing_entry.delete(0, 'end')
        self.typing_entry.insert(0, self.logic.display_expression)
        self.typing_entry.configure(text_color='#888888' if invalid else '#FFFFFF')

        if self.logic.calculated:
            self.typing_entry.configure(font=ctk.CTkFont(size=24, weight='bold'))
        else:
            self.typing_entry.configure(font=ctk.CTkFont(size=24))


    def add_history_item(self, raw_input, expression, result):

        line = f'{expression} = {result}'

        outer = ctk.CTkFrame(self.history_scroll, fg_color='#444444')
        outer.pack(fill='x', pady=(4, 2))

        item_frame = ctk.CTkFrame(outer, fg_color='#444444')
        item_frame.pack(fill='x', pady=1)
        item_frame.grid_rowconfigure(0, weight=1)
        item_frame.grid_columnconfigure(0, weight=1)
        item_frame.grid_columnconfigure(1, weight=0)
        item_frame.grid_columnconfigure(2, weight=0)

        item_label = ctk.CTkLabel(
                item_frame,
                text=line,
                anchor='w',
                justify='left',
                fg_color='#444444',
                text_color='#BFBFBF',
                font=ctk.CTkFont(size=24)
            )
        item_label.grid(row=0, column=0, sticky='nsew', padx=(5, 0), pady=(1, 0))

        item_label.configure(cursor='hand2')
        item_label.bind('<Enter>', lambda e: item_label.configure(text_color='#FFFFFF'))
        item_label.bind('<Leave>', lambda e: item_label.configure(text_color='#BBBBBB'))
        item_label.bind('<Button-1>', lambda e, r=raw_input: self.history_click(r))

        formatted_line = self.format_history_item(line)
        item_label.configure(text=formatted_line)

        copy_button = ctk.CTkButton(
            item_frame,
            text='⧉',
            width=24,
            height=24,
            fg_color='#444444',
            hover_color='#555555',
            font=('Jetbrains Mono', 14),
            command=lambda l=line: self.history_copy(l)
        )
        copy_button.grid(row=0, column=1, sticky='e', padx=(5, 0))

        copy_button.configure(cursor='hand2')
        copy_button.bind('<Enter>', lambda e: copy_button.configure(text_color='#FFFFFF'))
        copy_button.bind('<Leave>', lambda e: copy_button.configure(text_color='#BBBBBB'))

        delete_button = ctk.CTkButton(
            item_frame,
            text='✕',
            width=24,
            height=24,
            fg_color='#444444',
            hover_color='#555555',
            font=('Jetbrains Mono', 14),
            command=lambda f=outer: self.history_delete(f)
        )
        delete_button.grid(row=0, column=2, sticky='e', padx=(5, 0))
      
        delete_button.configure(cursor='hand2')
        delete_button.bind('<Enter>', lambda e: delete_button.configure(text_color='#FFFFFF'))
        delete_button.bind('<Leave>', lambda e: delete_button.configure(text_color='#BBBBBB'))

        separator = ctk.CTkFrame(outer, height=1, fg_color='#555555')
        separator.pack(fill='x', pady=(0, 6))

        def scroll_to_bottom():
            canvas = self.history_scroll._parent_canvas
            canvas.update_idletasks()
            canvas.yview_moveto(1.0)

        self.history_scroll.after(0, scroll_to_bottom)


    def format_history_item(self, line):

        if len(line) > self.max_history_chars:
            return line[:self.max_history_chars - 1] + '…'
        return line


    def history_clear(self):

        for frame in list(self.history_scroll.winfo_children()):
            frame.destroy()

        def scroll_to_top():
            canvas = self.history_scroll._parent_canvas
            canvas.update_idletasks()
            canvas.yview_moveto(0.0)

        self.history_scroll.after(0, scroll_to_top)


    def history_click(self, raw_input):

        self.logic.calculated = False
        self.logic.last_result = None

        self.logic.raw_input = raw_input

        try:
            self.logic.tokens = self.logic.lexer.tokenize(raw_input)
            self.logic._update_expressions_from_tokens()
        except ValueError as v:
            print(f'{v}')
            self.logic.raw_input = ''
            self.logic.display_expression = 'Error'
            self.logic.tokens.clear()

        self.update_typing_display()


    def history_copy(self, line):
        self.clipboard_clear()
        self.clipboard_append(line)


    def history_delete(self, frame):
        frame.destroy()


    def _handle_key_release(self, event=None):

        if event is None:
            return None

        if event.keysym in ('Return', 'BackSpace'):
            return None
        
        if self.logic.display_expression == 'Error' and event.char:
            self.logic.clear()
            self.typing_entry.delete(0, 'end')
            self.typing_entry.insert(0, event.char)

        text = self.typing_entry.get().rstrip('\n')
        self.logic.raw_input = text

        self.logic.calculated = False

        invalid = False
        try:
            self.logic.tokens = self.logic.lexer.tokenize(text)
            print(self.logic.tokens)

            self.logic._update_expressions_from_tokens()
            if any(token.is_invalid() for token in self.logic.tokens):
                invalid = True

        except SyntaxError:
            invalid = True
            self.logic.display_expression = text

        self.update_typing_display(invalid)
        return None


    def _handle_backspace(self, event=None):

        self.logic.backspace()

        invalid = False
        if any(token.is_invalid() for token in self.logic.tokens):
            invalid = True

        self.update_typing_display(invalid)

        return 'break'


    def _handle_enter(self, event=None):

        original_input = self.logic.raw_input

        expression, result = self.logic.calculate()
        if expression:
            self.add_history_item(original_input, expression, result)

        self.update_typing_display()

        return 'break'


    def _handle_entry_outside_click(self, event):

        widget = event.widget
        while widget is not None:
            if widget == self.typing_entry:
                return
            widget = getattr(widget, 'master', None)

        self.focus_set()