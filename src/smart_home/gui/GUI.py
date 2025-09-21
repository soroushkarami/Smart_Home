from smart_home.Devices.Base import Base
from smart_home.Devices.Light import Light
import tkinter as tk
import logging

logger = logging.getLogger(__name__)

class RegistrationGUI:
    def __init__(self, root):
        self.root = root

        # Frames
        self.selection_fr = tk.Frame(root)
        self.selection_fr.grid()

        # Selection frame
        self.select_lbl = tk.Label(self.selection_fr, text='Please choose a device to register')
        self.selection_variable = tk.StringVar(value='light')
        self.light_rad = tk.Radiobutton(self.selection_fr, text='Light',
                                   variable=self.selection_variable, value='light')
        self.select_lbl.grid()
        self.light_rad.grid()


