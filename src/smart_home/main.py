from smart_home.gui.GUI import RegistrationGUI, StatusGUI
import logging
import tkinter as tk

def logging_setting():
    logging.debug(f'logging setting function is called...')
    # This config is just for the root .log file which is the log in main module
    logging.basicConfig(level= logging.DEBUG,
                format='%(asctime)s | %(levelname)s: %(message)s', filemode='w')

    # catching loggers from other modules
    base_log = logging.getLogger('Base')
    light_log = logging.getLogger('Light')
    gui_log = logging.getLogger('GUI')

    # setting their level
    base_log.setLevel(logging.DEBUG)
    light_log.setLevel(logging.DEBUG)
    gui_log.setLevel(logging.DEBUG)
    logging.info(f'Setting level for module loggers finished successfully!')

    # preventing propagating their messages to root .log
    base_log.propagate = False
    light_log.propagate = False
    gui_log.propagate = False
    logging.info(f'Propagation set to False for module loggers!')

    # creating exclusive .log file for each module
    base_handler = logging.FileHandler('Base.log')
    light_handler = logging.FileHandler('Light.log')
    gui_handler = logging.FileHandler('GUI.log')
    logging.info(f'Creating handlers for each module finished successfully!')

    # this format is for each module
    formatter = logging.Formatter('%(asctime)s | %(levelname)s: %(message)s')

    # setting the formatter to each handler
    base_handler.setFormatter(formatter)
    light_handler.setFormatter(formatter)
    gui_handler.setFormatter(formatter)
    logging.info(f'Customized formatter set to module handlers successfully!')

    # assigning the setting to each module
    base_log.addHandler(base_handler)
    light_log.addHandler(light_handler)
    gui_log.addHandler(gui_handler)
    logging.info(f'Customized handlers set to module loggers successfully!')

def main():
    my_registry = tk.Tk()
    my_registry.title(f'Registration')
    my_registry.geometry(f'400x400')

    devices = {}

    my_status = tk.Tk()
    my_status.title(f'Status')
    my_status.geometry(f'700x500')

    RegistrationGUI(my_registry, devices)
    StatusGUI(my_status, devices)

    my_registry.mainloop()
    my_status.mainloop()

if __name__ == '__main__':
    main()

