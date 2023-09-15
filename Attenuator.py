import urllib

class AttenuatorException(Exception):
    """Exceptions for Attenuator Interactions"""
    pass


class Attenuator(object):
    """ Automate an Attenuator through its web APIs """
    START_MODE_LAST_ATTENUATION = 'L'
    START_MODE_FIXED_ATTENUATION = 'F'
    START_MODE_FACTORY_DEFAULT = 'N'

    DIRECTION_FORWARD = '0'
    DIRECTION_BACKWARDS = '1'
    DIRECTION_BIDIRECTIONAL = '2'
    DWELL_TIME_UNITS_MICROSECONDS = 'U'
    DWELL_TIME_UNITS_MILLISECONDS = 'M'
    DWELL_TIME_UNITS_SECONDS = 'S'
    MODE_ON = 'ON'
    MODE_OFF = 'OFF'

    def __init__(self, device_details):
        self.model_name = device_details['Model Name']
        self.serial_number = device_details['Serial Number']
        self.ip_address = device_details['IP Address']
        self.port = device_details['Port']
        self.subnet_mask = device_details['Subnet Mask']
        self.network_gateway = device_details['Network Gateway']
        self.mac_address = device_details['Mac Address']
        self._url = "http://%s:%s/" % (self.ip_address, self.port)
        self.password = None

    def __str__(self) -> str:
        return self._get_attenuator_details()

    def _get_attenuator_details(self) -> str:
        """String representation of the Attenuator object

        :returns: details of the attenuator
        :rtype: string
        """
        return "Model Name: " + self.model_name + "\n" + \
            "Serial Number: " + self.serial_number + "\n" + \
            "IP Address: " + self.ip_address + " Port: " + self.port + "\n" + \
            "Subnet Mask: " + self.subnet_mask + "\n" + \
            "Network Gateway: " + self.network_gateway + "\n" + \
            "Mac Address: " + self.mac_address

    def _send_http_cmd(self, command: str) -> str:
        """Send HTTP commands to the Attenuator

        :param command: the command to send
        :type command: string
        :returns: command result
        :rtype: string
        """
        if self.password:
            http_cmd = self._url + self.password + ';' + command
        else:
            http_cmd = self._url + command
        request_response = urllib.request.urlopen(urllib.request.Request(http_cmd),
                                           timeout=60)
        return request_response.read()

    def set_attenuation(self, db: float) -> None:
        """Sets the attenuation

        :param db: the attenation to set (in db)
        :type db: float
        """
        return_code = self._send_http_cmd(":SETATT=%s" % db)
        if return_code == '0':
            raise AttenuatorException('Command to set Attenuation Failed')
        if return_code == '2':
            raise AttenuatorException("Requested attenuation was higher than the allowed range, " +
                                        "the attenuation was set to the device's maximum")

    def get_attenuation(self) -> str:
        """Returns the current attenuation

        :returns: the current attenuation
        :rtype: string
        """
        return self._send_http_cmd(":ATT?")

    def set_startup_attenuation_mode(self, start_mode: str):
        """Set startup attenuation mode

        :param start_mode: the startup mode (use START_MODE_* constants)
        :type start_mode: string
        """
        return_code = self._send_http_cmd('STARTUPATT:INDICATOR:%s' % start_mode)
        if return_code != '1':
            raise AttenuatorException('Command to change attenuator startup mode failed')

    def get_startup_attenuation_mode(self) -> str:
        """Returns the startup mode currently in use by the attenuator

        :returns: the current start mode (see START_MODE_* constants)
        :rtype: string
        """
        return self._send_http_cmd(":STARTUPATT:INDICATOR?")

    def set_startup_attenuation_value(self, db: float):
        """Sets the attenuation value to be loaded when the attenuator is powered
           up in Fixed Attenuation mode

        :param db: the initial attenuation (in db)
        :type db: float
        """
        return_code = self._send_http_cmd(":STARTUPATT:VALUE:%s" % db)
        if return_code == '0':
            raise AttenuatorException('Command to set Attenuation Failed')
        if return_code == '2':
            raise AttenuatorException("Requested attenuation was higher than the allowed range," +
                                        "the attenuation was set to the device's maximum")

    def get_startup_attenuation_value(self) -> str:
        """Gets the attenuation value to be loaded when the attenuator is first powered
           up in Fixed Attenuation mode

        :returns: the attenuation value (in db)
        :rtype: string
        """
        return self._send_http_cmd(":STARTUPATT:VALUE?")

    def get_firmware_version(self) -> str:
        """Gets the firmware version of the attenuator

        :returns: the firmware version
        :rtype: string
        """
        return self._send_http_cmd(':FIRMWARE?')

    def hop_mode_set_points(self, points: int):
        """Sets the number of points to be used in the attenuation hop sequence

        :param points: the number of points to set
        :type points: int
        """
        return_code = self._send_http_cmd(':HOP:POINTS:%s' % points)
        if return_code != '1':
            raise AttenuatorException('Command to set number of hop points failed')

    def hop_mode_get_points(self) -> str:
        """Returns the number of points to be used in the attenuation hop sequence

        :returns: the number of points
        :rtype: string
        """
        return self._send_http_cmd(':HOP:POINTS?')

    def hop_mode_set_direction(self, direction: str):
        """Sets the direction in which the attenuator will progress through the list of attenuation hops

        :param direction: the sequence direction (see DIRECTION_* constants)
        :type direction: string
        """
        return_code = self._send_http_cmd(':HOP:DIRECTION:%s' % direction)
        if return_code != '1':
            raise AttenuatorException('Command to set hop direction failed')

    def hop_mode_get_direction(self) -> str:
        """Returns the direction in which the attenuator will progress through the lsit of attenuation

        :returns: the hop direction (see DIRECTION_* constants)
        :rtype: string
        """
        return self._send_http_cmd(':HOP:DIRECTION?')

    def hop_mode_set_indexed_point(self, point:int):
        """Select a point in the hop sequence to be further configured

        :param point: the point to select
        :type point: int
        """
        return_code = self._send_http_cmd(':HOP:POINT:%s' % point)
        if return_code != '1':
            raise AttenuatorException('Command to set indexed point failed')

    def hop_mode_get_indexed_point(self) -> str:
        """Returns the currently indexed attenuation point within the hop sequence

        :returns: the currently indexed point
        :rtype: string
        """
        return self._send_http_cmd(':HOP:POINT?')

    def hop_mode_set_point_dwell_time_units(self, units: str):
        """Sets the units to be used for the dwell time of the indexed point

        :param units: the units to set (see DWELL_TIME_UNITS_* constants)
        :type units: string
        """
        return_code = self._send_http_cmd(':HOP:DWELL_UNIT:%s' % units)
        if return_code != '1':
            raise AttenuatorException('Command to set dwell time units failed')

    def hop_mode_set_point_dwell_time(self, dwell_time: int):
        """Sets the dwell time of the indexed point in the hop sequence

        :param dwell_time: the time to set
        :type dwell_time: int
        """
        return_code = self._send_http_cmd(':HOP:DWELL:%s' % dwell_time)
        if return_code != '1':
            raise AttenuatorException('Command to set dwell time failed')

    def hop_mode_get_point_dwell_time(self) -> str:
        """Gets the dwell time (including units) of the indexed point in the hop sequence

        :returns: the dwell time (including units)
        :rtype: string
        """
        return self._send_http_cmd(':HOP:DWELL?')

    def hop_mode_set_point_attenuation(self, db: float):
        """Sets the attenuation of the indexed hop point

        :param db: the attenuation to set (in db)
        :type db: float
        """
        return_code = self._send_http_cmd(':HOP:ATT:%s' % db)
        if return_code != '1':
            raise AttenuatorException('Command to set point attenuation failed')

    def hop_mode_get_point_attenuation(self) -> str:
        """Returns the attenuation of the indexed hop point

        :returns: the attenaution (in db)
        :rtype: string
        """
        return self._send_http_cmd(':HOP:ATT?')

    def set_hop_mode(self, mode: str):
        """Enable or disable the hop sequence

        :param mode: on/off (see MODE_* constants)
        :type mode: string
        """
        return_code = self._send_http_cmd(':HOP:MODE:%s' % mode)
        if return_code != '1':
            raise AttenuatorException('Command to set hop mode failed')

    def sweep_mode_set_sweep_direction(self, direction: str):
        """Sets the direction in which the attenuation level will sweep

        :param direction: the direction (see DIRECTION_* constants)
        :type direction: string
        """
        return_code = self._send_http_cmd(':SWEEP:DIRECTION:%s' % direction)
        if return_code != '1':
            raise AttenuatorException('Command to set sweep direction failed')

    def sweep_mode_get_sweep_direction(self) -> str:
        """Returns the direction in which the attenuation level will sweep

        :returns: the direction of the attenuation sweep (see DIRECTION_* constants)
        :rtype: string
        """
        return self._send_http_cmd(':SWEEP:DIRECTION?')

    def sweep_mode_set_dwell_time_units(self, units: str):
        """Sets the units to be used for the sweep dwell time

        :param units: the units to set (see DWELL_TIME_UNITS_* constants)
        :type units: string
        """
        return_code = self._send_http_cmd(':SWEEP:DWELL_UNIT:%s' % units)
        if return_code != '1':
            raise AttenuatorException('Command to set sweep dwell time units failed')

    def sweep_mode_set_dwell_time(self, dwell_time: str):
        """Sets the dwell time to be used for the sweep

        :param dwell_time: the dwell time to set
        :type dwell_time: int
        """
        return_code = self._send_http_cmd(':SWEEP:DWELL:%s' % dwell_time)
        if return_code != '1':
            raise AttenuatorException('Command to set sweep dwell time failed')

    def sweep_mode_get_dwell_time(self) -> str:
        """Returns the dwell time (including units) of the attenuation sweep

        :returns: the dwell time (including units)
        :rtype: string
        """
        return self._send_http_cmd(':SWEEP:DWELL?')

    def sweep_mode_set_start_attenuation(self, db: float):
        """Sets the first attenuation level to be loaded during the sweep

        :param db: the attenuation level to set (in db)
        :type db: float
        """
        return_code = self._send_http_cmd(':SWEEP:START:%s' % db)
        if return_code != '1':
            raise AttenuatorException('Command to set sweep start attenuation failed')

    def sweep_mode_get_start_attenuation(self) -> str:
        """Returns the first attenuation level to be loaded during the sweep

        :returns: the start attenuation level (in db)
        :rtype: string
        """
        return self._send_http_cmd(':SWEEP:START?')

    def sweep_mode_set_stop_attenuation(self, db: float):
        """Sets the final attenuation level to be loaded during the sweep

        :param db: the attenuation level to be set (in db)
        :type db: float
        """
        return_code = self._send_http_cmd(':SWEEP:STOP:%s' % db)
        if return_code != '1':
            raise AttenuatorException('Command to set sweep stop attenuation failed')

    def sweep_mode_get_stop_attenuation(self) -> str:
        """Returns the final attenuation level to be loaded during the sweep

        :returns: the final attenuation level (in db)
        :type: string
        """
        return self._send_http_cmd(':SWEEP:STOP?')

    def sweep_mode_set_step_size(self, db: float):
        """Sets the attenuation step size

        :param db: the attenuation step size for the sweep (in db)
        :type db: float
        """
        return_code = self._send_http_cmd(':SWEEP:STEPSIZE:%s' % db)
        if return_code != '1':
            raise AttenuatorException('Command to set sweep step size failed')

    def sweep_mode_get_step_size(self) -> str:
        """Returns the attenuation step size

        :returns: the step size to be used for the sweep (in db)
        :rtype: string
        """
        return self._send_http_cmd(':SWEEP:STEPSIZE?')

    def set_sweep_mode(self, mode: str):
        """Enable or disable the sweep sequence

        :param mode: on/off (see MODE_* constants)
        :type mode: string
        """
        return_code = self._send_http_cmd(':SWEEP:MODE:%s' % mode)
        if return_code != '1':
            raise AttenuatorException('Command to set sweep mode failed')
    
