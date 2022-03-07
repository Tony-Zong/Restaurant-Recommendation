import pickle
import pickle5 as p
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from datetime import date , timedelta


# start date and end date are None by default. if this is the case return dataviz
# for all dates in date range

def date_range(start_date , end_date):
    '''
    '''
    delta = end_date - start_date  # as timedelta
    days = [start_date + timedelta(days=i) for i in range(delta.days + 1)]
    for day in days:
        print(day)
    #return days