import customtkinter as ctk

COMMON_CONVERSIONS = {
    'Length': (
        (('Meters', 'm'), ('Feet', 'ft')), (('Kilometers', 'km'), ('Miles', 'mi')), (('Centimeters', 'cm'), ('Inches', 'in')),
        (('Feet', 'ft'), ('Meters', 'm')), (('Miles', 'mi'), ('Kilometers', 'km')), (('Inches', 'in'), ('Centimeters', 'cm')),
    ),
    'Weight': (
        (('Kilograms', 'kg'), ('Pounds', 'lb')), (('Grams', 'g'), ('Ounces', 'oz')), (('Tonnes', 't'), ('Kilograms', 'kg')),
        (('Pounds', 'lb'), ('Kilograms', 'kg')), (('Ounces', 'oz'), ('Grams', 'g')), (('Kilograms', 'kg'), ('Tonnes', 't')),
    ),
    'Temperature': (
        (('Celsius', '°C'), ('Fahrenheit', '°F')), (('Celsius', '°C'), ('Kelvin', 'K')), (('Fahrenheit', '°F'), ('Kelvin', 'K')),
        (('Fahrenheit', '°F'), ('Celsius', '°C')), (('Kelvin', 'K'), ('Celsius', '°C')), (('Kelvin', 'K'), ('Fahrenheit', '°F')),
    ),
    'Time': (
        (('Minutes', 'min'), ('Seconds', 'sec')), (('Hours', 'hr'), ('Minutes', 'min')), (('Days', 'day'), ('Hours', 'hr')),
        (('Seconds', 'sec'), ('Minutes', 'min')), (('Minutes', 'min'), ('Hours', 'hr')), (('Hours', 'hr'), ('Days', 'day')),
    ),
    'Area': (
        (('Square Meters', 'm²'), ('Square Feet', 'ft²')), (('Square Kilometers', 'km²'), ('Square Miles', 'mi²')), (('Square Centimeters', 'cm²'), ('Square Inches', 'in²')),
        (('Square Feet', 'ft²'), ('Square Meters', 'm²')), (('Square Miles', 'mi²'), ('Square Kilometers', 'km²')), (('Square Inches', 'in²'), ('Square Centimeters', 'cm²')),
    ),
    'Speed': (
        (('Kilometers/Hour', 'km/h'), ('Miles/Hour', 'mph')), (('Meters/Second', 'm/s'), ('Feet/Second', 'ft/s')), (('Knots', 'kn'), ('Miles/Hour', 'mph')),
        (('Miles/Hour', 'mph'), ('Kilometers/Hour', 'km/h')), (('Feet/Second', 'ft/s'), ('Meters/Second', 'm/s')), (('Miles/Hour', 'mph'), ('Knots', 'kn')),
    ),
    'Volume': (
        (('Liters', 'L'), ('Gallons', 'gal')), (('Milliliters', 'ml'), ('Cubic Meters', 'm³')), (('Liters', 'L'), ('Quarts', 'qt')),
        (('Gallons', 'gal'), ('Liters', 'L')), (('Cubic Meters', 'm³'), ('Milliliters', 'ml')), (('Quarts', 'qt'), ('Liters', 'L')),
    ),
    'Energy': (
        (('Joules', 'J'), ('Kilocalories', 'kcal')), (('Kilojoules', 'kJ'), ('BTU', 'BTU')), (('Kilowatt-Hours', 'kWh'), ('Joules', 'J')),
        (('Kilocalories', 'kcal'), ('Joules', 'J')), (('BTU', 'BTU'), ('Kilojoules', 'kJ')), (('Joules', 'J'), ('Kilowatt-Hours', 'kWh')),
    ),
    'Data': (
        (('Megabytes', 'MB'), ('Gigabytes', 'GB')), (('Gigabytes', 'GB'), ('Terabytes', 'TB')), (('Bytes', 'B'), ('Kilobytes', 'KB')),
        (('Gigabytes', 'GB'), ('Megabytes', 'MB')), (('Terabytes', 'TB'), ('Gigabytes', 'GB')), (('Kilobytes', 'KB'), ('Bytes', 'B')),
    ),
}

class UnitUI(ctk.CTkFrame):

    def __init__(self, parent, logic):

        super().__init__(parent, fg_color='#292929')
        self.width = 750
        self.height = 390
        self.logic = logic

        self.categories = ('Length', 'Weight', 'Temperature', 'Time', 'Speed', 'Area', 'Volume', 'Energy', 'Data')
        self.current_category = self.categories[0]
        self.category_buttons = {}
        self.reference_labels = []
        self.conversion_shortcuts = []

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_converter()

        self.winfo_toplevel().bind('<Button-1>', self._handle_entry_outside_click, add='+')

        self._select_category(self.current_category)


    def _build_sidebar(self):

        self.buttons_frame = ctk.CTkFrame(self, width=180, fg_color='#1F1F1F', corner_radius=0)
        self.buttons_frame.grid(row=0, column=0, sticky='nsew', pady=(0, 2))

        for i, category in enumerate(self.categories):
            button = ctk.CTkButton(
                self.buttons_frame,
                text=category,
                font=('Jetbrains Mono', 16),
                fg_color='#242424',
                hover_color='#2E2E2E',
                border_width=1,
                border_color='#333333',
                command=lambda c=category: self._select_category(c)
            )
            button.grid(row=i, column=0, sticky='ew', padx=5, pady=5)
            button.configure(cursor='hand2')
            self.buttons_frame.grid_rowconfigure(i, weight=1)

            self.category_buttons[category] = button

        self.buttons_frame.grid_columnconfigure(0, weight=1)


    def _build_converter(self):

        self.converter_frame = ctk.CTkFrame(self, fg_color='#292929', corner_radius=0)
        self.converter_frame.grid(row=0, column=1, sticky='nsew')

        self.converter_frame.grid_columnconfigure(0, weight=1)
        self.converter_frame.grid_rowconfigure(0, weight=0)
        self.converter_frame.grid_rowconfigure(1, weight=0)
        self.converter_frame.grid_rowconfigure(2, weight=0)
        self.converter_frame.grid_rowconfigure(3, weight=0)
        self.converter_frame.grid_rowconfigure(4, weight=1)

        self.entry_frame = ctk.CTkFrame(self.converter_frame, fg_color='#292929', corner_radius=0)
        self.entry_frame.grid(row=0, column=0, sticky='nsew')

        self.entry_frame.grid_columnconfigure(0, weight=1)
        self.entry_frame.grid_columnconfigure(1, weight=0)
        self.entry_frame.grid_columnconfigure(2, weight=1)

        self.from_label = ctk.CTkLabel(
            self.entry_frame,
            text='From:',
            font=('Jetbrains Mono', 12),
            text_color='#777777'
        )
        self.from_label.grid(row=0, column=0, sticky='w', padx=8, pady=(3, 0))

        self.from_entry = ctk.CTkEntry(
            self.entry_frame,
            font=('Jetbrains Mono', 20),
            fg_color='#242424',
            border_width=1,
            border_color='#4A4A4A',
            height=44
        )
        self.from_entry.grid(row=1, column=0, sticky='ew', padx=8, pady=(2, 6))
        self.from_entry.bind('<KeyRelease>', self._convert)

        self.from_unit_menu = ctk.CTkOptionMenu(
            self.entry_frame,
            values=[],
            font=('Jetbrains Mono', 14),
            fg_color='#242424',
            button_color='#2E2E2E',
            button_hover_color='#383838',
            text_color='#CCCCCC',
            dropdown_fg_color='#242424',
            dropdown_hover_color='#333333',
            dropdown_text_color='#CCCCCC',
            dynamic_resizing=False,
            command=self._convert
        )
        self.from_unit_menu.grid(row=2, column=0, sticky='ew', padx=8, pady=(0, 10))
        self.from_unit_menu.configure(cursor='hand2')

        self.swap_button = ctk.CTkButton(
            self.entry_frame,
            text='⇄',
            font=('Jetbrains Mono', 20),
            fg_color='#262626',
            hover_color='#3A3A3A',
            text_color='#AAAAAA',
            border_width=1,
            border_color='#333333',
            width=40,
            command=self._swap_units
        )
        self.swap_button.grid(row=1, column=1, padx=8)
        self.swap_button.configure(cursor='hand2')

        self.to_label = ctk.CTkLabel(
            self.entry_frame,
            text='To:',
            font=('Jetbrains Mono', 12),
            text_color='#777777'
        )
        self.to_label.grid(row=0, column=2, sticky='w', padx=8, pady=(3, 0))

        self.to_entry = ctk.CTkEntry(
            self.entry_frame,
            font=('Jetbrains Mono', 20),
            fg_color='#242424',
            text_color='#999999',
            border_width=0,
            height=44
        )
        self.to_entry.grid(row=1, column=2, sticky='ew', padx=8, pady=(2, 6))
        self.to_entry.configure(state='readonly')

        self.to_unit_menu = ctk.CTkOptionMenu(
            self.entry_frame,
            values=[],
            font=('Jetbrains Mono', 14),
            fg_color='#242424',
            button_color='#2E2E2E',
            button_hover_color='#383838',
            text_color='#CCCCCC',
            dropdown_fg_color='#242424',
            dropdown_hover_color='#333333',
            dropdown_text_color='#CCCCCC',
            dynamic_resizing=False,
            command=self._convert
        )
        self.to_unit_menu.grid(row=2, column=2, sticky='ew', padx=8, pady=(0, 10))
        self.to_unit_menu.configure(cursor='hand2')

        top_separator = ctk.CTkFrame(self.converter_frame, height=1, fg_color='#333333')
        top_separator.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(0, 3))

        self.reference_frame = ctk.CTkFrame(self.converter_frame, fg_color='#292929', corner_radius=0)
        self.reference_frame.grid(row=2, column=0, sticky='nsew')

        self.reference_frame.grid_columnconfigure(0, weight=1)

        self.reference_header = ctk.CTkLabel(
                    self.reference_frame,
                    text='Reference Table',
                    font=('Jetbrains Mono', 12),
                    text_color='#777777'
                )
        self.reference_header.grid(row=0, column=0, columnspan=3)

        for i in range(3):
            label = ctk.CTkLabel(
                self.reference_frame,
                text='',
                font=('Jetbrains Mono', 15),
                text_color='#CCCCCC'
            )
            label.grid(row=1 + i, column=0, columnspan=3)
            self.reference_labels.append(label)

        bottom_separator = ctk.CTkFrame(self.converter_frame, height=1, fg_color='#333333')
        bottom_separator.grid(row=3, column=0, columnspan=3, sticky='ew', pady=3)

        self.shortcuts_frame = ctk.CTkFrame(self.converter_frame, fg_color='#292929', corner_radius=0)
        self.shortcuts_frame.grid(row=4, column=0, sticky='nsew')

        self.shortcuts_frame.grid_columnconfigure(0, weight=1)
        self.shortcuts_frame.grid_rowconfigure(1, weight=1)

        self.shortcuts_header = ctk.CTkLabel(
                            self.shortcuts_frame,
                            text='Common Conversions',
                            font=('Jetbrains Mono', 12),
                            text_color='#777777'
                        )
        self.shortcuts_header.grid(row=0, column=0, columnspan=3)

        self.shortcuts_grid = ctk.CTkFrame(self.shortcuts_frame, fg_color='#292929', corner_radius=0)
        self.shortcuts_grid.grid(row=1, column=0, sticky='nsew', padx=8, pady=(0, 8))

        for column in range(3):
            self.shortcuts_grid.grid_columnconfigure(column, weight=1)
        for row in range(2):
            self.shortcuts_grid.grid_rowconfigure(row, weight=1)

        for i in range(6):
            button = ctk.CTkButton(
                self.shortcuts_grid,
                text='',
                font=('Jetbrains Mono', 15),
                fg_color='#242424',
                hover_color='#2E2E2E',
                text_color='#CCCCCC',
                border_width=1,
                border_color='#333333',
                command=lambda i=i: self._apply_shortcut(i)
            )
            button.grid(row=i // 3, column=i % 3, sticky='ew', padx=5, pady=1)
            self.conversion_shortcuts.append(button)


    def _select_category(self, category):

        self.current_category = category

        for c, button in self.category_buttons.items():
            button.configure(fg_color='#3C3C3C' if c == category else '#2A2A2A')

        units = self.logic.get_units(category)

        self.from_unit_menu.configure(values=units)
        self.to_unit_menu.configure(values=units)
        self.from_unit_menu.set(units[0])
        self.to_unit_menu.set(units[1])

        self.from_entry.delete(0, 'end')
        self._set_result('')
        self._update_reference_table()
        self._update_shortcuts()


    def _swap_units(self):

        from_unit = self.from_unit_menu.get()
        to_unit = self.to_unit_menu.get()

        self.from_unit_menu.set(to_unit)
        self.to_unit_menu.set(from_unit)

        self.from_entry.delete(0, 'end')
        self.from_entry.insert(0, self.to_entry.get())

        self._convert()


    def _convert(self, _=None):

        text = self.from_entry.get()

        try:
            value = float(text)
        except ValueError:
            self._update_reference_table()
            self._set_result('')
            return

        from_unit = self.from_unit_menu.get()
        to_unit = self.to_unit_menu.get()

        result = self.logic.convert(self.current_category, value, from_unit, to_unit)

        self._set_result('' if result is None else f'{result:.10g}')
        self._update_reference_table()


    def _update_reference_table(self):

        from_unit = self.from_unit_menu.get()
        to_unit = self.to_unit_menu.get()

        for label, factor in zip(self.reference_labels, (1, 10, 100)):
            result = self.logic.convert(self.current_category, factor, from_unit, to_unit)
            if result is None:
                label.configure(text='')
            else:
                label.configure(text=f'{factor} {from_unit}  =  {result:.6g} {to_unit}')


    def _update_shortcuts(self):

        conversions = COMMON_CONVERSIONS.get(self.current_category, [])

        for button, shortcut in zip(self.conversion_shortcuts, conversions):
            (_, from_symbol), (_, to_symbol) = shortcut
            button.configure(text=f'{from_symbol} → {to_symbol}')


    def _apply_shortcut(self, index):

        conversions = COMMON_CONVERSIONS.get(self.current_category, [])

        (from_name, _), (to_name, _) = conversions[index]
        self.from_unit_menu.set(from_name)
        self.to_unit_menu.set(to_name)

        self._convert()


    def _set_result(self, text):
        self.to_entry.configure(state='normal')
        self.to_entry.delete(0, 'end')
        self.to_entry.insert(0, text)
        self.to_entry.configure(state='readonly')


    def _handle_entry_outside_click(self, event):

        widget = event.widget
        while widget is not None:
            if widget == self.from_entry:
                return
            widget = getattr(widget, 'master', None)

        self.focus_set()