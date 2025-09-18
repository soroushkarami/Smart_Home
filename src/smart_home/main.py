import logging

def logging_setting():
    # This config is just for the root .log file which is the log in main module
    logging.basicConfig(level= logging.DEBUG,
                format='%(asctime)s | %(levelname)s: %(message)s', filemode='w')

    # catching loggers from other modules
    base_log = logging.getLogger('Base')
    light_log = logging.getLogger('Light')

    # setting their level
    base_log.setLevel(logging.DEBUG)
    light_log.setLevel(logging.DEBUG)

    # preventing propagating their messages to root .log
    base_log.propagate = False
    light_log.propagate = False

    # creating exclusive .log file for each module
    base_handler = logging.FileHandler('Base.log')
    light_handler = logging.FileHandler('Light.log')

    # this format is for each module
    formatter = logging.Formatter('%(asctime)s | %(levelname)s: %(message)s')

    # setting the formatter to each handler
    base_handler.setFormatter(formatter)
    light_handler.setFormatter(formatter)

    # assigning the setting to each module
    base_log.addHandler(base_handler)
    light_log.addHandler(light_handler)