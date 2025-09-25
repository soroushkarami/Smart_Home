from abc import ABC, abstractmethod 
import logging

logger = logging.getLogger(__name__)

class Base(ABC):
    all_devices = 0
    ip_list = []
    def __init__(self, name: str, battery: int):
        logger.debug(f'init method is called for {name}...')
        Base.all_devices += 1
        self._dev_id = Base.all_devices
        self.name = name
        self.battery = battery
        self._is_on = False
        self._is_charging = False
        self._is_connected = False
        self._ip = None

    @property
    def dev_id(self):
        return self._dev_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        logger.debug(f'name setter is called for ID {self._dev_id}...')
        if not value:
            logger.error(f'Nothing entered as name!')
            raise ValueError(f'Name cannot be empty!')
        self._name = value
        logger.info(f"{value} set as this {self.__class__.__name__}'s name!")

    @property
    def battery(self):
        return self._battery

    @battery.setter
    def battery(self, value):
        logger.debug(f'battery setter is called for ID {self._dev_id}...')
        if not isinstance(value, int):
            logger.error(f'Non-int value entered as battery!')
            raise TypeError(f'Please enter a number as battery percentage!')
        if not 0 <= value <= 100:
            logger.error(f'Out of range value entered as battery')
            raise ValueError(f'Battery must be between 0 to 100%!')
        logger.info(f'{value} successfully assigned as {self.name} battery percentage!')
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

    @property
    def ip(self):
        return self._ip

    def connect(self):
        logger.debug(f'connect method is called for ID {self.dev_id}...')
        if self.is_connected:
            logger.warning(f'{self.__class__.__name__} {self.name} is already connected!')
            return
        logger.debug(f'Calling connect_logic method for ID {self.dev_id}...')
        result = self.connect_logic()
        if result == 'failure':
            logger.error(f'Assigning IP address to {self.name} failed!')
            raise Exception(f'No IP found!')
        self._is_connected = True
        Base.ip_list.append(self.ip)
        logger.info(f'New IP assigned to {self.name} with ID {self.dev_id}, IP: {self.ip}')

    @abstractmethod
    def connect_logic(self):
        pass

    def disconnect(self):
        logger.debug(f'disconnect method is called for ID {self.dev_id}...')
        if not self.is_connected:
            logger.warning(f'{self.__class__.__name__} {self.name} is already disconnected!')
            return
        if self.ip in Base.ip_list:
            Base.ip_list.remove(self.ip)
        self._ip = None
        self._is_connected = False
        logger.info(f'{self.__class__.__name__} {self.name} with ID {self.dev_id} disconnected!')

    async def turn_on(self):
        logger.debug(f'turn_on method is called for ID {self.dev_id}...')
        if self.is_on:
            logger.warning(f'{self.__class__.__name__} {self.name} is already on!')
            return
        if self._battery == 0:
            logger.warning(f'{self.name} cannot be turned on! Charging needed!')
            return
        if self._is_charging:
            logger.warning(f'{self.name} is charging, cannot be turned on!')
            return
        logger.debug(f'Calling turn_on_logic method for ID {self.dev_id}...')
        await self.turn_on_logic()
        self._is_on = True
        logger.info(f'{self.__class__.__name__} {self.name} turned on!')

    @abstractmethod
    async def turn_on_logic(self):
        # Each device must determine its own logic
        pass

    def turn_off(self):
        logger.debug(f'turn_off method is called for ID {self.dev_id}...')
        if not self.is_on:
            logger.warning(f'{self.__class__.__name__} {self.name} is already off!')
            return
        logger.debug(f'Calling turn_off_logic method for ID {self.dev_id}...')
        self.turn_off_logic()
        self._is_on = False
        logger.info(f'{self.__class__.__name__} {self.name} turned off!')

    @abstractmethod
    def turn_off_logic(self):
        pass

    async def charging(self):
        logger.debug(f'charging method is called for ID {self.dev_id}...')
        if self.battery == 100:
            logger.warning(f'{self.name} with ID {self.dev_id} battery is already full!')
            return
        if self._is_on:
            logger.warning(f'{self.name} with ID {self.dev_id} cannot be charged as it is on!')
            return
        logger.debug(f'Calling charging_logic method for ID {self.dev_id}...')
        self._is_charging = True
        await self.charging_logic()

    @abstractmethod
    async def charging_logic(self):
        # this process should be async or else it'll freeze the program
        pass

    def stop_charging(self):
        logger.debug(f'stop_charging method is called for ID {self.dev_id}...')
        if not self._is_charging:
            logger.warning(f'{self.name} with ID {self.dev_id} is not in charging state!')
            return
        self._is_charging = False

    def toggle(self):
        logger.debug(f'toggle method is called for {self.name} with ID {self.dev_id}...')
        if self.is_on:
            self.turn_off()
        else:
            self.turn_on()

    def get_info(self):
        logger.debug(f'get_info method is called for ID {self.dev_id}...')
        return (f'Type: {self.__class__.__name__} | Name: {self.name} | ID: {self.dev_id} | '
                f'On? {self.is_on} | Connected? {self.is_connected} | Battery: {self.battery} | '
                f'Charging? {self.is_charging}')