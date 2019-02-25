import board
import digitalio
import time
from pni_libs.debug import *

import analogio
from board import *

class test_data_collection_adc:

    def __init__(self, pin):
        self.pin = pin
        self.adc = analogio.AnalogIn(self.pin)
        # self.reference_voltage = reference_voltage

    def get_adc_value(self):
        return self.adc.value

    def value_to_voltage(self):
        return self.get_adc_value()*3.3/65535

    # def get_ref_voltage(self):
    #     return self.reference_voltage

class test_data_collection_dig:
    def __init__(self, pin):
        self.pin = pin
        self.dig = digitalio.DigitalInOut(self.pin)
        self.dig.direction = digitalio.Direction.INPUT
        self.dig.pull = digitalio.Pull.DOWN

    def get_dig_value(self):
        return self.dig.value

if __name__ == "__main__":

    adc1 = test_data_collection_adc(board.A2)
    dig1 = test_data_collection_dig(board.D3)
    dig2 = test_data_collection_dig(board.D7)

    timeRead = []
    data = []
    baseline = []

    def average(list):
        return sum(list)/len(list)

    while True:
        # # ***** SLOW *****
        # if dig1.get_dig_value():
        #     print("At time," , time.monotonic(), ", my reading is," , adc1.value_to_voltage())
        # else:
        #     continue


        # ***** FAST *****

        if dig1.get_dig_value():
            # here you have another if statement that only takes readings when the readings are above the baseline and then stops when they fall back to within a 0.1V range of the baseline
            if (adc1.value_to_voltage() > (average(baseline))):
                timeRead.append(time.monotonic())
                data.append(adc1.value_to_voltage())
                # ii = 0
                # while (ii<0xFF):
                #     ii += 1
            else:
                continue

        else:
            # here you toggle the second switch and take 100 measurements, average them, and that becomes your baseline
            if dig2.get_dig_value():
                while (len(baseline) < 100):
                    baseline.append(adc1.value_to_voltage())
            else:
                if (len(timeRead) > 0):
                    for i in range(1, len(timeRead)):
                        print(("At time, %12.5f, my reading is, %f") % (timeRead[i], data[i]))
                        time.sleep(0.01)
                    print("== DONE ==")
                    print ("baseline average is:", average(baseline))
                        # print("At time," , timeRead[i], ", my reading is," , data[i])
                    timeRead = []
                    data = []
                    baseline = []
                else:
                    continue
