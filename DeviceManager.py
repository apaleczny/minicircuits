import re
import time
import socket
import select
from Attenuator import Attenuator

class DeviceManager(object):
    """ Detect and Manage Mini-Circuits Devices on the LAN """
    MINI_CIRCUITS_LISTENTING_PORT = 4950
    MINI_CIRCUITS_ANSWERING_PORT = 4951
    SOCKET_BUFFER_SIZE = 1024

    def discover_devices(self, discovery_time: int=30) -> [Attenuator]:
        """Discover Mini-Circuits Devices on the LAN

        :param discovery_time: time to wait (seconds) for devices to respond to broadcast
        :type discovery_time: int
        :returns: all detected devices
        :rtype: list
        """
        broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_socket.bind(('', 0))
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        msg = 'MCLDAT?' + '\n'
        broadcast_socket.sendto(msg, ('<broadcast>', self.MINI_CIRCUITS_LISTENTING_PORT))
        receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        receiver_socket.bind(('', self.MINI_CIRCUITS_ANSWERING_PORT))
        broadcast_responses = []
        timeout = time.time() + discovery_time
        while time.time() < timeout:
            ready = select.select([receiver_socket], [], [], timeout-time.time())
            if ready[0]:
                data, addr = receiver_socket.recvfrom(self.SOCKET_BUFFER_SIZE)
                broadcast_responses.append(data)
        discovered_devices = []
        for device in broadcast_responses:
            try:
                device_details = {}
                for field in device.splitlines():
                    if 'IP Address' in field:
                        ip_address_pattern = "IP Address=([\d\.]*)  Port: (\d+)"
                        match_ip_address = re.match(ip_address_pattern, field)
                        if match_ip_address:
                            device_details['IP Address'] = match_ip_address.group(1)
                            device_details['Port'] = match_ip_address.group(2)
                    else:
                        split_fields = re.split('[:=]|\s\s+', field)
                        for i in range(0, len(split_fields), 2):
                            device_details[split_fields[i].strip()] = split_fields[i+1].strip()
                discovered_devices.append(Attenuator(device_details))
            except:
                print("Invalid Device Description Response")
        return discovered_devices
