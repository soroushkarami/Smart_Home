from smart_home.Devices.Light import Light
from smart_home.Devices.Thermostat import Thermostat
import tkinter as tk
from tkinter import messagebox
import logging
import asyncio

logger = logging.getLogger('GUI')

class RegistrationGUI:
    def __init__(self, root, devices):
        logger.info(f'RegistrationGUI init is called...')
        self.root = root
        self.devices = devices

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
        logger.debug(f'RegGUI: Selection frame formed!')

        # Buttons frame
        self.next = tk.Button(self.buttons_fr, text='Next', command=self.next, font=('MV Boli', 9),)
        self.register = tk.Button(self.buttons_fr, text='Register Device', command=self.register, font=('MV Boli', 9),)
        self.back = tk.Button(self.buttons_fr, text='Back', state=tk.DISABLED, command=self.back, font=('MV Boli', 9),)
        self.next.grid()
        self.back.grid()
        logger.debug(f'RegGUI: Buttons frame formed!')

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
        logger.debug(f'RegGUI: Light frame formed!')

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
        logger.debug(f'RegGUI: Thermostat frame formed!')

        # this attr is to link the 2 GUIs together
        self.status_ref = None

    def status_reference(self, status_gui):
        self.status_ref = status_gui

    def register(self):
        logger.debug(f'RegGUI: register button is pressed...')
        if self.selection_variable.get() == 'thermo':
            logger.info(f'RegGUI: The device is a thermostat!')
            self.register_thermostat()
        else:
            logger.info(f'RegGUI: The device is a light!')
            self.register_light()

    def register_thermostat(self):
        logger.info(f'RegGUI: register_thermostat method is called...')
        try:
            logger.info(f"RegGUI: Trying to assign user input to device's parameters...")
            the_name = self.tname.get()
            the_battery = self.tbattery.get()
            the_loc = self.tloc.get()
            newThermostat = Thermostat(
                name=the_name,
                battery=int(the_battery),
                location=the_loc
            )
            logger.info(f'RegGUI: Assignment finished successfully!')
            self.thermo_lbl.config(text=f'Thermostat {the_name} with ID {newThermostat.dev_id} created!')
            # storing 'the object' inside devices dict
            self.devices[the_name] = newThermostat
            logger.info(f'RegGUI: {the_name} added into registered devices dictionary!')
            logger.debug(f'RegGUI: clearing entries...')
            self.tname.delete(0, tk.END)
            self.tbattery.delete(0, tk.END)
            self.tloc.delete(0, tk.END)
            # Refresh the status GUI
            if self.status_ref:
                logger.warning(f'RegGUI: status_ref exists, applying changes into StatusGUI...')
                self.status_ref.button_creator()
        except ValueError as e:
            messagebox.showerror(f'ValueError', f'Invalid input for battery: {e}')
            logger.error(f'RegGUI: Assignment failed! Invalid input entered: {e}')
        except Exception as e:
            messagebox.showerror(f'Exception', f'Unexpected error happened: {e}')
            logger.error(f'RegGUI: Assignment failed: {e}')

    def register_light(self):
        logger.info(f'RegGUI: register_light method is called...')
        try:
            logger.info(f"RegGUI: Trying to assign user input to device's parameters...")
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
            logger.info(f'RegGUI: Assignment finished successfully!')
            self.light_lbl.config(text=f'Light {the_name} with ID {newLight.dev_id} created!')
            # storing 'the object' inside devices dict
            self.devices[the_name] = newLight
            logger.info(f'RegGUI: {the_name} added into registered devices dictionary!')
            logger.debug(f'RegGUI: clearing entries...')
            self.lname.delete(0, tk.END)
            self.lbattery.delete(0, tk.END)
            self.lloc.delete(0, tk.END)
            self.lcolor.delete(0, tk.END)
            self.lbrightness.delete(0, tk.END)
            # Refresh status GUI
            if self.status_ref:
                logger.warning(f'RegGUI: status_ref exists, applying changes into StatusGUI...')
                self.status_ref.button_creator()
        except ValueError as e:
            messagebox.showerror(f'ValueError', f'Invalid input for battery or brightness: {e}')
            logger.error(f'RegGUI: Assignment failed! Invalid input entered: {e}')
        except Exception as e:
            messagebox.showerror(f'Exception', f'Unexpected error happened: {e}')
            logger.error(f'RegGUI: Assignment failed: {e}')

    def next(self):
        logger.debug(f'RegGUI: next button is pressed...')
        self.buttons_fr.grid_forget()
        self.next.grid_forget()
        self.register.grid()
        self.back.config(state=tk.ACTIVE)
        if self.selection_variable.get() == 'thermo':
            self.thermostat_grid()
        else:
            self.light_grid()

    def thermostat_grid(self):
        logger.debug(f'RegGUI: thermostat_grid method is called...')
        self.selection_fr.grid_forget()
        self.thermostat_fr.grid(pady=20)
        self.buttons_fr.grid(pady=10)

    def light_grid(self):
        logger.debug(f'RegGUI: light_grid method is called...')
        self.selection_fr.grid_forget()
        self.light_fr.grid(pady=20)
        self.buttons_fr.grid(pady=10)

    def back(self):
        logger.debug(f'RegGUI: back button is pressed...')
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
        logger.info(f'StatusGUI init is called...')
        self.root = root
        self.devices = devices

        # to hold the async loop and pass it to ControlGUI when needed
        self.loop = None

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
            # used by ControlGUI:
        self.control_frame = tk.Frame(self.root)
        self.control_frame.grid(row=3, column=1, sticky="ns")

        # Light Frame
        self.lights_lbl = tk.Label(self.lightframe, text='Lights', font=("Segoe Print", 14))
        self.lights_lbl.grid(row=0, column=0, pady=20)
        logger.debug(f'StsGUI: Light frame formed!')

        # Thermo Frame
        self.thermo_lbl = tk.Label(self.thermoframe, text='Thermostats', font=("Segoe Print", 14))
        self.thermo_lbl.grid(row=0, column=0)
        logger.debug(f'StsGUI: Thermo frame formed!')

        self.canvas = tk.Canvas(self.info_frame, width=100, height=30)
        self.canvas.grid(row=2, column=2, sticky='nsew')
        logger.debug(f'StsGUI: Canvas for visual representation created!')

        # polling parameter
        self.pole_id = None

    def button_clearer(self):
        logger.debug(f'StsGUI: button_clearer method is called...')
        for widget in self.lightframe.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()
        logger.debug(f'StsGUI: All light devices are deleted')
        for widget in self.thermoframe.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()
        logger.debug(f'StsGUI: All thermostat devices are deleted')

    def button_creator(self):
        logger.info(f'StsGUI: button_creator method is called, calling button_clearer...')
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
            logger.info(f'StsGUI: Button for {device} created!')

    def showinfo(self, device):
        logger.debug(f'StsGUI: showinfo method is called for {device}...')
        self.widget_remover()
        all_info = device.get_info()
        logger.info(f"StsGUI: {device}'s info extracted using its get_info, passing it to analyze_info...")
        self.analyze_info(device, all_info)

    def widget_remover(self):
        logger.debug(f'StsGUI: widget_remover method is called...')
        for widget in self.info_frame.winfo_children():
            widget.destroy()
        logger.debug(f'StsGUI: All previous info cleared!')
        # the canvas is deleted because of line above
        self.canvas = tk.Canvas(self.info_frame, width=100, height=30)
        self.canvas.grid(row=2, column=2, columnspan=2, sticky='nsew')

    def analyze_info(self, the_device, the_info):
        logger.info(f'StsGUI: analyze_info method is called...')
        strings = {}
        for segment in the_info.split('|'):
            logger.debug(f"StsGUI: info is split by '|'")
            segment = segment.strip()
            if ':' in segment:
                key, value = segment.split(':')
                logger.debug(f"StsGUI: info is split by ':'")
                key = key.strip()
                value = value.strip()
                if key in ['Type', 'Name', 'ID', 'IP', 'Location']:
                    strings[key] = value
                    logger.debug(f'StsGUI: Key {key} extracted for {the_device.name}!')
                if isinstance(the_device, Light):
                    if key in ['Brightness', 'Battery']:
                        logger.debug(f'StsGUI: Key {key} extracted for {the_device.name}!')
                        bg_rec, rec = self.light_draw_bar(key)
                        percentage = int(value)
                        self.update_bar(bg_rec, rec, percentage)
                    elif key == 'Color':
                        logger.debug(f'StsGUI: Key {key} extracted for {the_device.name}!')
                        colorbox = tk.Button(self.info_frame, text='COLOR', state='disabled', bg=value, width=10)
                        colorbox.grid(row=3, column=2, columnspan=2)
                        logger.debug(f'StsGUI: Color representation created for this light: {value}')
                elif isinstance(the_device, Thermostat):
                    if key == 'Battery':
                        logger.debug(f'StsGUI: Key {key} extracted for {the_device.name}!')
                        bg_rec, rec = self.thermo_draw_bar()
                        percentage = int(value)
                        self.update_bar(bg_rec, rec, percentage)
                    elif key == 'Mode':
                        logger.debug(f'StsGUI: Key {key} extracted for {the_device.name}!')
                        mode_frame = tk.Frame(self.info_frame)
                        mode_lbl = tk.Label(mode_frame, text='MODE', font=('Gabriola', 12, 'bold'))
                        cool_box = tk.Button(mode_frame, text='COOL', state='disabled', relief='groove', font=('Ariel', 8, 'bold'))
                        heat_box = tk.Button(mode_frame, text='HEAT', state='disabled', relief='groove', font=('Ariel', 8, 'bold'))
                        off_box = tk.Button(mode_frame, text='OFF', state='disabled', relief='groove', font=('Ariel', 8, 'bold'))
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
                        logger.debug(f'StsGUI: Mode {value} set for {Thermostat.name}!')
                    elif key == 'Current Temperature':
                        logger.debug(f'StsGUI: Key {key} extracted for {the_device.name}!')
                        current_temp_var = tk.StringVar(value=value)
                        # Create a Label that uses the StringVar
                        logger.debug(f'StsGUI: Creating a dynamic Label for showing current temprerature...')
                        temp_lbl = tk.Label(self.info_frame, textvariable=current_temp_var, font=('Gabriola', 14, 'bold'))
                        temp_lbl.grid(row=3, column=4, columnspan=2)
                        # Start the periodic update mechanism(polling)
                        self.start_polling(the_device, current_temp_var)
            elif '?' in segment:
                key, value = segment.split('?')
                logger.debug(f"StsGUI: info is split by '?'")
                key = key.strip()
                value = value.strip()
                checkmark = "✔"
                cross = "❌"
                if key == 'On':
                    logger.debug(f'StsGUI: Key {key} extracted for {the_device.name}!')
                    on_off_frame = tk.Frame(self.info_frame)
                    on_box = tk.Button(on_off_frame, text='ON', state='disabled', relief='groove', font=('Ariel', 8, 'bold'))
                    off_box = tk.Button(on_off_frame, text='OFF', state='disabled', relief='groove', font=('Ariel', 8, 'bold'))
                    if value.title() == 'True':
                        on_box.config(relief='sunken')
                    else:
                        off_box.config(relief='sunken')
                    logger.debug(f'StsGUI: {the_device.name} state is {value}!')
                    on_box.grid(row=0, column=0, padx=10)
                    off_box.grid(row=0, column=1)
                    on_off_frame.grid(row=1, column=0, columnspan=2)
                elif key == 'Connected':
                    logger.debug(f'StsGUI: Key {key} extracted for {the_device.name}!')
                    connect_frame = tk.Frame(self.info_frame)
                    connect_lbl = tk.Label(connect_frame, text='Connection', font=('Gabriola', 12, 'bold'))
                    true_box = tk.Button(connect_frame, text=checkmark, state='disabled', relief='groove')
                    false_box = tk.Button(connect_frame, text=cross, state='disabled', relief='groove')
                    connect_lbl.grid(row=0, column=0)
                    true_box.grid(row=0, column=1, padx=10)
                    false_box.grid(row=0, column=2)
                    connect_frame.grid(row=1, column=2, columnspan=2)
                    if value.title() == 'True':
                        true_box.config(relief='sunken')
                    else:
                        false_box.config(relief='sunken')
                    logger.debug(f'StsGUI: {the_device.name} connection set as {value}!')
                elif key == 'Charging':
                    logger.debug(f'StsGUI: Key {key} extracted for {the_device.name}!')
                    charging_frame = tk.Frame(self.info_frame)
                    charging_lbl = tk.Label(charging_frame, text='Charging', font=('Gabriola', 12, 'bold'))
                    true_box = tk.Button(charging_frame, text=checkmark, state='disabled', relief='groove')
                    false_box = tk.Button(charging_frame, text=cross, state='disabled', relief='groove')
                    charging_lbl.grid(row=0, column=0)
                    true_box.grid(row=0, column=1, padx=10)
                    false_box.grid(row=0, column=2)
                    charging_frame.grid(row=1, column=4, columnspan=2)
                    if value.title() == 'True':
                        true_box.config(relief='sunken')
                    else:
                        false_box.config(relief='sunken')
                    logger.debug(f'StsGUI: {the_device.name} charging state set as {value}!')
                if isinstance(the_device, Thermostat):
                    if key == 'in process':
                        logger.debug(f'StsGUI: Key {key} extracted for {the_device.name}!')
                        process_frame = tk.Frame(self.info_frame)
                        process_lbl = tk.Label(process_frame, text='In Process', font=('Gabriola', 12, 'bold'))
                        true_box = tk.Button(process_frame, text=checkmark, state='disabled', relief='groove')
                        false_box = tk.Button(process_frame, text=cross, state='disabled', relief='groove')
                        process_lbl.grid(row=0, column=0)
                        true_box.grid(row=0, column=1, padx=10)
                        false_box.grid(row=0, column=2)
                        process_frame.grid(row=3, column=0, columnspan=2)
                        if value.title() == 'True':
                            true_box.config(relief='sunken')
                        else:
                            false_box.config(relief='sunken')
                        logger.debug(f'StsGUI: {the_device.name} process state set as {value}!')
        string_phrase = ''
        for k, v in strings.items():
            if string_phrase:
                string_phrase += f'   |   {k}: {v}'
            else:
                string_phrase += f'{k}: {v}'
        string_lbl = tk.Label(self.info_frame, text=f'{string_phrase}', font=('Gabriola', 15))
        string_lbl.grid(row=0, column=2, columnspan=2, sticky='nsew')

        # create this device's ControlGUI:
        controller = ControlGUI(self.control_frame, the_device)
        controller.widget_creator()
        controller.start_executing(self.loop)

        return

    def start_polling(self, the_device, current_temp_var):
        logger.debug(f'StsGUI: start_polling method is called...')
        # first cancel any other polling if it exists:
        if self.pole_id:
            self.root.after_cancel(self.pole_id)
            self.pole_id = None
            logger.warning(f'StsGUI: Any previous polling canceled!')
        # then start polling:
        self.polling_process(the_device, current_temp_var)

    def polling_process(self, the_device, current_temp_var):
        logger.debug(f'StsGUI: polling_process method is called...')
        info = the_device.get_info()
        logger.info(f'StsGUI: info extracted, extracting Current Temperature...')
        for segment in info.split('|'):
            segment = segment.strip()
            if ':' in segment:
                key, value = segment.split(':')
                key = key.strip()
                value = value.strip()
                if key == 'Current Temperature':
                    current_temp_var.set(value)     # in tkinter we use set() for assigning dynamic values not '='
        if the_device.in_process and the_device.is_on:
            # check the temp each 1000ms (1s)
            logger.info(f'StsGUI: Checking current temperature...')
            self.pole_id = self.root.after(1000, self.polling_process, the_device, current_temp_var)
        else:   # ie the process is finished
            logger.warning(f'StsGUI: Target temperature is reached, canceling polling...')
            if self.pole_id:
                self.root.after_cancel(self.pole_id)
                self.pole_id = None

    def light_draw_bar(self, rec_type):
        logger.debug(f'StsGUI: light_draw_bar method is called...')
        if rec_type == 'Battery':
            bg_rec = self.canvas.create_rectangle(70, 5, 130, 25, fill='azure1', outline='black')
            rec = self.canvas.create_rectangle(70, 5, 71, 25, fill='aquamarine2')
            logger.debug(f'StsGUI: Raw battery representation created for this light!')
        elif rec_type == 'Brightness':
            bg_rec = self.canvas.create_rectangle(160, 5, 240, 25, fill='black')
            rec = self.canvas.create_rectangle(160, 5, 111, 25, fill='white')
            logger.debug(f'StsGUI: Raw brightness representation created for this light!')
        return bg_rec, rec

    def thermo_draw_bar(self):
        logger.debug(f'StsGUI: thermo_draw_bar method is called...')
        bg_rec = self.canvas.create_rectangle(200, 5, 280, 25, fill='azure1', outline='black')
        rec = self.canvas.create_rectangle(200, 5, 201, 25, fill='aquamarine2')
        logger.debug(f'StsGUI: Raw battery representation created for this thermostat!')
        return bg_rec, rec

    def update_bar(self, bg_rectangle, rectangle, percentage):
        logger.debug(f'StsGUI: update_bar method is called...')
        coordinates = self.canvas.coords(bg_rectangle)
        x_max = coordinates[2] - coordinates[0]
        new_x = (percentage / 100) * x_max
        self.canvas.coords(rectangle, coordinates[0], coordinates[1], new_x + coordinates[0], coordinates[3])
        logger.debug(f'StsGUI: Visual representation updated: {new_x}%')

    def get_async_loop(self, the_loop):
        logger.debug(f'StsGUI: get_async_loop method is called...')
        self.loop = the_loop
        logger.info(f'The async loop caught and stored in StatusGUI!')

class ControlGUI:
    def __init__(self, control_frame, the_device):
        logger.info(f'ControlGUI init is called...')
        self.frame = control_frame
        self.device = the_device
        self.async_loop = None

    def widget_creator(self):
        logger.debug(f'ctrlGUI: widget_creator method is called...')
        toggle = tk.Button(self.frame, text='Toggle State', command=self.toggle_caller)

    def start_looping(self, the_loop):
        logger.debug(f'ctrlGUI: start_looping method is called...')
        self.async_loop = the_loop
        logger.info(f'The async loop passed to ControlGUI successfully!')

    def toggle_caller(self):
        logger.debug(f'ctrlGUI: toggle_caller method is called...')
        if self.async_loop:
            logger.info(f'ctrlGUI: Sending the async toggle to the new thread...')
            asyncio.run_coroutine_threadsafe(self.device.toggle(), self.async_loop)
        else:
            logger.error(f'ctrlGUI: No active loop found!')
