import customtkinter as ctk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from core.exceptions import SyntaxError

class GraphUI(ctk.CTkFrame):

    def __init__(self, parent, logic):

        super().__init__(parent, fg_color='#1F1F1F')

        self.width = 520
        self.height = 620
        self.logic = logic
        self.toggle_state = False
        self.roots_visible = False
        self.secondary_buttons = {}
        self.plotted_functions = []
        self.current_roots = []

        self.point_marker = None
        self.point_label = None

        self.root_markers = None

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
            text='⌖',
            font=('Jetbrains Mono', 16),
            width=18,
            height=18,
            text_color='#BBBBBB',
            fg_color='#2E2E2E',
            hover_color='#2E2E2E',
            command=self.recenter
        )
        self.recenter_button.place(relx=0.0, rely=0.0, anchor='nw', x=1, y=4)

        self.recenter_button.configure(cursor='hand2')
        self.recenter_button.bind('<Enter>', lambda e: self.recenter_button.configure(text_color='#FFFFFF'))
        self.recenter_button.bind('<Leave>', lambda e: self.recenter_button.configure(text_color='#BBBBBB'))        

        self.vertical_separator_1 = ctk.CTkFrame(
            self.canvas_frame,
            width=1,
            height=28,
            fg_color='#444444'
        )
        self.vertical_separator_1.place(relx=0.0, rely=0.0, anchor='nw', x=30, y=5)

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

        self.vertical_separator_1 = ctk.CTkFrame(
            self.canvas_frame,
            width=1,
            height=28,
            fg_color='#444444'
        )
        self.vertical_separator_1.place(relx=0.0, rely=0.0, anchor='nw', x=82, y=5)

        self.toggle_roots_button = ctk.CTkButton(
            self.canvas_frame,
            text='☉',
            font=('Jetbrains Mono', 16),
            width=18,
            height=18,
            text_color='#BBBBBB',
            fg_color='#2E2E2E',
            hover_color='#2E2E2E',
            command=self.toggle_roots
        )
        self.toggle_roots_button.place(relx=0.0, rely=0.0, anchor='nw', x=83, y=7)

        self.toggle_roots_button.configure(cursor='hand2')

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
        self.function_entry.bind('<KeyRelease>', self._handle_key_release)
        self.function_entry.bind('<BackSpace>', self._handle_backspace)
        self.function_entry.bind('<Return>', self.plot_function)        

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
             ('⌫', 'backspace'),
             ('.', 'decimal'),
             ('+', 'operator'),
             (('x²', '√'), 'function'),
             (('x³', '∛'), 'function'),
             (('xʸ', '|x|'), 'function')),

            (('1', 'number'),
             ('2', 'number'),
             ('3', 'number'),
             ('-', 'operator'),
             (('log', '10ˣ'), 'function'),
             (('log₂', '2ˣ'), 'function'),
             (('ln', 'eˣ'), 'function')),

            (('4', 'number'),
             ('5', 'number'),
             ('6', 'number'),
             ('×', 'operator'),
             (('sin', 'sin⁻¹'), 'function'),
             (('cos', 'cos⁻¹'), 'function'),
             (('tan', 'tan⁻¹'), 'function')),

            (('7', 'number'),
             ('8', 'number'),
             ('9', 'number'),
             ('÷', 'operator'),
             (('csc', 'csc⁻¹'), 'function'),
             (('sec', 'sec⁻¹'), 'function'),
             (('cot', 'cot⁻¹'), 'function')),

            (('0', 'number'),
             ('x', 'variable'),
             ('(', 'parenthesis'),
             (')', 'parenthesis'),
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
                elif type == 'backspace':
                    button = ctk.CTkButton(
                        self.buttons_frame,
                        text=text,
                        font=('Jetbrains Mono', 20),
                        fg_color='#262626',
                        hover_color='#C42B2B',
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
                elif type == 'number':
                    button = ctk.CTkButton(
                        self.buttons_frame,
                        text=text,
                        font=('Jetbrains Mono', 20),
                        fg_color='#3C3C3C',
                        hover_color='#4A4A4A',
                        command=lambda t=text: self._graph_click(t)
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
        for c in range(len(graph_buttons[0])):
            self.buttons_frame.grid_columnconfigure(c, weight=1, uniform='button_columns')


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

        self.logic.clear()
        self.update_typing_display()
        self._redraw_curves()
        self.canvas.draw()


    def clear_functions(self):

        self.ax.clear()
        self.plotted_functions.clear()
        self.current_roots = []

        self.point_marker = None
        self.point_label = None
        self.root_markers = None

        self._style_axes()
        self.canvas.draw()


    def handle_symbol(self, symbol):

        if symbol == 'C':
            self.logic.clear()
        elif symbol == '⌫':
            self.logic.backspace()
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


    def toggle_roots(self):

        self.roots_visible = not self.roots_visible

        if self.roots_visible:
            self.toggle_roots_button.configure(text_color='#FFFFFF')
            self._show_roots(self.current_roots)
        else:
            self.toggle_roots_button.configure(text_color='#BBBBBB')
            self._show_roots([])


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


    def _handle_key_release(self, event=None):

        if event is None:
            return

        if event.keysym in ('Return', 'BackSpace'):
            return None

        new_text = self.function_entry.get()
        old_text = self.logic.display_expression

        if new_text == old_text:
            return

        if len(new_text) > len(old_text) and new_text.startswith(old_text):
            added = new_text[len(old_text):]
            
            try:
                self.logic.append(added)
            except SyntaxError:
                pass
            self.update_typing_display()
        else:
            self.function_entry.icursor('end')
            try:
                self.logic.raw_input = new_text
                self.logic.tokens = self.logic.lexer.tokenize(new_text)
                self.logic._update_expressions_from_tokens()
            except SyntaxError:
                pass


    def _handle_backspace(self, event=None):

            self.logic.backspace()
            self.update_typing_display()

            return 'break'


    def _redraw_curves(self):

        if not self.plotted_functions:
            self.current_roots = []
            return

        try:
            xlim = self.ax.get_xlim()
            x = np.linspace(xlim[0], xlim[1], 400)
            self.current_roots = []

            for plotted_function in self.plotted_functions:
                y = np.array([self.logic.evaluate_graph(xi, tokens=plotted_function['tokens']) for xi in x], dtype=float)
                plotted_function['line'].set_data(x, y)
                self.current_roots.extend(self._find_roots(x, y, plotted_function['tokens']))

            if self.roots_visible:
                self._show_roots(self.current_roots)

        except SyntaxError:
            pass


    def _find_roots(self, x, y, tokens):

        roots = []
        finite_y = y[~np.isnan(y)]
        y_range = finite_y.max() - finite_y.min() if finite_y.size else 1.0
        root_tolerance = max(y_range * 0.05, 1e-6)

        for i in range(len(y) - 1):
            y1, y2 = y[i], y[i+1]
            x1, x2 = x[i], x[i+1]

            if np.isnan(y1) or np.isnan(y2):
                continue

            if not (y1 == 0 or y1 * y2 < 0):
                continue

            if abs(y1) > root_tolerance and abs(y2) > root_tolerance:
                continue

            mid_x = None
            mid_y = None

            for _ in range(50):
                mid_x = (x1 + x2) / 2
                mid_y = self.logic.evaluate_graph(mid_x, tokens=tokens)

                if mid_y is None or np.isnan(mid_y):
                    mid_x = None
                    break

                if mid_y == 0 or abs(x2 - x1) < 1e-10:
                    break

                if (y1 <= 0 <= mid_y) or (y1 >= 0 >= mid_y):
                    x2, y2 = mid_x, mid_y
                else:
                    x1, y1 = mid_x, mid_y

            if mid_x is not None and mid_y is not None and abs(mid_y) < 1e-6:
                roots.append(0.0 if abs(mid_x) < 1e-4 else round(mid_x, 6))

        for i in range(1, len(y) - 1):
            y0, y1, y2 = y[i - 1], y[i], y[i + 1]

            if np.isnan(y0) or np.isnan(y1) or np.isnan(y2):
                continue

            if abs(y1) > root_tolerance * 0.2:
                continue

            is_local_extreme = (y0 > y1 < y2) or (y0 < y1 > y2)
            if not is_local_extreme:
                continue

            x0, x1, x2 = x[i - 1], x[i], x[i + 1]

            best_x, best_y = x1, y1
            for _ in range(15):
                mid_left = (x0 + x1) / 2
                mid_right = (x1 + x2) / 2
                y_left = self.logic.evaluate_graph(mid_left, tokens=tokens)
                y_right = self.logic.evaluate_graph(mid_right, tokens=tokens)

                if y_left is None or y_right is None or np.isnan(y_left) or np.isnan(y_right):
                    break

                if abs(y_left) < abs(best_y):
                    best_x, best_y = mid_left, y_left
                if abs(y_right) < abs(best_y):
                    best_x, best_y = mid_right, y_right

                if abs(y_left) < abs(y_right):
                    x2, x1 = x1, mid_left
                else:
                    x0, x1 = x1, mid_right

            if abs(best_y) < 1e-6:
                already_found = any(abs(root - best_x) < 1e-3 for root in roots)
                if not already_found:
                    roots.append(0.0 if abs(best_x) < 1e-4 else round(best_x, 6))

        return roots


    def _find_nearest_point(self, click_x, click_y):

        closest_function = None
        closest_distance = None
        closest_index = None

        max_distance = (self.ax.get_xlim()[1] - self.ax.get_xlim()[0]) * 0.02

        for plotted_function in self.plotted_functions:

            x_data, y_data = plotted_function['line'].get_data()

            distances = np.hypot(x_data - click_x, y_data - click_y)
            index = np.argmin(distances)
            distance = distances[index]

            if closest_distance is None or distance < closest_distance:
                closest_function = plotted_function
                closest_distance = distance
                closest_index = index

        if closest_function is None or closest_distance > max_distance:
            return None

        closest_x, closest_y = closest_function['line'].get_data()

        return closest_function, closest_x[closest_index], closest_y[closest_index]


    def _show_roots(self, roots):

        if self.root_markers is None:
            self.root_markers = []

        if not self.roots_visible:
            for marker, label in self.root_markers:
                marker.set_visible(False)
                label.set_visible(False)
            self.canvas.draw_idle()
            return

        xlim = self.ax.get_xlim()
        x_range = xlim[1] - xlim[0]
        match_tolerance = max(x_range * 0.01, 1e-3)
        matched_markers = set()

        for root in roots:
            closest_index = None
            closest_distance = match_tolerance

            for index, (marker, _) in enumerate(self.root_markers):
                if index in matched_markers:
                    continue

                marker_x = marker.get_xdata()[0]
                distance = abs(marker_x - root)
                if distance < closest_distance:
                    closest_index = index
                    closest_distance = distance

            if closest_index is None:
                root_marker, = self.ax.plot(
                    [root], [0],
                    marker='o',
                    markersize=6,
                    color='#FFFFFF',
                    markeredgecolor='#000000',
                    markeredgewidth=1,
                    zorder=5
                )

                root_label = self.ax.annotate(
                    f'({root:.3g}, 0)',
                    xy=(root, 0),
                    xytext=(8, 8),
                    textcoords='offset points',
                    color='#FFFFFF',
                    fontsize=9,
                    fontfamily='monospace',
                    bbox=dict(
                        boxstyle='round,pad=0.3',
                        fc='#2E2E2E',
                        ec='#555555',
                        lw=0.5
                    )
                )
                self.root_markers.append((root_marker, root_label))
                closest_index = len(self.root_markers) - 1

            marker, label = self.root_markers[closest_index]
            marker.set_data([root], [0])
            marker.set_visible(True)
            label.xy = (root, 0)
            label.set_text(f'({root:.3g}, 0)')
            label.set_visible(True)
            matched_markers.add(closest_index)

        for index, (marker, label) in enumerate(self.root_markers):
            marker_x = marker.get_xdata()[0]
            in_range = xlim[0] <= marker_x <= xlim[1]
            if index not in matched_markers:
                marker.set_visible(in_range)
                label.set_visible(in_range)

        self.canvas.draw_idle()


    def _show_selected_point(self, nearest):

        if self.point_marker is not None:
            self.point_marker.remove()
            self.point_marker = None

        if self.point_label is not None:
            self.point_label.remove()
            self.point_label = None

        if nearest is None:
            self.canvas.draw_idle()
            return

        plotted_function, x, y = nearest

        self.point_marker, = self.ax.plot(
            [x], [y],
            marker='o',
            markersize=6,
            color='#FFFFFF',
            markeredgecolor='#000000',
            markeredgewidth=1,
            zorder=5
        )

        self.point_label = self.ax.annotate(
            f'({x:.3g}, {y:.3g})',
            xy=(x, y),
            xytext=(8, 8),
            textcoords='offset points',
            color='#FFFFFF',
            fontsize=9,
            fontfamily='monospace',
            bbox=dict(
                boxstyle='round,pad=0.3',
                fc='#2E2E2E',
                ec='#555555',
                lw=0.5
            )
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