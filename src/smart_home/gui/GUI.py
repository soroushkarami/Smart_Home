from smart_home.Devices.Light import Light
from smart_home.Devices.Thermostat import Thermostat
import tkinter as tk
from tkinter import messagebox
import logging

logger = logging.getLogger(__name__)

class RegistrationGUI:
    def __init__(self, root):
        self.root = root

        # 1: Light / 2: Thermostat
        self.device = 1

        # Frames
        self.selection_fr = tk.Frame(root)
        self.selection_fr.grid()
        self.buttons_fr = tk.Frame(root)
        self.buttons_fr.grid()
        self.light_fr = tk.Frame(root)
        self.thermostat_fr = tk.Frame(root)

        # Selection frame
        self.select_lbl = tk.Label(self.selection_fr, text='Please choose a device to register')
        self.selection_variable = tk.StringVar(value='light')
        self.light_rad = tk.Radiobutton(self.selection_fr, text='Light',
                                   variable=self.selection_variable, value='light')
        self.thermostat_rad = tk.Radiobutton(self.selection_fr, text='Thermostat',
                                        variable=self.selection_variable, value='thermo')
        self.select_lbl.grid()
        self.light_rad.grid()
        self.thermostat_rad.grid()

        # Buttons frame
        self.next = tk.Button(self.buttons_fr, text='Next', command=self.next)
        self.register = tk.Button(self.buttons_fr, text='Register Device', command=self.register)
        self.back = tk.Button(self.buttons_fr, text='Back', state=tk.DISABLED, command=self.back)
        self.next.grid()
        self.back.grid()

        # Light frame
        self.light_lbl = tk.Label(self.light_fr, text='Light setting', font=('Inconsolata', 15))
        self.lname_lbl = tk.Label(self.light_fr, text='Name')
        self.lname = tk.Entry(self.light_fr)
        self.lbattery_lbl = tk.Label(self.light_fr, text='Battery')
        self.lbattery = tk.Entry(self.light_fr)
        self.lloc_lbl = tk.Label(self.light_fr, text='Location')
        self.lloc = tk.Entry(self.light_fr)
        self.lcolor_lbl = tk.Label(self.light_fr, text='Color')
        self.lcolor = tk.Entry(self.light_fr)
        self.lbrightness_lbl = tk.Label(self.light_fr, text='Brightness')
        self.lbrightness = tk.Entry(self.light_fr)
        self.light_lbl.grid(row=0, column=0)
        self.lname_lbl.grid(row=1, column=0)
        self.lname.grid(row=1, column=1)
        self.lbattery_lbl.grid(row=2, column=0)
        self.lbattery.grid(row=2, column=1)
        self.lloc_lbl.grid(row=3, column=0)
        self.lloc.grid(row=3, column=1)
        self.lcolor_lbl.grid(row=4, column=0)
        self.lcolor.grid(row=4, column=1)
        self.lbrightness_lbl.grid(row=5, column=0)
        self.lbrightness.grid(row=5, column=1)

        # Thermostat frame
        self.thermo_lbl = tk.Label(self.thermostat_fr, text='Thermostat setting', font=('Inconsolata', 15))
        self.tname_lbl = tk.Label(self.thermostat_fr, text='Name')
        self.tname = tk.Entry(self.thermostat_fr)
        self.tbattery_lbl = tk.Label(self.thermostat_fr, text='Battery')
        self.tbattery = tk.Entry(self.thermostat_fr)
        self.tloc_lbl = tk.Label(self.thermostat_fr, text='Location')
        self.tloc = tk.Entry(self.thermostat_fr)
        self.thermo_lbl.grid(row=0, column=0)
        self.tname_lbl.grid(row=1, column=0)
        self.tname.grid(row=1, column=1)
        self.tbattery_lbl.grid(row=2, column=0)
        self.tbattery.grid(row=2, column=1)
        self.tloc_lbl.grid(row=3, column=0)
        self.tloc.grid(row=3, column=1)

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
            self.tname.delete(0, tk.END)
            self.tbattery.delete(0, tk.END)
            self.tloc.delete(0, tk.END)
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
            self.lname.delete(0, tk.END)
            self.lbattery.delete(0, tk.END)
            self.lloc.delete(0, tk.END)
            self.lcolor.delete(0, tk.END)
            self.lbrightness.delete(0, tk.END)
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
        self.thermostat_fr.grid()
        self.buttons_fr.grid()

    def light(self):
        self.selection_fr.grid_forget()
        self.light_fr.grid()
        self.buttons_fr.grid()

    def back(self):
        self.buttons_fr.grid_forget()
        self.thermostat_fr.grid_forget()
        self.light_fr.grid_forget()
        self.selection_fr.grid()
        self.register.grid_forget()
        self.next.grid()
        self.back.config(state=tk.DISABLED)
        self.buttons_fr.grid()