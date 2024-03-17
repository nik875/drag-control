import time
from .bmp388 import BMP388


bmp388 = BMP388()


def read_data():
    temperature,pressure,altitude = bmp388.get_temperature_and_pressure_and_altitude()
    return altitude / 100


def sample(num):
    return sum(read_data() for _ in range(num)) / num


def sample_time(duration):
    st = time.time()
    data = []
    while time.time() < st + duration:
        data.append(read_data())
    return sum(data) / len(data)



if __name__ == '__main__':
    print(sample_time(.1))
