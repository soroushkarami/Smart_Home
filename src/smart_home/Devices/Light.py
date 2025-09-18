from Base import Base
import logging
import asyncio
import random

class Light(Base):
    def __init__(self, name: str, battery: int, location: str, color :str, brightness: int = 0):
        super().__init__(name, battery)
        self.loc = location
        self.color = color
        if brightness != 0:
            self._is_on = True
        self.brightness = brightness

    @property
    def loc(self):
        return self._loc

    @loc.setter
    def loc(self, value: str):
        logging.debug(f'loc setter is called for ID {self._dev_id}...')
        if not value:
            logging.error(f'Nothing entered as location!')
            raise ValueError(f'Location cannot be empty!')
        self._loc = value
        logging.info(f"{value} set as this {self.__class__.__name__}'s location!")

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value: str):
        logging.debug(f'color setter is called for ID {self._dev_id}...')
        if not isinstance(value, str):
            logging.error(f'A non-str input entered as color: {value}')
            raise TypeError(f'The color must be a string!')
        if not value:
            logging.error(f'Nothing entered as color!')
            raise ValueError(f'Color cannot be empty!')
        value = value.title()
        if value not in ['Red', 'White', 'Blue', 'Green', 'Yellow', 'Purple']:
            logging.error(f'{value} is an invalid color!')
            raise ValueError(f'Invalid color!')
        self._color = value
        logging.info(f"{value} set as this {self.__class__.__name__}'s color!")

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value: int):
        logging.debug(f'brightness setter is called for ID {self._dev_id}...')
        if not isinstance(value, int):
            logging.error(f'Non-int value entered as brightness!')
            raise TypeError(f'Please enter a number as brightness!')
        if not 0 <= value <= 100:
            logging.error(f'Out of range value entered as brightness!')
            raise ValueError(f'Brightness must be between 0 to 100%!')
        self._brightness = value
        logging.info(f'{value} successfully assigned as {self.name} brightness!')

    def connect_logic(self):
        main_section = '120.30.110.'
        counter = 0
        while counter <= 10:    # 10 chances
            # the range for lights is from 120.30.110.1 to 120.30.110.50
            last_section = random.randint(1, 50)
            assigned = ''.join([main_section, str(last_section)])
            counter += 1
            if assigned in Base.ip_list:
                logging.warning(f'IP {assigned} is already taken, trying another IP...')
                continue
            else:
                break
        else:
            logging.warning(f'No available IP found!')
            return 'failure'
        self._ip = assigned

    def turn_on_logic(self):
        if self.brightness == 0:
            logging.warning(f'{self.name} brightness is 0, setting to 100%...')
            self.brightness = 100
        else:
            logging.info(f'{self.name} brightness: {self.brightness}%')

    def turn_off_logic(self):
        if self.brightness != 0:
            logging.warning(f'{self.name} brightness is {self.brightness}, setting to 0%...')
            self.brightness = 0
        else:
            logging.info(f'{self.name} brightness: {self.brightness}%')

    async def charging_logic(self):
        while self.battery < 100:
            self.battery += 1
            await asyncio.sleep(5)
            logging.info(f'Charging started: 1% : 5 sec')
        else:
            logging.info(f'{self.name} fully charged!')