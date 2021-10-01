from audiometer import tone_generator
import numpy as np
import argparse
import time
import os
import csv
import random


def config():

    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument(
        "--device", type=int, default=None)
    parser.add_argument("--beginning-fam-level", type=float, default=40,
                        help="in dBHL")
    parser.add_argument("--attack", type=float, default=30)
    parser.add_argument("--release", type=float, default=40)
    parser.add_argument(
        "--tone-duration", type=float, default=2)
    parser.add_argument("--small-level-increment", type=float, default=5)
    parser.add_argument("--large-level-increment", type=float, default=10)
    parser.add_argument("--small-level-decrement", type=float, default=10)
    parser.add_argument("--large-level-decrement", type=float, default=20)
    parser.add_argument("--start-level-familiar", type=float, default=-40)
    parser.add_argument("--results-path", type=str,
                        default='audiometer/results/')
    parser.add_argument("--filename", default='result_{}'.format(time.strftime(
                        '%Y-%m-%d_%H-%M-%S')) + '.csv')

    # Random Calibration values
    # PC Sound Level: Maximum
    # Calibration values: [frequency, reference, correction]
    parser.add_argument("--cal125", default=[125, -81, 17])
    parser.add_argument("--cal250", default=[250, -92, 12])
    parser.add_argument("--cal500", default=[500, -80, -5])
    parser.add_argument("--cal750", default=[750, -85, -3])
    parser.add_argument("--cal1000", default=[1000, -84, -4])
    parser.add_argument("--cal1500", default=[1500, -82, -4])
    parser.add_argument("--cal2000", default=[2000, -90, 2])
    parser.add_argument("--cal3000", default=[3000, -94, 10])
    parser.add_argument("--cal4000", default=[4000, -91, 11])
    parser.add_argument("--cal6000", default=[6000, -70, -5])
    parser.add_argument("--cal8000", default=[8000, -76, 1])

    args = parser.parse_args()

    if not os.path.exists(args.results_path):
        os.makedirs(args.results_path)

    return args


class Controller:  

    def __init__(self):

        self.config = config()

        self.csvfile = open(os.path.join(self.config.results_path,  
                                         self.config.filename), 'w')
        self.writer = csv.writer(self.csvfile)
        self.writer.writerow(['Conduction', "Air Conduction", None])
        self.writer.writerow(['Masking', "Masking", None])
        self.writer.writerow(['Level/dB', 'Frequency/Hz', 'Earside'])

        self.cal_parameters = np.vstack((self.config.cal125,
                                        self.config.cal250,
                                        self.config.cal500,
                                        self.config.cal750,
                                        self.config.cal1000,
                                        self.config.cal1500,
                                        self.config.cal2000,
                                        self.config.cal3000,
                                        self.config.cal4000,
                                        self.config.cal6000,
                                        self.config.cal8000))

        self._audio = tone_generator.AudioStream(self.config.device,
                                                 self.config.attack,
                                                 self.config.release)
        
    
    def audibletone2(self, freq, current_level_dBHL, earside):
        if self.dBHL2dBFS(freq, current_level_dBHL) > 0:
            print("WARNING: Signal is distorted. Decrease the current "
                    "level!")
        self._audio.start(freq,
                            self.dBHL2dBFS(freq, current_level_dBHL),
                            earside)
            
        return current_level_dBHL
    
    def audibletone3(self, freq, current_level_dBHL, earside):
        if self.dBHL2dBFS(freq, current_level_dBHL) > 0:
            print("WARNING: Signal is distorted. Decrease the current "
                    "level!")
        self._audio.stop()    
        self._audio.start(freq,
                            self.dBHL2dBFS(freq, current_level_dBHL),
                            earside)
            
        
    def stopaudibletone(self):
        self._audio.stop()


    def save_results(self, level, freq, earside):
        row = [level, freq, earside]
        self.writer.writerow(row)

    def dBHL2dBFS(self, freq_value, dBHL):
        calibration = [(ref, corr) for freq, ref, corr in self.cal_parameters
                       if freq == freq_value]
        return calibration[0][0] + calibration[0][1] + dBHL

    def __enter__(self):
        return self

    def __exit__(self, *args):
        time.sleep(0.1)
        self._audio.close()
        self.csvfile.close()

