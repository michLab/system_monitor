import psutil
import time
import collections

class CPU:
    def __init__(self, number):
        self.number = number
        self.time_stamp_us = 0
        self.freq_curr = 0
        self.freq_min = 0
        self.freq_max = 0
        self.temp = 0
        self.usage = 0
    def show(self):
        print "number=",self.number,"freq_curr=",self.freq_curr,\
                "freq_min=",self.freq_min,"freq_max=",self.freq_max,\
                "temp=",self.temp,"usage=",self.usage


class SystemMonitor:
    def __init__(self):
        self.cpu = []
        self.initialize_cpu_instances()
        self.cpu_freq = []
        self.cpu_usage = []
        self.current_time_us = 0
        self.sensor_temperatures = []

    def initialize_cpu_instances(self):
        self.cpu_count = psutil.cpu_count()
        for i in range(self.cpu_count):
            self.cpu.append(CPU(i))

    def get_cpu_freq(self):
        self.cpu_freq = psutil.cpu_freq(percpu=True)
        for i in range(self.cpu_count):
            self.cpu[i].freq_curr = self.cpu_freq[i].current
            self.cpu[i].freq_min = self.cpu_freq[i].min
            self.cpu[i].freq_max = self.cpu_freq[i].max

    def get_time_us(self):
        current_time_s = time.time()
        self.current_time_us = int(round(current_time_s * 1000000))
        for i in range(self.cpu_count):
            self.cpu[i].time_stamp_us = self.current_time_us

    def get_cpu_usage(self):
        self.cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
        for i in range(self.cpu_count):
            self.cpu[i].usage = self.cpu_usage[i]

    def get_sensor_temperatures(self):
        self.sensor_temperatures = psutil.sensors_temperatures()
        for i in range(self.cpu_count):
            self.cpu[i].temp = self.sensor_temperatures[i].current

    def get_current_state(self):
        self.get_time_us()
        self.get_cpu_freq()
        self.get_cpu_usage();
        self.get_sensor_temperatures()
        
    def print_current_state(self):
        for i in range(self.cpu_count):
            self.cpu[i].show()

sm = SystemMonitor()

sm.get_current_state()
sm.print_current_state()
