# minicircuits
Python Interface for MiniCircuits Attenuators

Example Usage


from DeviceManager import DeviceManager
```
device_manager = DeviceManager()
attenuators = device_manager.discover_devices(5)
print(attenuators)
for attenuator in attenuators:
    if attenuator.serial_number == "1234":
        my_attenuator = attenuator

my_attenuator.set_attenuation(40)
print(my_attenuator.get_attenuation())
```
