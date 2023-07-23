# Module to read/write Modbus message over TCP to Alfen Eve (Single Pro-Line) car charger
# This code has been created by heavily making use of the code for SolarEdge inverter
# created by nmakel/solaredge_modbus on GitHub.com
# Basically I have adapted that code to reflect the situation for the Alfen CarCharger instead of the SolarEdge Inverter

import enum
import time
import syslog

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client import ModbusTcpClient
from pymodbus.register_read_message import ReadHoldingRegistersResponse


RETRIES = 3
TIMEOUT = 1

class registerType(enum.Enum):
    INPUT = 1
    HOLDING = 2

class registerDataType(enum.Enum):
    UINT16 = 1
    UINT32 = 2
    UINT64 = 3
    INT16 = 4
    SCALE = 4
    ACC32 = 5
    FLOAT32 = 6
    SEFLOAT = 7
    FLOAT64 = 8
    STRING = 9

METER_TYPE_MAP = {
    "0": "RTU",
    "1": "TCP/IP",
    "2": "UDP",
    "3": "P1",
    "4": "Other"
}

METER_STATE_MAP = {
    "1": "Initialised",
    "2": "Updated",
    "3": "Initialised & Updated",
    "4": "Warning",
    "5": "Warning & Initialised",
    "6": "Warning & Updated",
    "7": "Warning, Initialised & Updated",
    "8": "Error",
    "9": "Error & Initialised",
    "10": "Error & Updated",
    "11": "Error, Initialised & Updated",
    "12": "Error & Warning",
    "13": "Error, Warning & Initialised",
    "14": "Error, Warning & Updated",
    "15": "Error, Warning, Initialised & Updated"
}

AVAILABILITY_MAP = {
    "0": "Inoperable",
    "1": "Operable"
}

MODE_3_STATE_MAP = {
    "A": "NotConnected",
    "B1": "Connected",
    "B2": "Connected",
    "C1": "Connected",
    "C2": "Charging",
    "D1": "Connected",
    "D2": "Charging",
    "E": "NotConnected",
    "F": "Error"
}

SETPOINT_MAP = {
    "0": "No",
    "1": "Yes"
}

MODBUS_SLAVE_MAX_CURRENT_ENABLE_MAP = {
    "0": "Disabled",
    "1": "Enabled"
}

class AlfenEve:

    model = "Alfen Eve"
    wordorder = Endian.Big

    def __init__(
        self, host=False, port=False,
        timeout=TIMEOUT, retries=RETRIES,
        parent=False
    ):

        if parent:
            self.client = parent.client
            self.timeout = parent.timeout
            self.retries = parent.retries

            self.host = parent.host
            self.port = parent.port
        else:
            self.host = host
            self.port = port

            self.timeout = timeout
            self.retries = retries

            self.client = ModbusTcpClient(
                host=self.host,
                port=self.port,
                timeout=self.timeout
            )

    def __repr__(self):
        return f"{self.model}({self.host}:{self.port}: timeout={self.timeout}, retries={self.retries})"

    def _read_holding_registers(self, slave, address, length):
        for i in range(self.retries):
            if not self.connected():
                self.connect()
                time.sleep(0.1)
                continue

            result = self.client.read_holding_registers(address, length, slave=slave)

            if not isinstance(result, ReadHoldingRegistersResponse):
                continue
            if len(result.registers) != length:
                continue

            return BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big, wordorder=self.wordorder)

        return None

    def _write_holding_register(self, slave, address, value):
        return self.client.write_registers(address=address, values=value, slave=slave)

    def _encode_value(self, data, dtype):
        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=self.wordorder)

        try:
            if dtype == registerDataType.UINT16:
                builder.add_16bit_uint(data)
            elif dtype == registerDataType.UINT32:
                builder.add_32bit_uint(data)
            elif dtype == registerDataType.UINT64:
                builder.add_64bit_uint(data)
            elif dtype == registerDataType.INT16:
                builder.add_16bit_int(data)
            elif (dtype == registerDataType.FLOAT32 or
                  dtype == registerDataType.SEFLOAT):
                builder.add_32bit_float(data)
            elif dtype == registerDataType.FLOAT64:
                builder.add_64bit_float(data)
            elif dtype == registerDataType.STRING:
                builder.add_string(data)
            else:
                raise NotImplementedError(dtype)

        except NotImplementedError:
            raise

        return builder.to_registers()

    def _decode_value(self, data, length, dtype, vtype):
        try:
            if dtype == registerDataType.UINT16:
                decoded = data.decode_16bit_uint()
            elif (dtype == registerDataType.UINT32 or
                  dtype == registerDataType.ACC32):
                decoded = data.decode_32bit_uint()
            elif dtype == registerDataType.UINT64:
                decoded = data.decode_64bit_uint()
            elif dtype == registerDataType.INT16:
                decoded = data.decode_16bit_int()
            elif (dtype == registerDataType.FLOAT32 or
                dtype == registerDataType.SEFLOAT):
                decoded = data.decode_32bit_float()
            elif dtype == registerDataType.FLOAT64:
                decoded = data.decode_64bit_float()
            elif dtype == registerDataType.STRING:
                decoded = data.decode_string(length * 2).decode(encoding="utf-8", errors="ignore").replace("\x00", "").rstrip()
            else:
                raise NotImplementedError(dtype)

            return vtype(decoded)
        except NotImplementedError:
            raise

    def _read(self, value):
        slave, address, length, rtype, dtype, vtype, label, fmt, batch = value

        try:
            if rtype == registerType.INPUT:
                return self._decode_value(self._read_input_registers(slave, address, length), length, dtype, vtype)
            elif rtype == registerType.HOLDING:
                return self._decode_value(self._read_holding_registers(slave, address, length), length, dtype, vtype)
            else:
                raise NotImplementedError(rtype)
        except NotImplementedError:
            raise
        except AttributeError:
            return False

    def _read_all(self, values, rtype):
        addr_min = False
        addr_max = False

        for k, v in values.items():
            v_slave = v[0]
            v_addr = v[1]
            v_length = v[2]

            if addr_min is False:
                addr_min = v_addr
            if addr_max is False:
                addr_max = v_addr + v_length

            if v_addr < addr_min:
                addr_min = v_addr
            if (v_addr + v_length) > addr_max:
                addr_max = v_addr + v_length

        results = {}
        offset = addr_min
        length = addr_max - addr_min

        try:
            if rtype == registerType.INPUT:
                data = self._read_input_registers(v_slave, offset, length)
            elif rtype == registerType.HOLDING:
                data = self._read_holding_registers(v_slave, offset, length)
            else:
                raise NotImplementedError(rtype)

            if not data:
                return results

            for k, v in values.items():
                slave, address, length, rtype, dtype, vtype, label, fmt, batch = v

                if address > offset:
                    skip_bytes = address - offset
                    offset += skip_bytes
                    data.skip_bytes(skip_bytes * 2)

                results[k] = self._decode_value(data, length, dtype, vtype)
                offset += length
                #print(k, results[k])
        except NotImplementedError:
            raise

        return results

    def _write(self, value, data):
        slave, address, length, rtype, dtype, vtype, label, fmt, batch = value

        try:
            if rtype == registerType.HOLDING:
                return self._write_holding_register(slave, address, self._encode_value(data, dtype))
            else:
                raise NotImplementedError(rtype)
        except NotImplementedError:
            raise

    def connect(self):
        return self.client.connect()

    def disconnect(self):
        self.client.close()

    def connected(self):
        return self.client.is_socket_open()

    def read(self, key):
        if key not in self.registers:
            raise KeyError(key)

        return {key: self._read(self.registers[key])}

    def write(self, key, data):
        if key not in self.registers:
            raise KeyError(key)

        return self._write(self.registers[key], data)

    def read_all(self, rtype=registerType.HOLDING):
        registers = {k: v for k, v in self.registers.items() if (v[3] == rtype)}
        results = {}

        for batch in range(1, len(registers)):
            register_batch = {k: v for k, v in registers.items() if (v[8] == batch)}

            if not register_batch:
                break

            results.update(self._read_all(register_batch, rtype))

        return results


class CarCharger(AlfenEve):

    def __init__(self, *args, **kwargs):
        self.model = "Car Charger"
        self.wordorder = Endian.Big

        super().__init__(*args, **kwargs)

        self.registers = {
            # name, address, length, register, type, target type, description, unit, batch
            "c_name": (0xc8, 0x64, 17, registerType.HOLDING, registerDataType.STRING, str, "ALF_1000", "", 1),
            "c_manufacturer": (0xc8, 0x75, 5, registerType.HOLDING, registerDataType.STRING, str, "Alfen NV", "", 1),
            "c_modbus_table_version": (0xc8, 0x7a, 1, registerType.HOLDING, registerDataType.INT16, int, "1", "", 1),
            "c_firmware_version": (0xc8, 0x7b, 17, registerType.HOLDING, registerDataType.STRING, str, "3.4.0-2990", "", 1),
            "c_platform_type": (0xc8, 0x8c, 17, registerType.HOLDING, registerDataType.STRING, str, "NG910", "", 1),
            "c_station_serial_number": (0xc8, 0x9d, 11, registerType.HOLDING, registerDataType.STRING, str, "00000R000", "", 1),
            "c_date_year": (0xc8, 0xa8, 1, registerType.HOLDING, registerDataType.INT16, int, "2019", "1yr", 1),
            "c_date_month": (0xc8, 0xa9, 1, registerType.HOLDING, registerDataType.INT16, int, "03", "1mon", 1),
            "c_date_day": (0xc8, 0xaa, 1, registerType.HOLDING, registerDataType.INT16, int, "11", "1d", 1),
            "c_time_hour": (0xc8, 0xab, 1, registerType.HOLDING, registerDataType.INT16, int, "12", "1hr", 1),
            "c_time_minute": (0xc8, 0xac, 1, registerType.HOLDING, registerDataType.INT16, int, "01", "1min", 1),
            "c_time_second": (0xc8, 0xad, 1, registerType.HOLDING, registerDataType.INT16, int, "04", "1s", 1),
            "c_uptime": (0xc8, 0xae, 4, registerType.HOLDING, registerDataType.UINT64, int, "100", "0.001s", 1),
            "c_time_zone": (0xc8, 0xb2, 1, registerType.HOLDING, registerDataType.INT16, int, "Time zone offset to UTC in minutes", "1min", 1),

            "station_active_max_current": (0xc8, 0x44c, 2, registerType.HOLDING, registerDataType.FLOAT32, int, "The Actual Max Current", "A", 2),
            "temperature": (0xc8, 0x44e, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "Board Temperature", "degrees Celsius", 2),
            "ocpp_state": (0xc8, 0x450, 1, registerType.HOLDING, registerDataType.UINT16, int, "Back Office Connected", "", 2),
            "nr_of_sockets": (0xc8, 0x451, 1, registerType.HOLDING, registerDataType.UINT16, int, "Number of Sockets", "", 2),

            "meter_state": (0x1, 0x12c, 1, registerType.HOLDING, registerDataType.UINT16, int, "Bitmask with state", "", 3),
            "meter_last_value_timestamp": (0x1, 0x12d, 4, registerType.HOLDING, registerDataType.UINT64, int, "Milliseconds since last received measurement", "0.001s", 3),
            "meter_type": (0x1, 0x131, 1, registerType.HOLDING, registerDataType.UINT16, int, "0:RTU, 1:TCP/IP, 2:UDP, 3:P1, 4:other", "", 3),

            "voltage_phase_L1N": (0x1, 0x132, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "Voltage Phase L1N", "V", 4),
            "voltage_phase_L2N": (
            0x1, 0x134, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "Voltage Phase L2N", "V", 4),
            "voltage_phase_L3N": (
            0x1, 0x136, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "Voltage Phase L3N", "V", 4),
            "voltage_phase_L1L2": (
            0x1, 0x138, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "Voltage Phase L1L2", "V", 4),
            "voltage_phase_L2L3": (
                0x1, 0x13a, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "Voltage Phase L2L3", "V", 4),
            "voltage_phase_L3L1": (
                0x1, 0x13c, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "Voltage Phase L3L1", "V", 4),
            "current_N": (
                0x1, 0x13e, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "Current through N", "A", 4),
            "current_phase_L1": (
                0x1, 0x140, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "Current Phase L1", "A", 4),
            "current_phase_L2": (
                0x1, 0x142, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "Current Phase L2", "A", 4),
            "current_phase_L3": (
                0x1, 0x144, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "Current Phase L3", "A", 4),
            "current_sum": (
                0x1, 0x146, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "Current Sum", "A", 4),

            "power_factor_phase_L1": (
                0x1, 0x148, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "Power Factor Phase L1", "", 5),
            "power_factor_phase_L2": (
                0x1, 0x14a, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "Power Factor Phase L2", "", 5),
            "power_factor_phase_L3": (
                0x1, 0x14c, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "Power Factor Phase L3", "", 5),
            "power_factor_sum": (
                0x1, 0x14e, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "Power Factor Sum", "", 5),
            "frequency": (
                0x1, 0x150, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "Frequency", "Hz", 5),

            "real_power_phase_L1": (
                0x1, 0x152, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "Real Power Phase L1", "W", 5),
            "real_power_phase_L2": (
                0x1, 0x154, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "Real Power Phase L2", "W", 5),
            "real_power_phase_L3": (
                0x1, 0x156, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "Real Power Phase L3", "W", 5),
            "real_power_sum": (
                0x1, 0x158, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "Real Power Sum", "W", 5),

            "apparent_power_phase_L1": (
                0x1, 0x15a, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "Apparent Power Phase L1", "VA", 5),
            "apparent_power_phase_L2": (
                0x1, 0x15c, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "Apparent Power Phase L2", "VA", 5),
            "apparent_power_phase_L3": (
                0x1, 0x15e, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "Apparent Power Phase L3", "VA", 5),
            "apparent_power_sum": (
                0x1, 0x160, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "Apparent Power Sum", "VA", 5),

            "reactive_power_phase_L1": (
                0x1, 0x162, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "Reactive Power Phase L1", "VAr", 5),
            "reactive_power_phase_L2": (
                0x1, 0x164, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "Reactive Power Phase L2", "VAr", 5),
            "reactive_power_phase_L3": (
                0x1, 0x166, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "Reactive Power Phase L3", "VAr", 5),
            "reactive_power_sum": (
                0x1, 0x168, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "Reactive Power Sum", "VAr", 5),

            "real_energy_delivered_phase_L1": (
                0x1, 0x16a, 4, registerType.HOLDING, registerDataType.FLOAT64, float, "Real Energy Delivered Phase L1", "Wh", 6),
            "real_energy_delivered_phase_L2": (
                0x1, 0x16e, 4, registerType.HOLDING, registerDataType.FLOAT64, float, "Real Energy Delivered Phase L2", "Wh", 6),
            "real_energy_delivered_phase_L3": (
                0x1, 0x172, 4, registerType.HOLDING, registerDataType.FLOAT64, float, "Real Energy Delivered Phase L3", "Wh", 6),
            "real_energy_delivered_sum": (
                0x1, 0x176, 4, registerType.HOLDING, registerDataType.FLOAT64, float, "Real Energy Delivered Sum", "Wh", 6),

            "real_energy_consumed_phase_L1": (
                0x1, 0x17a, 4, registerType.HOLDING, registerDataType.FLOAT64, float, "Real Energy Consumed Phase L1", "Wh", 6),
            "real_energy_consumed_phase_L2": (
                0x1, 0x17e, 4, registerType.HOLDING, registerDataType.FLOAT64, float, "Real Energy Consumed Phase L2", "Wh", 6),
            "real_energy_consumed_phase_L3": (
                0x1, 0x182, 4, registerType.HOLDING, registerDataType.FLOAT64, float, "Real Energy Consumed Phase L3", "Wh", 6),
            "real_energy_consumed_sum": (
                0x1, 0x186, 4, registerType.HOLDING, registerDataType.FLOAT64, float, "Real Energy Consumed Sum", "Wh", 6),

            "apparent_energy_phase_L1": (
                0x1, 0x18a, 4, registerType.HOLDING, registerDataType.FLOAT64, float, "Apparent Energy Phase L1", "VAh", 6),
            "apparent_energy_phase_L2": (
                0x1, 0x18e, 4, registerType.HOLDING, registerDataType.FLOAT64, float, "Apparent Energy Phase L2", "VAh", 6),
            "apparent_energy_phase_L3": (
                0x1, 0x192, 4, registerType.HOLDING, registerDataType.FLOAT64, float, "Apparent Energy Phase L3", "VAh", 6),
            "apparent_energy_sum": (
                0x1, 0x196, 4, registerType.HOLDING, registerDataType.FLOAT64, float, "Apparent Energy Sum", "VAh", 6),

            "reactive_energy_phase_L1": (
                0x1, 0x19a, 4, registerType.HOLDING, registerDataType.FLOAT64, float, "Reactive Energy Phase L1", "VArh", 6),
            "reactive_energy_phase_L2": (
                0x1, 0x19e, 4, registerType.HOLDING, registerDataType.FLOAT64, float, "Reactive Energy Phase L2", "VArh", 6),
            "reactive_energy_phase_L3": (
                0x1, 0x1a2, 4, registerType.HOLDING, registerDataType.FLOAT64, float, "Reactive Energy Phase L3", "VArh", 6),
            "reactive_energy_sum": (
                0x1, 0x1a6, 4, registerType.HOLDING, registerDataType.FLOAT64, float, "Reactive Energy Sum", "VArh", 6),

            "availability": (
                0x1, 0x4b0, 1, registerType.HOLDING, registerDataType.UINT16, int, "1: Operative; 0: Inoperative", "",
                7),
            "mode_3_state": (0x1, 0x4b1, 5, registerType.HOLDING, registerDataType.STRING, str, "61851 states",
                             "", 7),
            "actual_applied_max_current": (
                0x1, 0x4b6, 2, registerType.HOLDING, registerDataType.FLOAT32, float,
                "Actual Applied Max Current for Socket", "A", 7),
            "modbus_slave_max_current_valid_time": (
                0x1, 0x4b8, 2, registerType.HOLDING, registerDataType.UINT32, int,
                "Remaining time before fallback to safe current", "1s", 7),
            "modbus_slave_max_current": (
                0x1, 0x4ba, 2, registerType.HOLDING, registerDataType.FLOAT32, float,
                "Modbus Slave Max Current", "A", 7),
            "active_load_balancing_safe_current": (
                0x1, 0x4bc, 2, registerType.HOLDING, registerDataType.FLOAT32, float,
                "Active Load Balancing Safe Current", "A", 7),
            "modbus_slave_received_setpoint_accounted_for": (
                0x1, 0x4be, 1, registerType.HOLDING, registerDataType.UINT16, int,
                "Modbus Slave Received Setpoint Accounted For", "", 7),
            "charge_using_1_or_3_phases": (
                0x1, 0x4bf, 1, registerType.HOLDING, registerDataType.UINT16, int,
                "Phases used for charging", "phases", 7),

            "scn_name": (0xc8, 0x578, 4, registerType.HOLDING, registerDataType.STRING, str, "", "", 8),
            "scn_sockets": (0xc8, 0x57c, 1, registerType.HOLDING, registerDataType.UINT16, int, "", "1A", 8),
            "scn_total_consumption_phase_l1": (0xc8, 0x57d, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "", "1A", 8),
            "scn_total_consumption_phase_l2": (0xc8, 0x57f, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "", "1A", 8),
            "scn_total_consumption_phase_l3": (0xc8, 0x581, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "", "1A", 8),
            "scn_actual_max_current_phase_l1": (0xc8, 0x583, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "", "1A", 8),
            "scn_actual_max_current_phase_l2": (0xc8, 0x585, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "", "1A", 8),
            "scn_actual_max_current_phase_l3": (0xc8, 0x587, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "", "1A", 8),
            "scn_max_current_phase_l1": (0xc8, 0x589, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "", "1A", 8),
            "scn_max_current_phase_l2": (0xc8, 0x58b, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "", "1A", 8),
            "scn_max_current_phase_l3": (0xc8, 0x58d, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "", "1A", 8),
            "remaining_valid_time_max_current_phase_l1": (0xc8, 0x58f, 2, registerType.HOLDING, registerDataType.UINT32, int, "Max current valid time", "1s", 8),
            "remaining_valid_time_max_current_phase_l2": (0xc8, 0x591, 2, registerType.HOLDING, registerDataType.UINT32, int, "Max current valid time", "1s", 8),
            "remaining_valid_time_max_current_phase_l3": (0xc8, 0x593, 2, registerType.HOLDING, registerDataType.UINT32, int, "Max current valid time", "1s", 8),
            "scn_safe_current": (0xc8, 0x595, 2, registerType.HOLDING, registerDataType.FLOAT32, float, "Configured SCN safe current", "1A", 8),
            "scn_modbus_slave_max_current_enable": (0xc8, 0x597, 1, registerType.HOLDING, registerDataType.UINT16, int, "1: Enabled; 0: Disabled", "1A",
            8)

        }

    def pause_charging(self):
        PAUSE_CURRENT = 5
        syslog.syslog("Stop Charging...")
        value = self.read('modbus_slave_max_current')
        current = value['modbus_slave_max_current']
        syslog.syslog(f"Current usage in A: {current}")
        if current > 5.5:
            syslog.syslog("Pausing...")
            self.set_current(PAUSE_CURRENT)
            syslog.syslog("Paused...")
        else:
            syslog.syslog("Already paused charging...")

    def switch_phase(self, phases):
        if (phases == 1 or phases == 3):
            current_phases = self.read('charge_using_1_or_3_phases')['charge_using_1_or_3_phases']
            if current_phases == phases:
                syslog.syslog(f"No need to switch, already at {phases} phase...")
            else:
                try:
                    syslog.syslog(f"Switch to {phases} phase(s)...")
                    syslog.syslog(f"Current phase(s): {current_phases}")
                    self.write('charge_using_1_or_3_phases', phases)
                    syslog.syslog("Switched...")
                except Exception as e:
                    syslog.syslog(e)
                finally:
                    current_phases = self.read('charge_using_1_or_3_phases')['charge_using_1_or_3_phases']
                    syslog.syslog(f"Current phase(s): {current_phases}")
        else:
            syslog.syslog(f"Invalid # of phases: {phases}...")

    def set_current(self, current):
        self.write('modbus_slave_max_current', current)
