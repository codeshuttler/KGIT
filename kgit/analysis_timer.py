

import numpy as np
from collections import defaultdict
import time


class AnalysisTimer(object):
    def __init__(self) -> None:
        self.data = {}
        self.timer = {}
    
    def start_timer(self, timer_name: str):
        self.timer[timer_name] = time.time()
    
    def end_timer(self, timer_name: str):
        start_time = self.timer[timer_name]
        end_time = time.time()

        if timer_name not in self.data:
            self.data[timer_name] = []
        self.data[timer_name].append(end_time - start_time)
    
    def get_summary(self):
        summary = {}
        for name, time_list in self.data.items():
            summary[name] = {
                'max': np.max(time_list),
                'min': np.min(time_list),
                'mean': np.mean(time_list),
                'median': np.median(time_list),
                'sum': np.sum(time_list),
            }
        
        return summary