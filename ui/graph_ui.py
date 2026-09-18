import customtkinter as ctk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from core.exceptions import SyntaxError

class GraphUI(ctk.CTkFrame):

    def __init__(self, parent, logic):

        super().__init__(parent, fg_color='#1F1F1F')

        self.width = 500
        self.height = 590
        self.logic = logic
        self.toggle_state = False
        self.secondary_buttons = {}
        self.plotted_functions = []

        self.selected_marker = None
        self.selected_label = None

        self.pan_start = None
        self.pan_start_xlim = None
        self.pan_start_ylim = None

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

        self.recenter_button = ctk.CTkButton(
            self.canvas_frame,
            text='⊙',
            font=('Jetbrains Mono', 16),
            width=18,
            height=18,
            text_color='#BBBBBB',
            fg_color='#2E2E2E',
            hover_color='#2E2E2E',
            command=self.recenter
        )
        self.recenter_button.place(relx=0.0, rely=0.0, anchor='nw', x=4, y=5)

        self.recenter_button.configure(cursor='hand2')
        self.recenter_button.bind('<Enter>', lambda e: self.recenter_button.configure(text_color='#FFFFFF'))
        self.recenter_button.bind('<Leave>', lambda e: self.recenter_button.configure(text_color='#BBBBBB'))
        

        self.vertical_separator = ctk.CTkFrame(
            self.canvas_frame,
            width=1,
            height=28,
            fg_color='#444444'
        )
        self.vertical_separator.place(relx=0.0, rely=0.0, anchor='nw', x=30, y=5)

        self.zoom_in_button = ctk.CTkButton(
            self.canvas_frame,
            text='+',
            font=('Jetbrains Mono', 16),
            width=18,
            height=18,
            text_color='#BBBBBB',
            fg_color='#2E2E2E',
            hover_color='#2E2E2E',
            command=lambda: self.zoom(0.9)
        )
        self.zoom_in_button.place(relx=0.0, rely=0.0, anchor='nw', x=34, y=5)

        self.zoom_in_button.configure(cursor='hand2')
        self.zoom_in_button.bind('<Enter>', lambda e: self.zoom_in_button.configure(text_color='#FFFFFF'))
        self.zoom_in_button.bind('<Leave>', lambda e: self.zoom_in_button.configure(text_color='#BBBBBB'))

        self.zoom_out_button = ctk.CTkButton(
            self.canvas_frame,
            text='-',
            font=('Jetbrains Mono', 16),
            width=18,
            height=18,
            text_color='#BBBBBB',
            fg_color='#2E2E2E',
            hover_color='#2E2E2E',
            command=lambda: self.zoom(1.1)
        )
        self.zoom_out_button.place(relx=0.0, rely=0.0, anchor='nw', x=58, y=5)

        self.zoom_out_button.configure(cursor='hand2')
        self.zoom_out_button.bind('<Enter>', lambda e: self.zoom_out_button.configure(text_color='#FFFFFF'))
        self.zoom_out_button.bind('<Leave>', lambda e: self.zoom_out_button.configure(text_color='#BBBBBB'))

        self.coords_label = ctk.CTkLabel(
            self.canvas_frame,
            text='',
            font=('Jetbrains Mono', 10),
            fg_color='#2E2E2E',
            text_color='#BBBBBB'
        )
        self.coords_label.place(relx=1.0, rely=0.0, anchor='ne', x=-5, y=5)

        self.canvas.mpl_connect('motion_notify_event', self.on_hover)
        self.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.canvas.mpl_connect('button_press_event', self._on_pan_start)
        self.canvas.mpl_connect('button_release_event', self._on_pan_end)        

        self.winfo_toplevel().bind('<Control-0>', lambda e: self.recenter())


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
            xlim = self.ax.get_xlim()
            x = np.linspace(xlim[0], xlim[1], 400)
            y = np.array([self.logic.evaluate_graph(xi) for xi in x], dtype=float)
        except SyntaxError:
            return

        line, = self.ax.plot(x, y)
        self.plotted_functions.append({'line': line, 'tokens': list(self.logic.tokens)})

        self.canvas.draw()


    def clear_functions(self):

        self.ax.clear()
        self.plotted_functions.clear()

        self.selected_marker = None
        self.selected_label = None

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

         if event.inaxes and self.pan_start:
             self._on_pan_move(event)

         if event.inaxes:
            x, y = event.xdata, event.ydata
            self.coords_label.configure(text=f'x={x:.2f}, y={y:.2f}')
            self.canvas.get_tk_widget().config(cursor='cross')
         else:
            self.coords_label.configure(text='')
            self.canvas.get_tk_widget().config(cursor='arrow')


    def on_scroll(self, event):

        if not event.inaxes:
            return

        factor = 0.9 if event.button == 'up' else 1.1
        self.zoom(factor, center_x=event.xdata, center_y=event.ydata)


    def zoom(self, factor, center_x=None, center_y=None):

        if center_x is None or center_y is None:
            center_x = (self.ax.get_xlim()[0] + self.ax.get_xlim()[1]) / 2
            center_y = (self.ax.get_ylim()[0] + self.ax.get_ylim()[1]) / 2

        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()

        new_width = (xlim[1] - xlim[0]) * factor
        if not (0.001 <= new_width <= 1_000_000):
            return

        left_distance = center_x - xlim[0]
        right_distance = xlim[1] - center_x
        new_xlim = (center_x - left_distance * factor, center_x + right_distance * factor)

        bottom_distance = center_y - ylim[0]
        top_distance = ylim[1] - center_y
        new_ylim = (center_y - bottom_distance * factor, center_y + top_distance * factor)

        self.ax.set_xlim(new_xlim)
        self.ax.set_ylim(new_ylim)

        self._redraw_curves()
        self.canvas.draw_idle()
        self._refresh_tick_labels()


    def recenter(self):

        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)

        self._redraw_curves()
        self.canvas.draw_idle()

        self._refresh_tick_labels()


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

        self.ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
        self.ax.yaxis.set_major_locator(MaxNLocator(nbins=5))

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

        self._refresh_tick_labels()


    def _sync_from_entry(self, event=None):

        text = self.function_entry.get()

        try:
            self.logic.raw_input = text
            self.logic.tokens = self.logic.lexer.tokenize(self.logic.raw_input)
            print(self.logic.tokens)
            self.logic._update_expressions_from_tokens()
        except SyntaxError:
            pass


    def _redraw_curves(self):

            if not self.plotted_functions:
                return

            try:
                xlim = self.ax.get_xlim()
                x = np.linspace(xlim[0], xlim[1], 400)

                for plotted_function in self.plotted_functions:
                    y = np.array([self.logic.evaluate_graph(xi, tokens=plotted_function['tokens']) for xi in x], dtype=float)
                    plotted_function['line'].set_data(x, y)
            except SyntaxError:
                pass


    def _find_nearest_point(self, click_x, click_y):

        closest_function = None
        closest_distance = None
        closest_index = None

        for plotted_function in self.plotted_functions:

            x_data, y_data = plotted_function['line'].get_data()

            distances = np.hypot(x_data - click_x, y_data - click_y)
            index = np.argmin(distances)
            distance = distances[index]

            if closest_distance is None or distance < closest_distance:
                closest_function = plotted_function
                closest_distance = distance
                closest_index = index

        if closest_function is None:
            return None

        closest_x, closest_y = closest_function['line'].get_data()

        return closest_function, closest_x[closest_index], closest_y[closest_index]


    def _show_selected_point(self, nearest):

        if self.selected_marker is not None:
            self.selected_marker.remove()
            self.selected_marker = None

        if self.selected_label is not None:
            self.selected_label.remove()
            self.selected_label = None

        if nearest is None:
            self.canvas.draw_idle()
            return

        plotted_function, x, y = nearest

        self.selected_marker, = self.ax.plot(
            [x], [y],
            marker='o',
            markersize=6,
            color='#FFFFFF',
            markeredgecolor='#000000',
            markeredgewidth=1,
            zorder=5
        )

        self.selected_label = self.ax.annotate(
            f'({x:.3g}, {y:.3g})',
            xy=(x, y),
            xytext=(8, 8),
            textcoords='offset points',
            color='#FFFFFF',
            fontsize=9,
            bbox=dict(boxstyle='round,pad=0.3', fc='#2E2E2E', ec='#555555', lw=1)
        )

        self.canvas.draw_idle()


    def _on_pan_start(self, event):
        if event.inaxes:
            self.pan_start = (event.x, event.y)
            self.pan_start_xlim = self.ax.get_xlim()
            self.pan_start_ylim = self.ax.get_ylim()


    def _on_pan_end(self, event):

        nearest = None

        if self.pan_start is not None:
            distance_moved = np.hypot(event.x - self.pan_start[0], event.y - self.pan_start[1])

            if event.inaxes and distance_moved < 5:
                nearest = self._find_nearest_point(event.xdata, event.ydata)

        self._show_selected_point(nearest)
        
        self.pan_start = None
        self.pan_start_xlim = None
        self.pan_start_ylim = None


    def _on_pan_move(self, event):

        dx_pixels = event.x - self.pan_start[0]
        dy_pixels = event.y - self.pan_start[1]

        inverse = self.ax.transData.inverted()

        origin_data = inverse.transform((0, 0))
        offset_data = inverse.transform((dx_pixels, dy_pixels))

        dx_data = offset_data[0] - origin_data[0]
        dy_data = offset_data[1] - origin_data[1]

        new_xlim = (self.pan_start_xlim[0] - dx_data, self.pan_start_xlim[1] - dx_data)
        new_ylim = (self.pan_start_ylim[0] - dy_data, self.pan_start_ylim[1] - dy_data)

        self.ax.set_xlim(new_xlim)
        self.ax.set_ylim(new_ylim)

        self._redraw_curves()

        self.canvas.draw_idle()
        self._refresh_tick_labels()


    def _refresh_tick_labels(self):

        xlim = self.ax.get_xlim()
        x_range = xlim[1] - xlim[0]

        if x_range < 0.1:
            decimals = 3
        elif x_range < 2:
            decimals = 2
        elif x_range < 5:
            decimals = 1
        else:
            decimals = 0

        x_labels = [f'{t:.{decimals}f}' if t != 0 else '' for t in self.ax.get_xticks()]
        y_labels = [f'{t:.{decimals}f}' if t != 0 else '' for t in self.ax.get_yticks()]
        
        self.ax.set_xticklabels(x_labels)
        self.ax.set_yticklabels(y_labels)