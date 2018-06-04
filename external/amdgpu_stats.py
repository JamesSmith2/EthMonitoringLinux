#!/usr/bin/python

import re

def read_watts(num):

    gpu_watts = []

    for i in range(num):
    
        file = '/sys/kernel/debug/dri/%s/amdgpu_pm_info' % str(i)

        with open(file, 'r') as data_file:
            data=data_file.read()
        
        try:
            match_watts = re.search( r'(.*) W \(average GPU\)', data).group(1)
            gpu_watts.append(match_watts.strip())
        
        except:
            gpu_watts.append('0')

    return gpu_watts