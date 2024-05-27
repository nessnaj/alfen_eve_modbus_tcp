#!/usr/bin/env python3

# This code has been created by heavily making use of the code for SolarEdge inverter
# created by nmakel/solaredge_modbus on GitHub.com
# Basically I have adapted that code to reflect the situation for the Alfen Eve CarCharger instead of the SolarEdge Inverter

import argparse
import json
import time

import alfen_eve_modbus_tcp


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("host", type=str, help="Modbus TCP address")
    argparser.add_argument("port", type=int, help="Modbus TCP port")
    argparser.add_argument("--timeout", type=int, default=1, help="Connection timeout")
    argparser.add_argument("--json", action="store_true", default=False, help="Output as JSON")
    args = argparser.parse_args()

    car_charger = alfen_eve_modbus_tcp.CarCharger(
        host=args.host,
        port=args.port,
        timeout=args.timeout
    )

    time.sleep(1)
    status = car_charger.connect()
    print(status)

    #car_charger.set_charge_profile(3,6)

    values = {}
    values['mode_3_state'] = False
    #values['scn_name'] = False
    #print(values)
    #while (values['mode_3_state'] == False): # or (values['scn_name'] == False):
    while (values['mode_3_state'] == False):
        print("Attempt")
        values = car_charger.read("mode_3_state")
        #values = car_charger.read("scn_name")
        #print(values)

    values = car_charger.read_all()
    print(values)

    if args.json:
        print(json.dumps(values, indent=4))
    else:
        print(f"{car_charger}:")
        print("\nRegisters:")

        print(f"\tName: {values['c_name']}")
        print(f"\tManufacturer: {values['c_manufacturer']}")
        print(f"\tModbus Table Version: {values['c_modbus_table_version']}")
        print(f"\tFirmware Version: {values['c_firmware_version']}")
        print(f"\tStation Serial Number: {values['c_station_serial_number']}")
        print(f"\tDate Year: {values['c_date_year']}")
        print(f"\tDate Month: {values['c_date_month']}")
        print(f"\tDate day: {values['c_date_day']}")
        print(f"\tTime hour: {values['c_time_hour']}")
        print(f"\tTime minute: {values['c_time_minute']}")
        print(f"\tTime second: {values['c_time_second']}")
        print(f"\tUptime: {values['c_uptime']}")
        print(f"\tTime zone: {values['c_time_zone']}")

        print(f"\tStation Active Maximum Current: {values['station_active_max_current']}")
        print(f"\tTemperature: {values['temperature']}")
        print(f"\tOCPP state: {values['ocpp_state']}")
        print(f"\tNr of sockets: {values['nr_of_sockets']}")

        print(f"\tAvailability: {alfen_eve_modbus_tcp.AVAILABILITY_MAP[str(values['availability'])]}")
        print(f"\tMode 3 state: {alfen_eve_modbus_tcp.MODE_3_STATE_MAP[values['mode_3_state']]}, {values['mode_3_state']}")
        print(f"\tActual Applied Max Current for Socket: {values['actual_applied_max_current']}")
        print(f"\tRemaining time before fallback to safe current: {values['modbus_slave_max_current_valid_time']}")

        print(f"\tMeter State: {alfen_eve_modbus_tcp.METER_STATE_MAP[str(values['meter_state'])]}")
        print(f"\tMeter Last Value Timestamp: {values['meter_last_value_timestamp']}")
        print(f"\tMeter Type: {alfen_eve_modbus_tcp.METER_TYPE_MAP[str(values['meter_type'])]}")

        print(f"\tVoltage Phase L1N: {values['voltage_phase_L1N']}")
        print(f"\tVoltage Phase L2N: {values['voltage_phase_L2N']}")
        print(f"\tVoltage Phase L3N: {values['voltage_phase_L3N']}")
        print(f"\tVoltage Phase L1L2: {values['voltage_phase_L1L2']}")
        print(f"\tVoltage Phase L2L3: {values['voltage_phase_L2L3']}")
        print(f"\tVoltage Phase L3L1: {values['voltage_phase_L3L1']}")
        print(f"\tCurrent N: {values['current_N']}")
        print(f"\tCurrent Phase L1: {values['current_phase_L1']}")
        print(f"\tCurrent Phase L2: {values['current_phase_L2']}")
        print(f"\tCurrent Phase L3: {values['current_phase_L3']}")
        print(f"\tCurrent Sum: {values['current_sum']}")

        print(f"\tPower Factor Phase L1: {values['power_factor_phase_L1']}")
        print(f"\tPower Factor Phase L2: {values['power_factor_phase_L2']}")
        print(f"\tPower Factor Phase L3: {values['power_factor_phase_L3']}")
        print(f"\tPower Factor Sum: {values['power_factor_sum']}")

        print(f"\tFrequency: {values['frequency']}")

        print(f"\tReal Power Phase L1: {values['real_power_phase_L1']}")
        print(f"\tReal Power Phase L2: {values['real_power_phase_L2']}")
        print(f"\tReal Power Phase L3: {values['real_power_phase_L3']}")
        print(f"\tReal Power Sum: {values['real_power_sum']}")

        print(f"\tApparent Power Phase L1: {values['apparent_power_phase_L1']}")
        print(f"\tApparent Power Phase L2: {values['apparent_power_phase_L2']}")
        print(f"\tApparent Power Phase L3: {values['apparent_power_phase_L3']}")
        print(f"\tApparent Power Sum: {values['apparent_power_sum']}")

        print(f"\tReactive Power Phase L1: {values['reactive_power_phase_L1']}")
        print(f"\tReactive Power Phase L2: {values['reactive_power_phase_L2']}")
        print(f"\tReactive Power Phase L3: {values['reactive_power_phase_L3']}")
        print(f"\tReactive Power Sum: {values['reactive_power_sum']}")

        print(f"\tReal Energy Delivered Phase L1: {values['real_energy_delivered_phase_L1']}")
        print(f"\tReal Energy Delivered Phase L2: {values['real_energy_delivered_phase_L2']}")
        print(f"\tReal Energy Delivered Phase L3: {values['real_energy_delivered_phase_L3']}")
        print(f"\tReal Energy Delivered Sum: {values['real_energy_delivered_sum']}")

        print(f"\tReal Energy Consumed Phase L1: {values['real_energy_consumed_phase_L1']}")
        print(f"\tReal Energy Consumed Phase L2: {values['real_energy_consumed_phase_L2']}")
        print(f"\tReal Energy Consumed Phase L3: {values['real_energy_consumed_phase_L3']}")
        print(f"\tReal Energy Consumed Sum: {values['real_energy_consumed_sum']}")

        print(f"\tApparent Energy Phase L1: {values['apparent_energy_phase_L1']}")
        print(f"\tApparent Energy Phase L2: {values['apparent_energy_phase_L2']}")
        print(f"\tApparent Energy Phase L3: {values['apparent_energy_phase_L3']}")
        print(f"\tApparent Energy Sum: {values['apparent_energy_sum']}")

        print(f"\tReactive Energy Phase L1: {values['reactive_energy_phase_L1']}")
        print(f"\tReactive Energy Phase L2: {values['reactive_energy_phase_L2']}")
        print(f"\tReactive Energy Phase L3: {values['reactive_energy_phase_L3']}")
        print(f"\tReactive Energy Sum: {values['reactive_energy_sum']}")

        print(f"\tModbus Slave Max Current: {values['modbus_slave_max_current']}")
        print(f"\tActive Load Balancing Safe Current: {values['active_load_balancing_safe_current']}")
        print(f"\tModbus Slave Received Setpoint Accounted For: {alfen_eve_modbus_tcp.SETPOINT_MAP[str(values['modbus_slave_received_setpoint_accounted_for'])]}")
        print(f"\tPhases used for charging: {values['charge_using_1_or_3_phases']}")

        #print(f"\tSCN Name: {values['scn_name']}")
        #print(car_charger.read("scn_name"))
        #print(f"\tSCN Sockets: {values['scn_sockets']}")
        #print(f"\tSCN Total Consumption Phase L1: {values['scn_total_consumption_phase_l1']}")
        #print(f"\tSCN Total Consumption Phase L2: {values['scn_total_consumption_phase_l2']}")
        #print(f"\tSCN Total Consumption Phase L3: {values['scn_total_consumption_phase_l3']}")
        #print(f"\tSCN Actual Max Current Phase L1: {values['scn_actual_max_current_phase_l1']}")
        #print(f"\tSCN Actual Max Current Phase L2: {values['scn_actual_max_current_phase_l2']}")
        #print(f"\tSCN Actual Max Current Phase L3: {values['scn_actual_max_current_phase_l3']}")
        #print(f"\tSCN Max Current Phase L1: {values['scn_max_current_phase_l1']}")
        #print(f"\tSCN Max Current Phase L2: {values['scn_max_current_phase_l2']}")
        #print(f"\tSCN Max Current Phase L3: {values['scn_max_current_phase_l3']}")
        #print(f"\tMax current valid time L1: {values['remaining_valid_time_max_current_phase_l1']}")
        #print(f"\tMax current valid time L2: {values['remaining_valid_time_max_current_phase_l2']}")
        #print(f"\tMax current valid time L3: {values['remaining_valid_time_max_current_phase_l3']}")
        #print(f"\tSCN safe current: {values['scn_safe_current']}")
        #print(car_charger.read("scn_safe_current"))
        #print(f"\tSCN Modbus Slave Max Current enable: {alfen_eve_modbus_tcp.MODBUS_SLAVE_MAX_CURRENT_ENABLE_MAP[str(values['scn_modbus_slave_max_current_enable'])]}")

    # print(car_charger.connect())
    # time.sleep(1)
    # print(car_charger.connected())
    # print(car_charger)
    # values = {}
    # values['mode_3_state'] = False
    # while values['mode_3_state'] == False:
    #     print("Attempt")
    #     values = car_charger.read("mode_3_state")
    # print(values)
    # print(car_charger.read("modbus_slave_max_current"))
    #
    # car_charger.write("modbus_slave_max_current", 7.0)
    # time.sleep(1)
    # print(car_charger.read("modbus_slave_max_current"))

    #print(car_charger.read_all())
    #print(car_charger.registers["mode_3_state"])
    #print(car_charger.registers["modbus_slave_max_current"])
    # car_charger.disconnect()
