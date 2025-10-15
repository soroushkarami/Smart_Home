from smart_home.gui.GUI import RegistrationGUI, StatusGUI
import logging
import tkinter as tk
import asyncio
import threading

def start_loop(loop):
    """Run the asyncio event loop in a separate thread."""
    global event_loop
    event_loop = loop
    # Set the loop as the current loop for this new thread
    asyncio.set_event_loop(loop)
    # Start the loop running forever
    loop.run_forever()

def main():
    logging_setting()

    # Initialize and start the asyncio loop in a background thread
    the_loop = asyncio.new_event_loop()
    new_thread = threading.Thread(target=start_loop,
                                  args=(the_loop,))
    new_thread.start()

    my_root = tk.Tk()
    my_root.title(f'Registration')
    my_root.geometry(f'400x400')
    # center all frames(all frames are at column=1)
    my_root.grid_columnconfigure(0, weight=1)   # left space
    my_root.grid_columnconfigure(2, weight=1)   # right space

    # making this a window that is created and managed by main window
    my_status = tk.Toplevel(my_root)
    my_status.title(f'Status')
    my_status.geometry(f'750x500')
    my_status.grid_columnconfigure(0, weight=1)   # left space
    my_status.grid_columnconfigure(2, weight=1)   # right space

    devices = {}

    reg_gui = RegistrationGUI(my_root, devices)
    stat_gui = StatusGUI(my_status, devices)

    # make registration be aware of status
    reg_gui.status_reference(stat_gui)

    stat_gui.button_creator()

    my_root.mainloop()

def logging_setting():
    logging.debug(f'logging setting function is called...')
    # This config is just for the root .log file which is the log in main module
    logging.basicConfig(level= logging.DEBUG,
                format='%(asctime)s | %(levelname)s: %(message)s', filemode='w')

    # catching loggers from other modules
    base_log = logging.getLogger('Base')
    light_log = logging.getLogger('Light')
    thermostat_log = logging.getLogger('Thermostat')
    gui_log = logging.getLogger('GUI')

    # setting their level
    base_log.setLevel(logging.DEBUG)
    light_log.setLevel(logging.DEBUG)
    thermostat_log.setLevel(logging.DEBUG)
    gui_log.setLevel(logging.DEBUG)
    logging.info(f'Setting level for module loggers finished successfully!')

    # preventing propagating their messages to root .log
    base_log.propagate = False
    light_log.propagate = False
    thermostat_log.propagate = False
    gui_log.propagate = False
    logging.info(f'Propagation set to False for module loggers!')

    # creating exclusive .log file for each module
    base_handler = logging.FileHandler('Base.log')
    light_handler = logging.FileHandler('Light.log')
    thermostat_handler = logging.FileHandler('Thermostat.log')
    gui_handler = logging.FileHandler('GUI.log')
    logging.info(f'Creating handlers for each module finished successfully!')

    # this format is for each module
    formatter = logging.Formatter('%(asctime)s | %(levelname)s: %(message)s')

    # setting the formatter to each handler
    base_handler.setFormatter(formatter)
    light_handler.setFormatter(formatter)
    thermostat_handler.setFormatter(formatter)
    gui_handler.setFormatter(formatter)
    logging.info(f'Customized formatter set to module handlers successfully!')

    # assigning the setting to each module
    base_log.addHandler(base_handler)
    light_log.addHandler(light_handler)
    thermostat_log.addHandler(thermostat_handler)
    gui_log.addHandler(gui_handler)
    logging.info(f'Customized handlers set to module loggers successfully!')

if __name__ == '__main__':
    main()