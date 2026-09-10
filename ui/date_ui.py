import customtkinter as ctk
from datetime import date

class DateUI(ctk.CTkFrame):

    def __init__(self, parent, logic):

        super().__init__(parent, fg_color='#2E2E2E')
        self.width = 460
        self.height = 315
        self.logic = logic

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_panel()

        self._calculate()


    def _build_panel(self):

        self.panel_frame = ctk.CTkFrame(self, fg_color='#1F1F1F', corner_radius=0)
        self.panel_frame.grid(row=0, column=0, sticky='nsew')

        self.panel_frame.grid_columnconfigure(0, weight=1)
        self.panel_frame.grid_rowconfigure(0, weight=0)
        self.panel_frame.grid_rowconfigure(1, weight=0)
        self.panel_frame.grid_rowconfigure(2, weight=0)
        self.panel_frame.grid_rowconfigure(3, weight=0)
        self.panel_frame.grid_rowconfigure(4, weight=0)

        self.inputs_frame = ctk.CTkFrame(self.panel_frame, fg_color='#1F1F1F', corner_radius=0)
        self.inputs_frame.grid(row=0, column=0, sticky='nsew')

        self.inputs_frame.grid_columnconfigure(0, weight=1)
        self.inputs_frame.grid_columnconfigure(1, weight=1)

        self.from_entries = self._build_date_row(self.inputs_frame, 'From:', column=0)
        self.to_entries = self._build_date_row(self.inputs_frame, 'To:', column=1)

        top_separator = ctk.CTkFrame(self.panel_frame, height=1, fg_color='#333333')
        top_separator.grid(row=1, column=0, sticky='ew', pady=6)

        self.result_label = ctk.CTkLabel(
            self.panel_frame, 
            text='', 
            font=('Jetbrains Mono', 22, 'bold'), 
            text_color='#FFFFFF'
        )
        self.result_label.grid(row=2, column=0, pady=4)

        bottom_separator = ctk.CTkFrame(self.panel_frame, height=1, fg_color='#333333')
        bottom_separator.grid(row=3, column=0, sticky='ew', pady=6)

        self.breakdown_frame = ctk.CTkFrame(self.panel_frame, fg_color='#1F1F1F', corner_radius=0)
        self.breakdown_frame.grid(row=4, column=0, sticky='nsew')

        self.breakdown_frame.grid_columnconfigure(0, weight=1)

        breakdown_header = ctk.CTkLabel(
            self.breakdown_frame, 
            text='Breakdown', 
            font=('Jetbrains Mono', 12), 
            text_color='#777777'
        )
        breakdown_header.grid(row=0, column=0, pady=(4, 6))

        self.days_label = ctk.CTkLabel(
            self.breakdown_frame, 
            text='', 
            font=('Jetbrains Mono', 14), 
            text_color='#CCCCCC'
        )
        self.days_label.grid(row=1, column=0, pady=1)

        self.months_label = ctk.CTkLabel(
            self.breakdown_frame, 
            text='', 
            font=('Jetbrains Mono', 14), 
            text_color='#CCCCCC'
        )
        self.months_label.grid(row=2, column=0, pady=1)

        self.years_label = ctk.CTkLabel(
            self.breakdown_frame, 
            text='', 
            font=('Jetbrains Mono', 14), 
            text_color='#CCCCCC'
        )
        self.years_label.grid(row=3, column=0, pady=1)


    def _build_date_row(self, parent, label_text, column):

        frame = ctk.CTkFrame(parent, fg_color='#1F1F1F', corner_radius=0)
        frame.grid(row=0, column=column, sticky='nsew', padx=8, pady=8)

        label = ctk.CTkLabel(
            frame,
            text=label_text, 
            font=('Jetbrains Mono', 12), 
            text_color='#777777'
        )
        label.pack(anchor='w', pady=(0, 4))

        fields_frame = ctk.CTkFrame(frame, fg_color='#1F1F1F', corner_radius=0)
        fields_frame.pack()

        day_entry = ctk.CTkEntry(
            fields_frame, 
            width=44, 
            font=('Jetbrains Mono', 16),
            fg_color='#242424',
            border_width=1, 
            border_color='#4A4A4A',
            placeholder_text='DD'
        )
        day_entry.grid(row=0, column=0, padx=2)

        month_entry = ctk.CTkEntry(
            fields_frame,
            width=44, 
            font=('Jetbrains Mono', 16),
            fg_color='#242424', 
            border_width=1, 
            border_color='#4A4A4A',
            placeholder_text='MM'
        )
        month_entry.grid(row=0, column=1, padx=2)

        year_entry = ctk.CTkEntry(
            fields_frame, 
            width=64, 
            font=('Jetbrains Mono', 16),
            fg_color='#242424', 
            border_width=1, 
            border_color='#4A4A4A',
            placeholder_text='YYYY'
        )
        year_entry.grid(row=0, column=2, padx=2)

        today = date.today()
        day_entry.insert(0, str(today.day))
        month_entry.insert(0, str(today.month))
        year_entry.insert(0, str(today.year))

        for entry in (day_entry, month_entry, year_entry):
            entry.bind('<KeyRelease>', self._calculate)

        return {
            'day': day_entry, 
            'month': month_entry, 
            'year': year_entry
        }


    def _read_date(self, entries):

        try:
            day = int(entries['day'].get())
            month = int(entries['month'].get())
            year = int(entries['year'].get())
        except ValueError:
            return None

        return self.logic.validate_date(day, month, year)


    def _calculate(self, event=None):

        from_date = self._read_date(self.from_entries)
        to_date = self._read_date(self.to_entries)

        if from_date is None or to_date is None:
            self.result_label.configure(text='Invalid date')
            self.days_label.configure(text='')
            self.months_label.configure(text='')
            self.years_label.configure(text='')
            return

        result = self.logic.calculate_difference(from_date, to_date)

        self.result_label.configure(
            text=f'{result['years']} Years, {result['months']} Months, {result['days']} Days'
        )
        self.days_label.configure(text=f'Days:   {result['total_days']}')
        self.months_label.configure(text=f'Months: {result['total_months']:.2f}')
        self.years_label.configure(text=f'Years:  {result['total_years']:.2f}')