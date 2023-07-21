# alfen_eve_modbus_tcp

alfen_eve_modbus_tcp is a python library that collects data from Alfen Eve Car Chargers over Modbus TCP.

## Installation

To install, either clone this project and install using `setuptools`:

```python3 setup.py install```

or install the package from PyPi:

```pip3 install alfen-eve-modbus-tcp```

## Usage

The script `example.py` provides a minimal example of connecting to and displaying all registers from an Alfen Eve Car Charger over Modbus TCP.

```
usage: example.py [-h] [--timeout TIMEOUT] [--json] host port

positional arguments:
  host               Modbus TCP address
  port               Modbus TCP port

optional arguments:
  -h, --help         show this help message and exit
  --timeout TIMEOUT  Connection timeout
  --json             Output as JSON
```

Output:

```
Car Charger(192.168.2.136:502: timeout=1, retries=3):

Registers:
	Name: DIE_14966
	Manufacturer: Alfen NV
	Modbus Table Version: 1
	Firmware Version: 6.1.0-4159
	Station Serial Number: ACE0287582
	Date Year: 2023
	Date Month: 7
	Date day: 15
	Time hour: 21
	Time minute: 3
	Time second: 39
	Uptime: 125689398
	Time zone: 60
	Station Active Maximum Current: 25
	Temperature: 35.9375
	OCPP state: 1
	Nr of sockets: 1
	Availability: Operable
	Mode 3 state: NotConnected, A
	Actual Applied Max Current for Socket: 6.0
	Remaining time before fallback to safe current: 0
	Meter State: Initialised & Updated
	Meter Last Value Timestamp: 334
	Meter Type: RTU
	Voltage Phase L1N: 238.1899871826172
	Voltage Phase L2N: 240.63999938964844
	Voltage Phase L3N: 238.4399871826172
	Voltage Phase L1L2: nan
	Voltage Phase L2L3: nan
	Voltage Phase L3L1: nan
	Current N: nan
	Current Phase L1: 0.0
	Current Phase L2: 0.0
	Current Phase L3: 0.0
	Current Sum: nan
	Power Factor Phase L1: nan
	Power Factor Phase L2: nan
	Power Factor Phase L3: nan
	Power Factor Sum: 0.0
	Frequency: 50.000003814697266
	Real Power Phase L1: nan
	Real Power Phase L2: nan
	Real Power Phase L3: nan
	Real Power Sum: 0.0
	Apparent Power Phase L1: nan
	Apparent Power Phase L2: nan
	Apparent Power Phase L3: nan
	Apparent Power Sum: nan
	Reactive Power Phase L1: nan
	Reactive Power Phase L2: nan
	Reactive Power Phase L3: nan
	Reactive Power Sum: nan
	Real Energy Delivered Phase L1: nan
	Real Energy Delivered Phase L2: nan
	Real Energy Delivered Phase L3: nan
	Real Energy Delivered Sum: 31.0
	Real Energy Consumed Phase L1: nan
	Real Energy Consumed Phase L2: nan
	Real Energy Consumed Phase L3: nan
	Real Energy Consumed Sum: nan
	Apparent Energy Phase L1: nan
	Apparent Energy Phase L2: nan
	Apparent Energy Phase L3: nan
	Apparent Energy Sum: nan
	Reactive Energy Phase L1: nan
	Reactive Energy Phase L2: nan
	Reactive Energy Phase L3: nan
	Reactive Energy Sum: nan
	Modbus Slave Max Current: 6.0
	Active Load Balancing Safe Current: 6.0
	Modbus Slave Received Setpoint Accounted For: Yes
	Phases used for charging: 3
	SCN Name: 
	SCN Sockets: 0
	SCN Total Consumption Phase L1: 0.0
	SCN Total Consumption Phase L2: 0.0
	SCN Total Consumption Phase L3: 0.0
	SCN Actual Max Current Phase L1: 0.0
	SCN Actual Max Current Phase L2: 0.0
	SCN Actual Max Current Phase L3: 0.0
	SCN Max Current Phase L1: 6.0
	SCN Max Current Phase L2: 6.0
	SCN Max Current Phase L3: 6.0
	Max current valid time L1: 0
	Max current valid time L2: 0
	Max current valid time L3: 0
	SCN safe current: 6.0
	SCN Modbus Slave Max Current enable: Disabled
```

Passing `--json` returns:

```
{
    "c_name": "DIE_14966",
    "c_manufacturer": "Alfen NV",
    "c_modbus_table_version": 1,
    "c_firmware_version": "6.1.0-4159",
    "c_platform_type": "NG910",
    "c_station_serial_number": "ACE0287582",
    "c_date_year": 2023,
    "c_date_month": 7,
    "c_date_day": 15,
    "c_time_hour": 21,
    "c_time_minute": 10,
    "c_time_second": 48,
    "c_uptime": 126118547,
    "c_time_zone": 60,
    "station_active_max_current": 25,
    "temperature": 35.8125,
    "ocpp_state": 1,
    "nr_of_sockets": 1,
    "meter_state": 3,
    "meter_last_value_timestamp": 29,
    "meter_type": 0,
    "voltage_phase_L1N": 237.8199920654297,
    "voltage_phase_L2N": 240.75999450683594,
    "voltage_phase_L3N": 238.80999755859375,
    "voltage_phase_L1L2": NaN,
    "voltage_phase_L2L3": NaN,
    "voltage_phase_L3L1": NaN,
    "current_N": NaN,
    "current_phase_L1": 0.0,
    "current_phase_L2": 0.0,
    "current_phase_L3": 0.0,
    "current_sum": NaN,
    "power_factor_phase_L1": NaN,
    "power_factor_phase_L2": NaN,
    "power_factor_phase_L3": NaN,
    "power_factor_sum": 0.0,
    "frequency": 50.02000427246094,
    "real_power_phase_L1": NaN,
    "real_power_phase_L2": NaN,
    "real_power_phase_L3": NaN,
    "real_power_sum": 0.0,
    "apparent_power_phase_L1": NaN,
    "apparent_power_phase_L2": NaN,
    "apparent_power_phase_L3": NaN,
    "apparent_power_sum": NaN,
    "reactive_power_phase_L1": NaN,
    "reactive_power_phase_L2": NaN,
    "reactive_power_phase_L3": NaN,
    "reactive_power_sum": NaN,
    "real_energy_delivered_phase_L1": NaN,
    "real_energy_delivered_phase_L2": NaN,
    "real_energy_delivered_phase_L3": NaN,
    "real_energy_delivered_sum": 31.0,
    "real_energy_consumed_phase_L1": NaN,
    "real_energy_consumed_phase_L2": NaN,
    "real_energy_consumed_phase_L3": NaN,
    "real_energy_consumed_sum": NaN,
    "apparent_energy_phase_L1": NaN,
    "apparent_energy_phase_L2": NaN,
    "apparent_energy_phase_L3": NaN,
    "apparent_energy_sum": NaN,
    "reactive_energy_phase_L1": NaN,
    "reactive_energy_phase_L2": NaN,
    "reactive_energy_phase_L3": NaN,
    "reactive_energy_sum": NaN,
    "availability": 1,
    "mode_3_state": "A",
    "actual_applied_max_current": 6.0,
    "modbus_slave_max_current_valid_time": 0,
    "modbus_slave_max_current": 6.0,
    "active_load_balancing_safe_current": 6.0,
    "modbus_slave_received_setpoint_accounted_for": 1,
    "charge_using_1_or_3_phases": 3,
    "scn_name": "",
    "scn_sockets": 0,
    "scn_total_consumption_phase_l1": 0.0,
    "scn_total_consumption_phase_l2": 0.0,
    "scn_total_consumption_phase_l3": 0.0,
    "scn_actual_max_current_phase_l1": 0.0,
    "scn_actual_max_current_phase_l2": 0.0,
    "scn_actual_max_current_phase_l3": 0.0,
    "scn_max_current_phase_l1": 6.0,
    "scn_max_current_phase_l2": 6.0,
    "scn_max_current_phase_l3": 6.0,
    "remaining_valid_time_max_current_phase_l1": 0,
    "remaining_valid_time_max_current_phase_l2": 0,
    "remaining_valid_time_max_current_phase_l3": 0,
    "scn_safe_current": 6.0,
    "scn_modbus_slave_max_current_enable": 0
}
```


### Connecting

If you wish to use Modbus TCP the following parameters are relevant:

`host = IP or DNS name of your Modbus TCP device, required`  
`port = TCP port of the Modbus TCP device, required`  

Connecting to the car charger:

```
    >>> import alfen_eve_modbus_tcp

    # Car Charger over Modbus TCP
    >>>  car_charger = alfen_eve_modbus_tcp.CarCharger(host="192.168.2.136", port=502)
```

Test the connection, remember that only a single connection at a time is allowed:

```
    >>> car_charger.connect()
    True

    >>> car_charger.connected()
    True
```

While it is not necessary to explicitly call `connect()` before reading registers, you should do so before calling `connected()`. The connection can be closed by calling `disconnect()`.

Printing the class yields basic device parameters:

```
    >>> car_charger
    Car Charger(192.168.2.136:502: timeout=1, retries=3)
```

### Reading Registers

Reading a single input register by name:

```
    >>> car_charger.read("c_manufacturer")
    {'c_manufacturer': 'Alfen NV'}
```

Read all input registers using `read_all()`:

```
    >>> car_charger.read_all()
    {
        'c_name': 'DIE_14966',
        'c_manufacturer': 'Alfen NV',
        'c_modbus_table_version': 1,
        'c_firmware_version': '6.1.0-4159',
        'c_platform_type': 'NG910',
        'c_station_serial_number': 'ACE0287582',
        'c_date_year': 2023,
        'c_date_month': 7,
        'c_date_day': 15,
        'c_time_hour': 21,
        'c_time_minute': 23,
        'c_time_second': 45,
        'c_uptime': 126895863,
        'c_time_zone': 60,
        'station_active_max_current': 25,
        'temperature': 35.75,
        'ocpp_state': 1,
        'nr_of_sockets': 1,
        'meter_state': 3,
        'meter_last_value_timestamp': 602,
        'meter_type': 0,
        'voltage_phase_L1N': 239.1999969482422,
        'voltage_phase_L2N': 241.25,
        'voltage_phase_L3N': 238.6599884033203,
        'voltage_phase_L1L2': nan,
        'voltage_phase_L2L3': nan,
        'voltage_phase_L3L1': nan,
        'current_N': nan,
        'current_phase_L1': 0.0,
        'current_phase_L2': 0.0,
        'current_phase_L3': 0.0,
        'current_sum': nan,
        'power_factor_phase_L1': nan,
        'power_factor_phase_L2': nan,
        'power_factor_phase_L3': nan,
        'power_factor_sum': 0.0,
        'frequency': 50.060001373291016,
        'real_power_phase_L1': nan,
        'real_power_phase_L2': nan,
        'real_power_phase_L3': nan,
        'real_power_sum': 0.0,
        'apparent_power_phase_L1': nan,
        'apparent_power_phase_L2': nan,
        'apparent_power_phase_L3': nan,
        'apparent_power_sum': nan,
        'reactive_power_phase_L1': nan,
        'reactive_power_phase_L2': nan,
        'reactive_power_phase_L3': nan,
        'reactive_power_sum': nan,
        'real_energy_delivered_phase_L1': nan,
        'real_energy_delivered_phase_L2': nan,
        'real_energy_delivered_phase_L3': nan,
        'real_energy_delivered_sum': 31.0,
        'real_energy_consumed_phase_L1': nan,
        'real_energy_consumed_phase_L2': nan,
        'real_energy_consumed_phase_L3': nan,
        'real_energy_consumed_sum': nan,
        'apparent_energy_phase_L1': nan,
        'apparent_energy_phase_L2': nan,
        'apparent_energy_phase_L3': nan,
        'apparent_energy_sum': nan,
        'reactive_energy_phase_L1': nan,
        'reactive_energy_phase_L2': nan,
        'reactive_energy_phase_L3': nan,
        'reactive_energy_sum': nan,
        'availability': 1,
        'mode_3_state': 'A',
        'actual_applied_max_current': 6.0,
        'modbus_slave_max_current_valid_time': 0,
        'modbus_slave_max_current': 6.0,
        'active_load_balancing_safe_current': 6.0,
        'modbus_slave_received_setpoint_accounted_for': 1,
        'charge_using_1_or_3_phases': 3,
        'scn_name': '',
        'scn_sockets': 0,
        'scn_total_consumption_phase_l1': 0.0,
        'scn_total_consumption_phase_l2': 0.0,
        'scn_total_consumption_phase_l3': 0.0,
        'scn_actual_max_current_phase_l1': 0.0,
        'scn_actual_max_current_phase_l2': 0.0,
        'scn_actual_max_current_phase_l3': 0.0,
        'scn_max_current_phase_l1': 6.0,
        'scn_max_current_phase_l2': 6.0,
        'scn_max_current_phase_l3': 6.0,
        'remaining_valid_time_max_current_phase_l1': 0,
        'remaining_valid_time_max_current_phase_l2': 0,
        'remaining_valid_time_max_current_phase_l3': 0,
        'scn_safe_current': 6.0,
        'scn_modbus_slave_max_current_enable': 0
    }
```

### Register Details

If you need more information about a particular register, to look up the units or enumerations, for example:

```
    >>> car_charger.registers["modbus_slave_max_current"]
        # unit, address, length, type, datatype, valuetype, name, unit, batching
        (
            1,
            1210,
            2,
            <registerType.HOLDING: 2>,
            <registerDataType.FLOAT32: 6>,
            <class 'float'>,
            'Modbus Slave Max Current',
            'A',
            7
        )
```

## Contributing

Contributions are more than welcome.