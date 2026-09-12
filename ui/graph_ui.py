import customtkinter as ctk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from core.exceptions import SyntaxError

class GraphUI(ctk.CTkFrame):

    def __init__(self, parent, logic):

        super().__init__(parent, fg_color='#1F1F1F')

        self.width = 500
        self.height = 590
        self.logic = logic
        self.toggle_state = False
        self.secondary_buttons = {}

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self._build_canvas()
        self._build_controls()
        self._build_buttons()


    def _build_canvas(self):

        self.canvas_frame = ctk.CTkFrame(self, fg_color='#2E2E2E', width=self.width, height=300)
        self.canvas_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=2)

        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self._style_axes()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        self.coords_label = ctk.CTkLabel(
            self.canvas_frame,
            text='',
            font=('Jetbrains Mono', 10),
            fg_color='#2E2E2E',
            text_color='#AAAAAA'
        )
        self.coords_label.place(relx=1.0, rely=0.0, anchor='ne', x=-5, y=5)

        self.canvas.mpl_connect('motion_notify_event', self.on_hover)


    def _build_controls(self):

        self.controls_frame = ctk.CTkFrame(self, fg_color='#1F1F1F', height=70)
        self.controls_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=(4, 8))

        self.controls_frame.grid_columnconfigure(0, weight=1)
        self.controls_frame.grid_columnconfigure(1, weight=1)

        self.function_entry = ctk.CTkEntry(
            self.controls_frame, 
            font=('Jetbrains Mono', 16),
            fg_color='#2E2E2E',
            height=40,
            border_width=1,
            border_color='#3C3C3C',
            placeholder_text='Enter function…'
        )
        self.function_entry.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=2, pady=(2, 6))

        self.function_entry.configure(cursor='xterm')
        self.function_entry.bind('<Return>', self.plot_function)
        self.function_entry.bind('<KeyRelease>', self._sync_from_entry)

        self.plot_button = ctk.CTkButton(
            self.controls_frame,
            text='Plot',
            font=('Jetbrains Mono', 14),
            fg_color='#2A2A2A',
            hover_color='#323232',
            border_width=1,
            border_color='#3C3C3C',
            command=self.plot_function
        )
        self.plot_button.grid(row=1, column=0, sticky='nsew', padx=2, pady=2)
        self.plot_button.configure(cursor='hand2')

        self.clear_button = ctk.CTkButton(
            self.controls_frame,
            text='Clear',
            font=('Jetbrains Mono', 14),
            fg_color='#2A2A2A',
            hover_color='#323232',
            border_width=1,
            border_color='#3C3C3C',
            command=self.clear_functions
        )
        self.clear_button.grid(row=1, column=1, sticky='nsew', padx=2, pady=2)
        self.clear_button.configure(cursor='hand2')

    def _build_buttons(self):

        self.buttons_frame = ctk.CTkFrame(self, fg_color='#1F1F1F', height=170)
        self.buttons_frame.grid(row=3, column=0, sticky='nsew', padx=10, pady=(0, 8))

        graph_buttons = (
            (('C', 'clear'),
             ('.', 'decimal'),
             ('+', 'operator'),
             ('-', 'operator'),
             ('×', 'operator'),
             ('÷', 'operator')),

            ((('sin', 'sin⁻¹'), 'function'),
             (('cos', 'cos⁻¹'), 'function'),
             (('tan', 'tan⁻¹'), 'function'),
             (('csc', 'csc⁻¹'), 'function'),
             (('sec', 'sec⁻¹'), 'function'),
             (('cot', 'cot⁻¹'), 'function')),

            ((('x²', '√'), 'function'),
             (('x³', '∛'), 'function'),
             (('xʸ', '|x|'), 'function'),
             (('log', '10ˣ'), 'function'),
             (('log₂', '2ˣ'), 'function'),
             (('ln', 'eˣ'), 'function')),

            (('(', 'parenthesis'),
             (')', 'parenthesis'),
             ('x', 'variable'),
             ('π', 'constant'),
             ('e', 'constant'),
             ('⇄', 'toggle'))
        )

        self.toggle_state = False
        self.secondary_buttons = {}

        for r, row in enumerate(graph_buttons):
            for c, btn in enumerate(row):

                labels, type = btn

                if isinstance(labels, tuple):
                    text = labels[0]
                else:
                    text = labels

                if type == 'clear':
                        button = ctk.CTkButton(
                            self.buttons_frame,
                            text=text, 
                            font=('Jetbrains Mono', 20), 
                            fg_color='#E07B1A', 
                            hover_color='#FF944D',
                            command=lambda l=labels: self._graph_click(l)
                        )
                elif type == 'toggle':
                    button = ctk.CTkButton(
                        self.buttons_frame,
                        text=text, 
                        font=('Jetbrains Mono', 20), 
                        fg_color='#3C3C3C', 
                        hover_color='#4A4A4A', 
                        command=lambda l=labels: self._graph_click(l)
                        )
                else:
                    button = ctk.CTkButton(
                        self.buttons_frame,
                        text=text, 
                        font=('Jetbrains Mono', 20), 
                        fg_color='#262626', 
                        hover_color='#323232',
                        command=lambda l=labels: self._graph_click(l)
                        )

                button.grid(row=r, column=c, sticky='nsew', padx=2, pady=2)
                button.configure(cursor='hand2')

                if isinstance(labels, tuple):
                    self.secondary_buttons[button] =  labels

        for r in range(len(graph_buttons)):
            self.buttons_frame.grid_rowconfigure(r, weight=1)
        for c in range(6):
            self.buttons_frame.grid_columnconfigure(c, weight=1)


    def plot_function(self, event=None):

        self.logic.calculated = True

        try:
            x = np.linspace(-10, 10, 400)
            y = np.array([self.logic.evaluate_graph(xi) for xi in x], dtype=float)
        except SyntaxError:
            return

        self.ax.plot(x, y)
        self.canvas.draw()


    def clear_functions(self):
        self.ax.clear()
        self._style_axes()
        self.canvas.draw()


    def handle_symbol(self, symbol):

        if symbol == 'C':
            self.logic.clear()

        else:
            self.logic.append(symbol)

        self.update_typing_display()


    def update_typing_display(self):
        self.function_entry.delete(0, 'end')
        self.function_entry.insert(0, self.logic.display_expression)


    def toggle_functions(self):

        self.toggle_state = not self.toggle_state

        for button, labels in self.secondary_buttons.items():
            new_button = labels[1] if self.toggle_state else labels[0]
            button.configure(text=new_button)


    def on_hover(self, event):

         if event.inaxes:
            x, y = event.xdata, event.ydata
            self.coords_label.configure(text=f'x={x:.2f}, y={y:.2f}')
            self.canvas.get_tk_widget().config(cursor='cross')
         else:
            self.coords_label.configure(text='')
            self.canvas.get_tk_widget().config(cursor='arrow')


    def _graph_click(self, labels):

        if labels == '⇄':
            self.toggle_functions()
            return

        if isinstance(labels, tuple):
            symbol = labels[1] if self.toggle_state else labels[0]
        else:
            symbol = labels

        self.handle_symbol(symbol)


    def _style_axes(self):

        self.ax.set_facecolor('#2E2E2E')
        self.fig.patch.set_facecolor('#2E2E2E')
        self.ax.grid(True, color='#444444')

        self.ax.set_xticks([-10, -5, 5, 10])
        self.ax.set_yticks([-10, -5, 5, 10])
        self.ax.set_xticklabels(['-10', '-5', '5', '10'])
        self.ax.set_yticklabels(['-10', '-5', '5', '10'])

        self.ax.tick_params(
            colors='#AAAAAA',
            labelsize=8
        )

        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

        self.ax.spines['bottom'].set_position('zero')
        self.ax.spines['left'].set_position('zero')

        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['bottom'].set_linewidth(1)
        self.ax.spines['left'].set_linewidth(1)

        self.ax.title.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.xaxis.label.set_color('white')

        self.ax.annotate(
            '0',
            xy=(0, 0),
            xytext=(-3, -3),
            textcoords='offset points',
            color='#AAAAAA',
            fontsize=8,
            ha='right',
            va='top'
        )

        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)

    def _sync_from_entry(self, event=None):

        text = self.function_entry.get()

        try:
            self.logic.raw_input = text
            self.logic.tokens = self.logic.lexer.tokenize(self.logic.raw_input)
            print(self.logic.tokens)
            self.logic._update_expressions_from_tokens()
        except SyntaxError:
            pass