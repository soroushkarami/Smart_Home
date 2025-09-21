from .Base import Base
import logging
import asyncio
import random

logger = logging.getLogger(__name__)

class Thermostat(Base):
    def __init__(self, name, battery, location):
        super().__init__(name, battery)
        self.loc = location
        self._temperature = 25
        self.target_temp = None
        self.mode = 'Off'
        self._in_process = False

    @property
    def loc(self):
        return self._loc

    @loc.setter
    def loc(self, value):
        logger.debug(f'loc setter is called for ID {self._dev_id}...')
        if not value:
            logger.error(f'Nothing entered as location!')
            raise ValueError(f'Location cannot be empty for the thermostat!')
        self._loc = value
        logger.info(f"{value} set as this thermostat's location!")

    @property
    def temperature(self):
        return self._temperature

    @property
    def target_temp(self):
        return self._target_temp

    @target_temp.setter
    def target_temp(self, value):
        logger.debug(f'target_temp setter is called for ID {self._dev_id}...')
        if not value:
            logger.error(f'Nothing entered as target temperature!')
            raise ValueError(f'Target temperature cannot be empty!')
        if not isinstance(value, (int, float)):
            logger.error(f'Non_number input entered!')
            raise TypeError(f'Invalid input!')
        self._target_temp = value
        logger.info(f"{value} set as this thermostat's target temperature!")
        if self.target_temp < self.temperature:
            self.mode = 'COOL'
        elif self.target_temp > self.temperature:
            self.mode = 'HEAT'
        else:
            self.mode = 'Off'

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        logger.debug(f'mode setter is called for ID {self._dev_id}...')
        if not value in ['COOL', 'HEAT']:
            logger.error(f'Invalid input entered as mode: {value}')
            raise ValueError(f'Invalid mode!')
        self._mode = value
        logger.info(f"Mode {value} assigned as this thermostat's mode!")

    @property
    def in_process(self):
        return self._in_process

    def target_set(self):
        # calls target_temp setter and tries to assign the user's target
        pass

    async def turn_on_logic(self):
        result = self.target_set()

        # if result successful then:
        if self.mode == 'COOL':
            await self.cooling()
        elif self.mode == 'HEAT':
            await self.heating()

    def turn_off_logic(self):
        self._in_process = False
        self._mode = 'Off'

    async def cooling(self):
        logger.debug(f'cooling method is called...')
        self._in_process = True
        while self.temperature > (self.target_temp + 0.05):
            self._temperature -= 0.05
            await asyncio.sleep(1)
            logger.info(f'Cooling started: -1°C : 20 sec')
        self._temperature = self.target_temp
        self._target_temp = None
        self._in_process = False
        logger.info(f'Cooling process finished, current temperature: {self.temperature}')

    async def heating(self):
        logger.debug(f'heating method is called...')
        self._in_process = True
        while self.temperature < (self.target_temp - 0.05):
            self._temperature += 0.1
            await asyncio.sleep(1)
            logger.info(f'Heating started: +1°C : 10 sec')
        self._temperature = self.target_temp
        self._target_temp = None
        self._in_process = False
        logger.info(f'Heating process finished, current temperature: {self.temperature}')

    async def charging_logic(self):
        while self.battery < 100:
            self.battery += 1
            await asyncio.sleep(10)
            logger.info(f'Charging started: 1% : 10 sec')
        else:
            logger.info(f'{self.name} fully charged!')

    def connect_logic(self):
        main_section = '120.30.110.'
        counter = 0
        while counter <= 5:    # 5 chances
            # the range for thermostats is from 120.30.110.100 to 120.30.110.120
            last_section = random.randint(100, 120)
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

    def get_info(self):
        base_info = super().get_info()
        return (f'{base_info} | Location: {self.loc} | Current Temperature: {self.temperature}°C'
                f' | in process? {self.in_process} | Mode: {self.mode}')