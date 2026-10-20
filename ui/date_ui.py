import customtkinter as ctk
from ctkdlib import CTkCalendar
from datetime import date

class DateUI(ctk.CTkFrame):

    def __init__(self, parent, logic):

        super().__init__(parent, fg_color='#2E2E2E')

        self.width = 600
        self.height = 500
        self.logic = logic

        self.selected_dates = {}

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self._build_panel()

        self._calculate()


    def _build_panel(self):

        self.inputs_frame = ctk.CTkFrame(self, fg_color='#2E2E2E', corner_radius=0)
        self.inputs_frame.grid(row=0, column=0, sticky='nsew')

        self.inputs_frame.grid_columnconfigure(0, weight=1)
        self.inputs_frame.grid_columnconfigure(1, weight=1)

        self.from_entries, self.from_calendar = self._build_date_picker(self.inputs_frame, 'From:', column=0)
        self.to_entries, self.to_calendar = self._build_date_picker(self.inputs_frame, 'To:', column=1)

        self.summary_frame = ctk.CTkFrame(self, fg_color='#1F1F1F', corner_radius=0)
        self.summary_frame.grid(row=1, column=0, sticky='nsew', pady=(0, 16))

        self.summary_frame.grid_columnconfigure(0, weight=0)
        self.summary_frame.grid_columnconfigure(1, weight=1)
        self.summary_frame.grid_columnconfigure(2, weight=0)

        self.from_date_label = ctk.CTkLabel(
            self.summary_frame,
            text='',
            width=100,
            anchor='w',
            font=('Jetbrains Mono', 13),
            text_color='#AAAAAA'
        )
        self.from_date_label.grid(row=1, column=0, sticky='w', padx=(24, 6), pady=(14, 6))

        self.track_label = ctk.CTkLabel(
            self.summary_frame,
            text='●' + '━' * 22 + '●',
            font=('Jetbrains Mono', 13),
            text_color='#888888'
        )
        self.track_label.grid(row=1, column=1, sticky='ew', padx=12, pady=(14, 6))

        self.to_date_label = ctk.CTkLabel(
            self.summary_frame,
            text='',
            width=100,
            anchor='e',
            font=('Jetbrains Mono', 13),
            text_color='#AAAAAA'
        )
        self.to_date_label.grid(row=1, column=2, sticky='e', padx=(6, 24), pady=(14, 6))

        self.result_label = ctk.CTkLabel(
            self.summary_frame,
            text='',
            font=('Jetbrains Mono', 20, 'bold'),
            text_color='#FFFFFF'
        )
        self.result_label.grid(row=2, column=0, columnspan=3, pady=(4, 4))

        self.breakdown_label = ctk.CTkLabel(
            self.summary_frame,
            text='',
            font=('Jetbrains Mono', 13),
            text_color='#888888'
        )
        self.breakdown_label.grid(row=3, column=0, columnspan=3, pady=(0, 10))


    def _build_date_picker(self, parent, label_text, column):

        date_frame = ctk.CTkFrame(parent, fg_color='#2E2E2E', corner_radius=0)
        date_frame.grid(row=0, column=column, sticky='nsew', padx=8, pady=8)

        fields_frame = ctk.CTkFrame(date_frame, fg_color='#2E2E2E', corner_radius=0)
        fields_frame.pack()

        label = ctk.CTkLabel(
            fields_frame,
            text=label_text, 
            font=('Jetbrains Mono', 12), 
            text_color='#777777'
        )
        label.grid(row=0, column=0, padx=(0, 6))

        day_entry = ctk.CTkEntry(
            fields_frame, 
            width=30, 
            font=('Jetbrains Mono', 14),
            fg_color='#292929',
            border_width=1, 
            border_color='#4A4A4A',
            justify='center'
        )
        day_entry.grid(row=0, column=1, padx=2)

        slash_label_1 = ctk.CTkLabel(
            fields_frame,
            text='/',
            font=('Jetbrains Mono', 16),
            text_color='#CCCCCC'
        )
        slash_label_1.grid(row=0, column=2, padx=2)

        month_entry = ctk.CTkEntry(
            fields_frame,
            width=30, 
            font=('Jetbrains Mono', 14),
            fg_color='#292929', 
            border_width=1, 
            border_color='#4A4A4A',
            justify='center'
        )
        month_entry.grid(row=0, column=3, padx=2)

        slash_label_2 = ctk.CTkLabel(
            fields_frame,
            text='/',
            font=('Jetbrains Mono', 16),
            text_color='#CCCCCC'
        )
        slash_label_2.grid(row=0, column=4, padx=2)

        year_entry = ctk.CTkEntry(
            fields_frame, 
            width=48, 
            font=('Jetbrains Mono', 14),
            fg_color='#292929', 
            border_width=1, 
            border_color='#4A4A4A',
            justify='center'
        )
        year_entry.grid(row=0, column=5, padx=2)

        entries = {
            'day': day_entry, 
            'month': month_entry, 
            'year': year_entry
        }

        calendar = CTkCalendar(
            date_frame,
            width=300,
            height=270,
            font=('Jetbrains Mono', 12),
            fg_color='#1F1F1F',
            header_color='#2A2A2A',
            header_text_color='#FFFFFF',
            text_color='#DDDDDD',
            hover_color='#3C3C3C',
            select_color='#E07B1A',
            corner_radius=6,
            command=lambda picked: self._pick_date(entries, calendar, picked)
        )
        calendar.pack(pady=8)

        self._add_year_buttons(calendar)

        today = date.today()
        day_entry.insert(0, str(today.day))
        month_entry.insert(0, str(today.month))
        year_entry.insert(0, str(today.year))

        for entry in (day_entry, month_entry, year_entry):
            entry.bind('<KeyRelease>', self._handle_key_release)

        return entries, calendar


    def _add_year_buttons(self, calendar):

        for text, side, step, neighbor in (('«', 'left', -1, calendar.left), ('»', 'right', 1, calendar.right)):
            year_button = ctk.CTkButton(
                calendar.header_frame,
                text=text,
                width=25,
                fg_color='transparent',
                hover=False,
                font=('Jetbrains Mono', 18),
                text_color='#FFFFFF',
                command=lambda s=step: self._jump_years(calendar, s)
            )
            year_button.pack(side=side, before=neighbor, pady=(0, 3))


    def _read_date(self, entries):

        try:
            day = int(entries['day'].get())
            month = int(entries['month'].get())
            year = int(entries['year'].get())
        except ValueError:
            return None

        return self.logic.validate_date(day, month, year)


    def _pick_date(self, entries, calendar, picked):

        day, month, year = picked

        for key, value in (('day', day), ('month', month), ('year', year)):
            entries[key].delete(0, 'end')
            entries[key].insert(0, str(value))

        self._select(calendar, picked)
        self._calculate()


    def _select(self, calendar, picked):

        previous = self.selected_dates.get(calendar)

        if previous is not None:
            calendar.mark(previous)

        calendar.mark(calendar.today, '#3C3C3C')
        calendar.select(picked)

        self.selected_dates[calendar] = picked


    def _calculate(self, event=None):

        from_date = self._read_date(self.from_entries)
        to_date = self._read_date(self.to_entries)

        if from_date is None or to_date is None:
            self.from_date_label.configure(text='')
            self.to_date_label.configure(text='')
            self.track_label.configure(text='')
            self.result_label.configure(text='Invalid date')
            self.breakdown_label.configure(text='')
            return

        start_date, end_date = (from_date, to_date) if from_date <= to_date else (to_date, from_date)

        self.from_date_label.configure(
            text=f'{start_date.strftime('%a')} {start_date.day} {start_date.strftime('%b %Y')}'
        )
        self.to_date_label.configure(
            text=f'{end_date.strftime('%a')} {end_date.day} {end_date.strftime('%b %Y')}'
        )
        self.track_label.configure(text='●' + '━' * 22 + '●')

        result = self.logic.calculate_difference(from_date, to_date)

        self.result_label.configure(
            text=f'{result['years']} Years, {result['months']} Months, {result['days']} Days'
        )

        self.breakdown_label.configure(
            text=f'{result['total_days']:,} days  ·  ~{result['total_months']:.2f} months  ·  ~{result['total_years']:.2f} years'
        )


    def _jump_years(self, calendar, step):
        calendar.year = max(1, min(9999, calendar.year + step))
        calendar.year_label.set(calendar.year)
        calendar.create_calendar_frame()


    def _sync_calendar(self, entries, calendar):

        if len(entries['year'].get()) != 4:
            return

        current = self._read_date(entries)

        if current is not None:
            self._select(calendar, (current.day, current.month, current.year))


    def _handle_key_release(self, event=None):
        self._calculate()
        self._sync_calendar(self.from_entries, self.from_calendar)
        self._sync_calendar(self.to_entries, self.to_calendar)