# -*- coding: utf-8 -*-
try:
    import RPi.GPIO as GPIO
except ImportError:
    raise ImportError(
        "You probably have to install RPi.GPIO"
    )
import time
import logging

logger = logging.getLogger(__name__)

__author__ = """Marco Roose"""
__email__ = 'marco.roose@gmx.de'
__version__ = '1.1.2'


class GenericHX711Exception(Exception):
    pass


class ParameterValidationError(Exception):
    pass


class HX711(object):
    # definitions for the hardware
    # defaults
    _channel = "A"
    _channel_a_gain = 64
    # properties
    _valid_channels = ['A', 'B']
    _valid_gains_for_channel_A = [64, 128]
    # define the minimum and maximum count for measures for an aggregated measure
    # this prevents from running the functions for a to long time
    min_measures = 2
    max_measures = 100

    def __init__(self, dout_pin, pd_sck_pin, gain=128, channel='A'):
        """
        :param dout_pin: number of the GPIO DOUT is connectedt to
        :type dout_pin: int
        :param pd_sck_pin: number of the GPIO SCK is connectedt to
        :type int
        :param gain: gain
        :type gain: int
        :param channel: selected channel
        :type channel: str
        """
        if (isinstance(dout_pin, int) and
            isinstance(pd_sck_pin, int)):  # just check of it is integer
            self._pd_sck = pd_sck_pin  # init pd_sck pin number
            self._dout = dout_pin  # init data pin number
        else:
            raise TypeError('dout_pin and pd_sck_pin have to be pin numbers.\nI have got dout_pin: ' \
                            + str(dout_pin) + \
                            ' and pd_sck_pin: ' + str(pd_sck_pin) + '\n')

        GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
        GPIO.setup(self._pd_sck, GPIO.OUT)  # pin _pd_sck is output only
        GPIO.setup(self._dout, GPIO.IN)  # pin _dout is input only
        self.channel = channel
        self.channel_a_gain = gain

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, channel):
        self._validate_channel_name(channel)
        self._channel = channel
        self._apply_setting()

    @property
    def channel_a_gain(self):
        return self._channel_a_gain

    @channel_a_gain.setter
    def channel_a_gain(self, channel_a_gain):
        if self.channel == "A":
            self._validate_gain_A_value(channel_a_gain)
            self._channel_a_gain = channel_a_gain
            self._apply_setting()
        else:
            logging.warning(
                """current channel != "A" so no need to set a gain"""
                """ current channel is '{channel}'""".format(channel=self.channel)
            )

    def power_down(self):
        """
        turn off the HX711
        :return: always True
        :rtype bool
        """
        GPIO.output(self._pd_sck, False)
        GPIO.output(self._pd_sck, True)
        time.sleep(0.01)
        return True

    def power_up(self):
        """
        power up the HX711

        :return: always True
        :rtype bool
        """
        GPIO.output(self._pd_sck, False)
        time.sleep(0.01)
        return True

    def reset(self):
        """
        reset the HX711 and prepare it for 	the next reading

        :return: True on success
        :rtype bool
        :raises GenericHX711Exception
        """
        logging.debug("power down")
        self.power_down()
        logging.debug("power up")
        self.power_up()
        logging.debug("read some raw data")
        result = self.get_raw_data(6)
        if result is False:
            raise GenericHX711Exception("failed to reset HX711")
        else:
            return True

    def _validate_measure_count(self, times):
        """
        check if "times" is within the borders defined in the class

        :param times: "times" to check
        :type times: int
        """
        if not self.min_measures <= times <= self.max_measures:
            raise ParameterValidationError(
                "{times} is not within the borders defined in the class".format(
                    times=times
                )
            )

    def _validate_channel_name(self, channel):
        """
        validate channel name
        :type channel: str
        :raises: ValueError
        """
        if channel not in self._valid_channels:
            raise ParameterValidationError('channel has to be "A" or "B". I got: ' + str(channel))

    def _validate_gain_A_value(self, gain_A):
        """
        validate a given value for gain_A

        :type gain_A: int
        :raises: ValueError
        """
        if gain_A not in self._valid_gains_for_channel_A:
            raise ParameterValidationError("{gain_A} is not a valid gain".format(gain_A=gain_A))

    def _apply_setting(self):
        """
        apply some setting by just do a read and wait a bit
        :param channel: channel to select
        :type channel: str
        :return: True if successful
        :rtype bool
        """
        # after changing channel or gain it has to wait 50 ms to allow adjustment.
        # the data before is garbage and cannot be used.
        self._read()
        time.sleep(0.5)
        return True

    def _ready(self):
        """
        check if ther is som data is ready to get read.
        :return True if there is some date
        :rtype bool
        """
        # if DOUT pin is low, data is ready for reading
        _is_ready = GPIO.input(self._dout) == 0
        logging.debug("check data ready for reading: {result}".format(
            result="YES" if _is_ready is True else "NO"
        ))
        return _is_ready

    def _set_channel_gain(self, num):
        """
        Finish data transmission from HX711 by setting
        next required gain and channel

        Only called from the _read function.
        :param num: how often so do the set (1...3)
        :type num: int
        :return True on success
        :rtype bool
        """
        if not 1 <= num <= 3:
            raise AttributeError(
                """"num" has to be in the range of 1 to 3"""
            )

        for _ in range(num):
            logging.debug("_set_channel_gain called")
            start_counter = time.perf_counter()  # start timer now.
            GPIO.output(self._pd_sck, True)  # set high
            GPIO.output(self._pd_sck, False)  # set low
            end_counter = time.perf_counter()  # stop timer
            time_elapsed = float(end_counter - start_counter)
            # check if HX711 did not turn off...
            # if pd_sck pin is HIGH for 60 µs and more the HX 711 enters power down mode.
            if time_elapsed >= 0.00006:
                logging.warning(
                    'setting gain and channel took more than 60µs. '
                    'Time elapsed: {:0.8f}'.format(time_elapsed)
                )
                # hx711 has turned off. First few readings are inaccurate.
                # Despite this reading was ok and data can be used.
                result = self.get_raw_data(times=6)  # set for the next reading.
                if result is False:
                    raise GenericHX711Exception("channel was not set properly")
        return True

    def _read(self, max_tries=40):
        """
        - read the bit stream from HX711 and convert to an int value.
        - validates the acquired data
        :param max_tries: how often to try to get data
        :type max_tries: int
        :return raw data
        :rtype: int
        """
        # start by setting the pd_sck to false
        GPIO.output(self._pd_sck, False)
        # init the counter
        ready_counter = 0

        # loop until HX711 is ready
        # halt when maximum number of tires is reached
        while self._ready() is False:
            time.sleep(0.01)  # sleep for 10 ms before next try
            ready_counter += 1  # increment counter
            # check loop count
            # and stop when defined maximum is reached
            if ready_counter >= max_tries:
                logging.debug('self._read() not ready after 40 trials\n')
                return False

        data_in = 0  # 2's complement data from hx 711
        # read first 24 bits of data
        for i in range(24):
            # start timer
            start_counter = time.perf_counter()
            # request next bit from HX711
            GPIO.output(self._pd_sck, True)
            GPIO.output(self._pd_sck, False)
            # stop timer
            end_counter = time.perf_counter()
            time_elapsed = float(end_counter - start_counter)

            # check if the hx 711 did not turn off:
            # if pd_sck pin is HIGH for 60 us and more than the HX 711 enters power down mode.
            if time_elapsed >= 0.00006:
                logging.debug('Reading data took longer than 60µs. Time elapsed: {:0.8f}'.format(time_elapsed))
                return False

            # Shift the bits as they come to data_in variable.
            # Left shift by one bit then bitwise OR with the new bit.
            data_in = (data_in << 1) | GPIO.input(self._dout)

        if self.channel == 'A' and self.channel_a_gain == 128:
            self._set_channel_gain(num=1)  # send one bit
        elif self.channel == 'A' and self.channel_a_gain == 64:
            self._set_channel_gain(num=3)  # send three bits
        else:
            self._set_channel_gain(num=2)  # send two bits

        logging.debug('Binary value as it has come: ' + str(bin(data_in)))

        # check if data is valid
        # 0x800000 is the lowest
        # 0x7fffff is the highest possible value from HX711
        if data_in == 0x7fffff or data_in == 0x800000:
            logging.debug('Invalid data detected: ' + str(data_in))
            return False

        # calculate int from 2's complement
        signed_data = 0
        if (data_in & 0x800000):  # 0b1000 0000 0000 0000 0000 0000 check if the sign bit is 1. Negative number.
            signed_data = -((data_in ^ 0xffffff) + 1)  # convert from 2's complement to int
        else:  # else do not do anything the value is positive number
            signed_data = data_in

        logging.debug('Converted 2\'s complement value: ' + str(signed_data))

        return signed_data

    def get_raw_data(self, times=5):
        """
        do some readings and aggregate them using the defined statistics function

        :param times: how many measures to aggregate
        :type times: int
        :return: the aggregate of the measured values
        :rtype float
        """

        self._validate_measure_count(times)

        data_list = []
        while len(data_list) < times:
            data = self._read()
            if data not in [False, -1]:
                data_list.append(data)

        return data_list
