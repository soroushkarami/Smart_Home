from .Base import Base
import logging
import asyncio
import random

logger = logging.getLogger('Light')

class Light(Base):
    colorlist = ['Red', 'White', 'Blue', 'Green', 'Yellow', 'Purple']
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
        logger.debug(f'loc setter is called for ID {self._dev_id}...')
        if not value:
            logger.error(f'Nothing entered as location!')
            raise ValueError(f'Location cannot be empty for the light!')
        self._loc = value
        logger.info(f"{value} set as this {self.__class__.__name__}'s location!")

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value: str):
        logger.debug(f'color setter is called for ID {self._dev_id}...')
        if not isinstance(value, str):
            logger.error(f'A non-str input entered as color: {value}')
            raise TypeError(f'The color must be a string!')
        if not value:
            logger.error(f'Nothing entered as color!')
            raise ValueError(f'Color cannot be empty!')
        value = value.title()
        if value not in Light.colorlist:
            logger.error(f'{value} is an invalid color!')
            raise ValueError(f'Invalid color!')
        self._color = value
        logger.info(f"{value} set as this {self.__class__.__name__}'s color!")

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value: int):
        logger.debug(f'brightness setter is called for ID {self._dev_id}...')
        if not isinstance(value, int):
            logger.error(f'Non-int value entered as brightness!')
            raise TypeError(f'Please enter a number as brightness!')
        if not 0 <= value <= 100:
            logger.error(f'Out of range value entered as brightness!')
            raise ValueError(f'Brightness must be between 0 to 100%!')
        self._brightness = value
        logger.info(f'{value} successfully assigned as {self.name} brightness!')

    async def turn_on_logic(self):
        if self.brightness == 0:
            logger.warning(f'{self.name} brightness is 0, setting to 100%...')
            self.brightness = 100
        else:
            logger.info(f'{self.name} brightness: {self.brightness}%')

    def turn_off_logic(self):
        if self.brightness != 0:
            logger.warning(f'{self.name} brightness is {self.brightness}, setting to 0%...')
            self.brightness = 0
        else:
            logger.info(f'{self.name} brightness: {self.brightness}%')

    async def charging_logic(self):
        while self.battery < 100:
            self.battery += 1
            await asyncio.sleep(5)
            logger.info(f'Charging started: 1% : 5 sec')
        else:
            logger.info(f'{self.name} fully charged!')

    def connect_logic(self):
        main_section = '120.30.110.'
        counter = 0
        while counter <= 10:    # 10 chances
            # the range for lights is from 120.30.110.1 to 120.30.110.50
            last_section = random.randint(1, 50)
            assigned = ''.join([main_section, str(last_section)])
            counter += 1
            if assigned in Base.ip_list:
                logger.warning(f'IP {assigned} is already taken, trying another IP...')
                continue
            else:
                break
        else:
            logger.warning(f'No available IP found!')
            return 'failure'
        self._ip = assigned

    def color_change(self):
        logger.debug(f'color_change method is called for {self.name}...')
        if not self.is_on:
            logger.error(f'{self.__class__.__name__} {self.name} is off!')
            raise RuntimeError(f'Failure, {self.name} is off!')
        if self.is_charging:
            logger.error(f'{self.__class__.__name__} {self.name} is charging!')
            raise RuntimeError(f'Failure, {self.name} is charging!')
        for color in Light.colorlist:
            if color == self.color:
                logger.info(f'Color found: {color}')
                current_index = Light.colorlist.index(color)
                next_index = current_index + 1
                if next_index == len(Light.colorlist):
                    logger.warning(f'The end of color list reached, circling around...')
                    next_index = 0
                self.color = Light.colorlist[next_index]
                break
        else:
            logger.error(f'the color of the light is invalid: {self.color}')
            raise ValueError(f'Invalid color!')

    def get_info(self):
        base_info = super().get_info()
        return f'{base_info} | Location: {self.loc} | Color: {self.color} | Brightness: {self.brightness}'