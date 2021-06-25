from smbus import SMBus
import time

# I2C simplified: 0x5E
EE895ADDRESS = 0x5E
I2CREGISTER = 0x00


def main():
    '''
    Main program function
    '''
    i2cbus = SMBus(1)
    # delay recommended according to this stackoverflow post
    # https://stackoverflow.com/questions/52735862/getting-ioerror-errno-121-remote-i-o-error-with-smbus-on-python-raspberry-w
    time.sleep(1)
    while True:
        try:
            read_data = i2cbus.read_i2c_block_data(EE895ADDRESS, I2CREGISTER, 8)
            # read_data contains ints, which we need to convert to bytes and merge
            # see datasheet
            co2 = read_data[0].to_bytes(1, 'big') + read_data[1].to_bytes(1, 'big')
            temperature = read_data[2].to_bytes(1, 'big') + read_data[3].to_bytes(1, 'big')
            # reserved value - useful to check that the sensor is reading out correctly
            # this should be 0x8000
            resvd = read_data[4].to_bytes(1, 'big') + read_data[5].to_bytes(1, 'big')
            pressure = read_data[6].to_bytes(1, 'big') + read_data[7].to_bytes(1, 'big')

            print("CO2: ", end='')
            print(int.from_bytes(co2, "big"), end='')
            print(" ppm [0x", end='')
            print(co2.hex(), end='')
            print("] | Temperature: ", end='')
            print(int.from_bytes(temperature, "big") / 100, end='')
            print("°C [0x", end='')
            print(temperature.hex(), end='')
            print("] | Reserved: ", end='')
            print(int.from_bytes(resvd, "big"), end='')
            print(" [0x", end='')
            print(resvd.hex(), end='')
            print("] | Pressure: ", end='')
            print(int.from_bytes(pressure, "big") / 10, end='')
            print("mbar [0x", end='')
            print(pressure.hex(), end='')
            print("]")
        except Exception:
            print("Could not read from the sensor. Is it attached?")

        # note the default measurement interval of the sensor is 15 sec
        time.sleep(1)


if __name__ == "__main__":
    main()
