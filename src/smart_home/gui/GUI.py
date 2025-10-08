from smart_home.Devices.Light import Light
from smart_home.Devices.Thermostat import Thermostat
import tkinter as tk
from tkinter import messagebox
import logging

logger = logging.getLogger(__name__)

class RegistrationGUI:
    def __init__(self, root, devices):
        logger.debug(f'init is called...')
        self.root = root
        self.devices = devices

        # 1: Light / 2: Thermostat
        self.device = 1

        # Frames
        self.selection_fr = tk.Frame(self.root)
        self.selection_fr.grid(row=1, column=1, pady=20)
        self.buttons_fr = tk.Frame(self.root)
        self.buttons_fr.grid(row=2, column=1)
        self.light_fr = tk.Frame(self.root)
        self.thermostat_fr = tk.Frame(self.root)

        # Selection frame
        self.select_lbl = tk.Label(self.selection_fr, text='Please choose a device to register', font=('Segoe Print', 12))
        self.selection_variable = tk.StringVar(value='light')
        self.light_rad = tk.Radiobutton(self.selection_fr, text='Light', font=('Segoe Print', 10),
                                   variable=self.selection_variable, value='light')
        self.thermostat_rad = tk.Radiobutton(self.selection_fr, text='Thermostat', font=('Segoe Print', 10),
                                        variable=self.selection_variable, value='thermo')
        self.select_lbl.grid(row=0, column=0)
        self.light_rad.grid(row=1, column=0)
        self.thermostat_rad.grid(row=2, column=0)

        # Buttons frame
        self.next = tk.Button(self.buttons_fr, text='Next', command=self.next, font=('MV Boli', 9),)
        self.register = tk.Button(self.buttons_fr, text='Register Device', command=self.register, font=('MV Boli', 9),)
        self.back = tk.Button(self.buttons_fr, text='Back', state=tk.DISABLED, command=self.back, font=('MV Boli', 9),)
        self.next.grid()
        self.back.grid()

        # Light frame
        self.light_lbl = tk.Label(self.light_fr, text='Light setting', font=('Gabriola', 16))
        self.lname_lbl = tk.Label(self.light_fr, text='Name', font=('Gabriola', 12))
        self.lname = tk.Entry(self.light_fr)
        self.lbattery_lbl = tk.Label(self.light_fr, text='Battery', font=('Gabriola', 12))
        self.lbattery = tk.Entry(self.light_fr)
        self.lloc_lbl = tk.Label(self.light_fr, text='Location', font=('Gabriola', 12))
        self.lloc = tk.Entry(self.light_fr)
        self.lcolor_lbl = tk.Label(self.light_fr, text='Color', font=('Gabriola', 12))
        self.lcolor = tk.Entry(self.light_fr)
        self.lbrightness_lbl = tk.Label(self.light_fr, text='Brightness', font=('Gabriola', 12))
        self.lbrightness = tk.Entry(self.light_fr)
        self.light_lbl.grid(row=0, column=0, columnspan=2)
        self.lname_lbl.grid(row=1, column=0, pady=1)
        self.lname.grid(row=1, column=1)
        self.lbattery_lbl.grid(row=2, column=0, pady=1)
        self.lbattery.grid(row=2, column=1)
        self.lloc_lbl.grid(row=3, column=0, pady=1)
        self.lloc.grid(row=3, column=1)
        self.lcolor_lbl.grid(row=4, column=0, pady=1)
        self.lcolor.grid(row=4, column=1)
        self.lbrightness_lbl.grid(row=5, column=0, pady=1)
        self.lbrightness.grid(row=5, column=1)

        # Thermostat frame
        self.thermo_lbl = tk.Label(self.thermostat_fr, text='Thermostat setting', font=('Gabriola', 16))
        self.tname_lbl = tk.Label(self.thermostat_fr, text='Name', font=('Gabriola', 12))
        self.tname = tk.Entry(self.thermostat_fr)
        self.tbattery_lbl = tk.Label(self.thermostat_fr, text='Battery', font=('Gabriola', 12))
        self.tbattery = tk.Entry(self.thermostat_fr)
        self.tloc_lbl = tk.Label(self.thermostat_fr, text='Location', font=('Gabriola', 12))
        self.tloc = tk.Entry(self.thermostat_fr)
        self.thermo_lbl.grid(row=0, column=0, columnspan=2)
        self.tname_lbl.grid(row=1, column=0, pady=1)
        self.tname.grid(row=1, column=1)
        self.tbattery_lbl.grid(row=2, column=0, pady=1)
        self.tbattery.grid(row=2, column=1)
        self.tloc_lbl.grid(row=3, column=0, pady=1)
        self.tloc.grid(row=3, column=1)

        # this attr is to link the 2 GUIs together
        self.status_ref = None

    def status_reference(self, status_gui):
        self.status_ref = status_gui

    def register(self):
        if self.device == 2:
            self.register_thermostat()
        else:
            self.register_light()

    def register_thermostat(self):
        try:
            the_name = self.tname.get()
            the_battery = self.tbattery.get()
            the_loc = self.tloc.get()
            newThermostat = Thermostat(
                name=the_name,
                battery=int(the_battery),
                location=the_loc
            )
            self.thermo_lbl.config(text=f'Thermostat {the_name} with ID {newThermostat.dev_id} created!')
            # storing 'the object' inside devices dict
            self.devices[the_name] = newThermostat
            self.tname.delete(0, tk.END)
            self.tbattery.delete(0, tk.END)
            self.tloc.delete(0, tk.END)
            # Refresh the status GUI
            if self.status_ref:
                self.status_ref.button_creator()
        except ValueError as e:
            messagebox.showerror(f'ValueError', f'Invalid input for battery: {e}')
            logger.error(f'Invalid input entered: {e}')
        except Exception as e:
            messagebox.showerror(f'Exception', f'Unexpected error happened: {e}')
            logger.error(f'Error: {e}')

    def register_light(self):
        try:
            the_name = self.lname.get()
            the_battery = self.lbattery.get()
            the_loc = self.lloc.get()
            the_color = self.lcolor.get()
            the_brightness = self.lbrightness.get()
            newLight = Light(
                name=the_name,
                battery=int(the_battery),
                location=the_loc,
                color=the_color,
                brightness=int(the_brightness)
            )
            self.light_lbl.config(text=f'Light {the_name} with ID {newLight.dev_id} created!')
            # storing 'the object' inside devices dict
            self.devices[the_name] = newLight
            self.lname.delete(0, tk.END)
            self.lbattery.delete(0, tk.END)
            self.lloc.delete(0, tk.END)
            self.lcolor.delete(0, tk.END)
            self.lbrightness.delete(0, tk.END)
            # Refresh status GUI
            if self.status_ref:
                self.status_ref.button_creator()
        except ValueError as e:
            messagebox.showerror(f'ValueError', f'Invalid input for battery or brightness: {e}')
            logger.error(f'Invalid input entered: {e}')
        except Exception as e:
            messagebox.showerror(f'Exception', f'Unexpected error happened: {e}')
            logger.error(f'Error: {e}')

    def next(self):
        self.buttons_fr.grid_forget()
        self.next.grid_forget()
        self.register.grid()
        self.back.config(state=tk.ACTIVE)
        if self.selection_variable.get() == 'thermo':
            self.device = 2
            self.thermostat()
        else:
            self.device = 1
            self.light()

    def thermostat(self):
        self.selection_fr.grid_forget()
        self.thermostat_fr.grid(pady=20)
        self.buttons_fr.grid(pady=10)

    def light(self):
        self.selection_fr.grid_forget()
        self.light_fr.grid(pady=20)
        self.buttons_fr.grid(pady=10)

    def back(self):
        self.buttons_fr.grid_forget()
        self.thermostat_fr.grid_forget()
        self.light_fr.grid_forget()
        self.register.grid_forget()
        self.selection_fr.grid(row=1, column=1, pady=20)
        self.back.config(state=tk.DISABLED)
        self.next.grid()
        self.buttons_fr.grid(row=2, column=1)


class StatusGUI:
    def __init__(self, root, devices):

        self.root = root
        self.devices = devices

        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=0)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

        # Frames
        self.lightframe = tk.Frame(self.root)
        self.lightframe.grid(row=0, column=1, sticky="ns")
        self.thermoframe = tk.Frame(self.root)
        self.thermoframe.grid(row=1, column=1, sticky="ns")
        self.info_frame = tk.Frame(self.root)
        self.info_frame.grid(row=2, column=1, sticky="ns")

        # Light Frame
        self.lights_lbl = tk.Label(self.lightframe, text='Lights', font=("Segoe Print", 14))
        self.lights_lbl.grid(row=0, column=0, pady=20)

        # Thermo Frame
        self.thermo_lbl = tk.Label(self.thermoframe, text='Thermostats', font=("Segoe Print", 14))
        self.thermo_lbl.grid(row=0, column=0)

        self.canvas = tk.Canvas(self.info_frame, width=100, height=30)
        self.canvas.grid(row=2, column=2, sticky='nsew')

    def button_clearer(self):
        for widget in self.lightframe.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()
        for widget in self.thermoframe.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()

    def button_creator(self):
        # first delete the existing buttons then recreate them using updated devicelist
        self.button_clearer()
        for device in self.devices:
            if isinstance(self.devices[device], Light):
                                                                    # putting the object of the device inside a var called obj, then calling showinfo() specifically for that object
                light = tk.Button(self.lightframe, text=device, command= lambda obj = self.devices[device]: self.showinfo(obj))
                light.grid(pady=5)
            elif isinstance(self.devices[device], Thermostat):
                thermo = tk.Button(self.thermoframe, text=device, command= lambda obj = self.devices[device]: self.showinfo(obj))
                thermo.grid(pady=5)

    def showinfo(self, device):
        self.widget_remover()
        all_info = device.get_info()
        if isinstance(device, Light):
            self.light_analyzeinfo(all_info)
        elif isinstance(device, Thermostat):
            self.thermo_analyzeinfo(all_info)

    def widget_remover(self):
        for widget in self.info_frame.winfo_children():
            widget.destroy()
        # the canvas is deleted because of line above
        self.canvas = tk.Canvas(self.info_frame, width=100, height=30)
        self.canvas.grid(row=2, column=2, columnspan=2, sticky='nsew')

    def thermo_analyzeinfo(self, the_info):
        strings = {}
        for segment in the_info.split('|'):
            segment = segment.strip()
            if ':' in segment:
                key, value = segment.split(':')
                key = key.strip()
                value = value.strip()
                if key in ['Type', 'Name', 'ID', 'IP', 'Location']:
                    strings[key] = value
                elif key == 'Battery':
                    bg_rec, rec = self.thermo_draw_bar()
                    percentage = int(value)
                    self.update_bar(bg_rec, rec, percentage)
                elif key == 'Mode':
                    mode_frame = tk.Frame(self.info_frame)
                    mode_lbl = tk.Label(mode_frame, text='MODE', font=('Gabriola', 12, 'bold'))
                    cool_box = tk.Button(mode_frame, text='COOL', state='disabled', font=('Ariel', 8, 'bold'))
                    heat_box = tk.Button(mode_frame, text='HEAT', state='disabled', font=('Ariel', 8, 'bold'))
                    off_box = tk.Button(mode_frame, text='OFF', state='disabled', font=('Ariel', 8, 'bold'))
                    if value == 'COOL':
                        cool_box.config(relief='sunken')
                    elif value == 'HEAT':
                        heat_box.config(relief='sunken')
                    else:
                        off_box.config(relief='sunken')
                    mode_lbl.grid(row=0, column=0)
                    cool_box.grid(row=0, column=1, padx=10)
                    heat_box.grid(row=0, column=2)
                    off_box.grid(row=0, column=3, padx=10)

                    mode_frame.grid(row=3, column=2, columnspan=2)
                    
            elif '?' in segment:
                key, value = segment.split('?')
                key = key.strip()
                value = value.strip()
                checkmark = "✔"
                cross = "❌"
                if key == 'On':
                    on_off_frame = tk.Frame(self.info_frame)
                    on_box = tk.Button(on_off_frame, text='ON', state='disabled', font=('Ariel', 8, 'bold'))
                    off_box = tk.Button(on_off_frame, text='OFF', state='disabled', font=('Ariel', 8, 'bold'))
                    if value.title() == 'True':
                        on_box.config(relief='sunken')
                    else:
                        off_box.config(relief='sunken')
                    on_box.grid(row=0, column=0, padx=10)
                    off_box.grid(row=0, column=1)

                    on_off_frame.grid(row=1, column=0, columnspan=2)

                elif key == 'Connected':
                    connect_frame = tk.Frame(self.info_frame)
                    connect_lbl = tk.Label(connect_frame, text='Connection', font=('Gabriola', 12, 'bold'))
                    true_box = tk.Button(connect_frame, text=checkmark, state='disabled')
                    false_box = tk.Button(connect_frame, text=cross, state='disabled')
                    connect_lbl.grid(row=0, column=0)
                    true_box.grid(row=0, column=1, padx=10)
                    false_box.grid(row=0, column=2)

                    connect_frame.grid(row=1, column=2, columnspan=2)

                    if value.title() == 'True':
                        true_box.config(relief='sunken')
                    else:
                        false_box.config(relief='sunken')

                elif key == 'Charging':
                    charging_frame = tk.Frame(self.info_frame)
                    charging_lbl = tk.Label(charging_frame, text='Charging', font=('Gabriola', 12, 'bold'))
                    true_box = tk.Button(charging_frame, text=checkmark, state='disabled')
                    false_box = tk.Button(charging_frame, text=cross, state='disabled')
                    charging_lbl.grid(row=0, column=0)
                    true_box.grid(row=0, column=1, padx=10)
                    false_box.grid(row=0, column=2)

                    charging_frame.grid(row=1, column=4, columnspan=2)

                    if value.title() == 'True':
                        true_box.config(relief='sunken')
                    else:
                        false_box.config(relief='sunken')
                elif key == 'in process':
                    process_frame = tk.Frame(self.info_frame)
                    process_lbl = tk.Label(process_frame, text='In Process', font=('Gabriola', 12, 'bold'))
                    true_box = tk.Button(process_frame, text=checkmark, state='disabled')
                    false_box = tk.Button(process_frame, text=cross, state='disabled')
                    process_lbl.grid(row=0, column=0)
                    true_box.grid(row=0, column=1, padx=10)
                    false_box.grid(row=0, column=2)

                    process_frame.grid(row=3, column=0, columnspan=2)

                    if value.title() == 'True':
                        true_box.config(relief='sunken')
                    else:
                        false_box.config(relief='sunken')


        string_phrase = ''
        for k, v in strings.items():
            if string_phrase:
                string_phrase += f'   |   {k}: {v}'
            else:
                string_phrase += f'{k}: {v}'
        string_lbl = tk.Label(self.info_frame, text=f'{string_phrase}', font=('Gabriola', 15))
        string_lbl.grid(row=0, column=2, columnspan=2, sticky='nsew')
        return

    def light_analyzeinfo(self, the_info):
        strings = {}
        for segment in the_info.split('|'):
            segment = segment.strip()
            if ':' in segment:
                key, value = segment.split(':')
                key = key.strip()
                value = value.strip()
                if key in ['Type', 'Name', 'ID', 'IP', 'Location']:
                    strings[key] = value
                elif key in ['Brightness', 'Battery']:
                    bg_rec, rec = self.light_draw_bar(key)
                    percentage = int(value)
                    self.update_bar(bg_rec, rec, percentage)
                elif key == 'Color':
                    colorbox = tk.Button(self.info_frame, text='COLOR', state='disabled', bg=value, width=10)
                    colorbox.grid(row=3, column=2, columnspan=2)
            elif '?' in segment:
                key, value = segment.split('?')
                key = key.strip()
                value = value.strip()
                checkmark = "✔"
                cross = "❌"
                if key == 'On':
                    on_off_frame = tk.Frame(self.info_frame)
                    on_box = tk.Button(on_off_frame, text='ON', state='disabled', font=('Ariel', 8, 'bold'))
                    off_box = tk.Button(on_off_frame, text='OFF', state='disabled', font=('Ariel', 8, 'bold'))
                    if value.title() == 'True':
                        on_box.config(relief='sunken')
                    else:
                        off_box.config(relief='sunken')
                    on_box.grid(row=0, column=0, padx=10)
                    off_box.grid(row=0, column=1)

                    on_off_frame.grid(row=1, column=0, columnspan=2)

                elif key == 'Connected':
                    connect_frame = tk.Frame(self.info_frame)
                    connect_lbl = tk.Label(connect_frame, text='Connection', font=('Gabriola', 12, 'bold'))
                    true_box = tk.Button(connect_frame, text=checkmark, state='disabled')
                    false_box = tk.Button(connect_frame, text=cross, state='disabled')
                    connect_lbl.grid(row=0, column=0)
                    true_box.grid(row=0, column=1, padx=10)
                    false_box.grid(row=0, column=2)

                    connect_frame.grid(row=1, column=2, columnspan=2)

                    if value.title() == 'True':
                        true_box.config(relief='sunken')
                    else:
                        false_box.config(relief='sunken')

                elif key == 'Charging':
                    charging_frame = tk.Frame(self.info_frame)
                    charging_lbl = tk.Label(charging_frame, text='Charging', font=('Gabriola', 12, 'bold'))
                    true_box = tk.Button(charging_frame, text=checkmark, state='disabled')
                    false_box = tk.Button(charging_frame, text=cross, state='disabled')
                    charging_lbl.grid(row=0, column=0)
                    true_box.grid(row=0, column=1, padx=10)
                    false_box.grid(row=0, column=2)

                    charging_frame.grid(row=1, column=4, columnspan=2)

                    if value.title() == 'True':
                        true_box.config(relief='sunken')
                    else:
                        false_box.config(relief='sunken')

        string_phrase = ''
        for k, v in strings.items():
            if string_phrase:
                string_phrase += f'   |   {k}: {v}'
            else:
                string_phrase += f'{k}: {v}'
        string_lbl = tk.Label(self.info_frame, text=f'{string_phrase}', font=('Gabriola', 15))
        string_lbl.grid(row=0, column=2, columnspan=2, sticky='nsew')
        return

    def light_draw_bar(self, rec_type):
        if rec_type == 'Battery':
            bg_rec = self.canvas.create_rectangle(70, 5, 130, 25, fill='azure1', outline='black')
            rec = self.canvas.create_rectangle(70, 5, 71, 25, fill='aquamarine2')
        elif rec_type == 'Brightness':
            bg_rec = self.canvas.create_rectangle(160, 5, 240, 25, fill='black')
            rec = self.canvas.create_rectangle(160, 5, 111, 25, fill='white')
        return bg_rec, rec

    def thermo_draw_bar(self):
        bg_rec = self.canvas.create_rectangle(200, 5, 280, 25, fill='azure1', outline='black')
        rec = self.canvas.create_rectangle(200, 5, 201, 25, fill='aquamarine2')
        return bg_rec, rec

    def update_bar(self, bg_rectangle, rectangle, percentage):
        coordinates = self.canvas.coords(bg_rectangle)
        x_max = coordinates[2] - coordinates[0]
        new_x = (percentage / 100) * x_max
        self.canvas.coords(rectangle, coordinates[0], coordinates[1], new_x + coordinates[0], coordinates[3])


#class ControlGUI: