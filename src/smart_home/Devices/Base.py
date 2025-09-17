from abc import ABC, abstractmethod 
import logging

logging.basicConfig(level=logging.INFO, format=f'%(levelname)s: %(message)s')

class Base(ABC):
    all_devices = 0
    def __init__(self, name: str, battery: int):
        logging.debug(f'init method is called for {name}...')
        Base.all_devices += 1
        self._dev_id = Base.all_devices
        self.name = name
        self.battery = battery
        self._is_on = False
        self._is_connected = False
        self._is_charging = False

    @property
    def dev_id(self):
        return self._dev_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        logging.debug(f'name setter is called for ID {self._dev_id}...')
        if not value:
            logging.error(f'Nothing entered as name!')
            raise ValueError(f'Name cannot be empty!')
        self._name = value
        logging.info(f"{value} set as this {self.__class__.__name__}'s name!")

    @property
    def battery(self):
        return self._battery

    @battery.setter
    def battery(self, value):
        logging.debug(f'battery setter is called for ID {self._dev_id}...')
        if not isinstance(value, int):
            logging.error(f'Non-int value entered as battery!')
            raise TypeError(f'Please enter a number as battery percentage!')
        if not 0 <= value <= 100:
            logging.error(f'Out of range value entered as battery')
            raise ValueError(f'Battery must be between 0 to 100%!')
        logging.info(f'{value} successfully assigned as {self.name} battery percentage!')
        self._battery = value

    @property
    def is_on(self):
        return self._is_on

    @property
    def is_connected(self):
        return self._is_connected

    @property
    def is_charging(self):
        return self._is_charging

    def connect(self):
        logging.debug(f'connect method is called for ID {self.dev_id}...')
        if self.is_connected:
            logging.warning(f'{self.__class__.__name__} {self.name} is already connected!')
            return
        logging.debug(f'Calling connect_logic method for ID {self.dev_id}...')
        self.connect_logic()
        self._is_connected = True
        logging.info(f'{self.__class__.__name__} {self.name} connected!')

    @abstractmethod
    def connect_logic(self):
        pass

    def disconnect(self):
        logging.debug(f'disconnect method is called for ID {self.dev_id}...')
        if not self.is_connected:
            logging.warning(f'{self.__class__.__name__} {self.name} is already disconnected!')
            return
        logging.debug(f'Calling disconnect_logic method for ID {self.dev_id}...')
        self.disconnect_logic()
        self._is_connected = False
        logging.info(f'{self.__class__.__name__} {self.name} disconnected!')

    @abstractmethod
    def disconnect_logic(self):
        pass

    def turn_on(self):
        logging.debug(f'turn_on method is called for ID {self.dev_id}...')
        if self.is_on:
            logging.warning(f'{self.__class__.__name__} {self.name} is already on!')
            return
        if self._battery == 0:
            logging.warning(f'{self.name} cannot be turned on! Charging needed!')
            return
        if self._is_charging:
            logging.warning(f'{self.name} is charging, cannot be turned on!')
            return
        logging.debug(f'Calling turn_on_logic method for ID {self.dev_id}...')
        self.turn_on_logic()
        self._is_on = True
        logging.info(f'{self.__class__.__name__} {self.name} turned on!')

    @abstractmethod
    def turn_on_logic(self):
        # Each device must determine its own logic
        pass

    def turn_off(self):
        logging.debug(f'turn_off method is called for ID {self.dev_id}...')
        if not self.is_on:
            logging.warning(f'{self.__class__.__name__} {self.name} is already off!')
            return
        logging.debug(f'Calling turn_off_logic method for ID {self.dev_id}...')
        self.turn_off_logic()
        self._is_on = False
        logging.info(f'{self.__class__.__name__} {self.name} turned off!')

    @abstractmethod
    def turn_off_logic(self):
        pass

    def charging(self):
        logging.debug(f'charging method is called for ID {self.dev_id}...')
        if self.battery == 100:
            logging.warning(f'{self.name} with ID {self.dev_id} battery is already full!')
            return
        if self._is_on:
            logging.warning(f'{self.name} with ID {self.dev_id} cannot be charged as it is on!')
            return
        logging.debug(f'Calling charging_logic method for ID {self.dev_id}...')
        self._is_charging = True
        self.charging_logic()

    @abstractmethod
    def charging_logic(self):
        pass

    def stop_charging(self):
        logging.debug(f'stop_charging method is called for ID {self.dev_id}...')
        if not self._is_charging:
            logging.warning(f'{self.name} with ID {self.dev_id} is not in charging state!')
            return
        self._is_charging = False

    def toggle(self):
        logging.debug(f'toggle method is called for {self.name} with ID {self.dev_id}...')
        if self.is_on:
            self.turn_off()
        else:
            self.turn_on()

    def get_info(self):
        logging.debug(f'get_info method is called for ID {self.dev_id}...')
        return (f'Type: {self.__class__.__name__} | Name: {self.name} | ID: {self.dev_id} | '
                f'On? {self.is_on} | Connected? {self.is_connected} | Battery: {self.battery}'
                f'Charging? {self.is_charging}')