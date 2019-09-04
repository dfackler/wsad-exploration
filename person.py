# person.py
import pandas as pd
import os
import ast
import math
from matplotlib import pylab
import numpy as np

base_dir = '/Users/david/Desktop/WESAD'


class Person(object):
    """ Class for holding data on a person in the study
    Assumes all files exist in correct format for subject num """

    def __init__(self, base_dir, num):
        self.base_dir = base_dir
        self.num = num
        # read in the readme and parse to get demographics
        self.timing = self._getTiming()
        self.panas = self._addEvent(self._getPANAS())
        self.stai = self._addEvent(self._getSTAI())
        self.sam = self._addEvent(self._getSAM())
        self.sssq = self._getSSSQ()
        self.respi = self._convertRespi(self._getRawRespi())

    def _getTiming(self):
        """ Assumes base_dir is string containing directory with all subject
        files and num is an integer referring to a valid subject number
        contained within the study.
        Will gather the order of studies and timings in minutes. """
        # TODO: strip leading hash mark
        timing = pd.read_csv(
            os.path.join(self.base_dir, ('S'+str(self.num)),
                         ('S'+str(self.num)+'_quest.csv')),
            sep=";", skiprows=1, nrows=2)
        # from README: Please ignore the elements “bRead”, “fRead”, and “sRead”
        timing.drop(['bRead', 'fRead', 'sRead'],
                    axis='columns', errors='ignore', inplace=True)
        timing.drop(list(timing.filter(regex='Unnamed')),
                    axis=1, inplace=True)
        return timing

    def _getPANAS(self):
        """ Assumes base_dir is string containing directory with all subject
        files and num is an integer referring to a valid subject number
        contained within the study.
        Will gather the PANAS survey data.
        1 = Not at all, 2 = A little bit, 3 = Somewhat, 4 = Very much,
        5 = Extremely
        """
        panas = pd.read_csv(
            os.path.join(self.base_dir, ('S'+str(self.num)),
                         ('S'+str(self.num)+'_quest.csv')),
            sep=";", skiprows=5, nrows=5, header=None)
        panas = panas.rename(columns={
            0: "test", 1: "active", 2: "distressed", 3: "interested",
            4: "inspired", 5: "annoyed", 6: "strong",
            7: "guilty", 8: "scared", 9: "hostile", 10: "excited",
            11: "proud", 12: "irritable", 13: "enthusiastic",
            14: "ashamed", 15: "alert", 16: "nervous",
            17: "determined", 18: "attentive", 19: "determined",
            20: "attentive", 21: "jittery", 22: "afraid",
            23: "stressed", 24: "frustrated", 25: "happy", 26: "sad"}
        )
        return panas

    def _getSTAI(self):
        """ Assumes base_dir is string containing directory with all subject
        files and num is an integer referring to a valid subject number
        contained within the study.
        Will gather the STAI survey data.
        1 = Not at all, 2 = Somewhat, 3 = Moderately so, 4 = Very much so
        """
        stai = pd.read_csv(
            os.path.join(self.base_dir, ('S'+str(self.num)),
                         ('S'+str(self.num)+'_quest.csv')),
            sep=";", skiprows=11, nrows=5, header=None)
        stai = stai.rename(columns={
            0: "test", 1: "atEase", 2: "nervous", 3: "jittery",
            4: "relaxed", 5: "worried", 6: "pleasant"}
        )
        # drop unused columns
        stai.drop(range(7, 27), axis=1, inplace=True)
        return stai

    def _getSAM(self):
        """ Assumes base_dir is string containing directory with all subject
        files and num is an integer referring to a valid subject number
        contained within the study.
        Will gather the SAM survey data.
        Scale 1-9
        """
        sam = pd.read_csv(
            os.path.join(self.base_dir, ('S'+str(self.num)),
                         ('S'+str(self.num)+'_quest.csv')),
            sep=";", skiprows=17, nrows=5, header=None)
        sam = sam.rename(columns={
            0: "test", 1: "valence", 2: "arousal"}
        )
        # drop unused columns
        sam.drop(range(3, 27), axis=1, inplace=True)
        return sam

    def _getSSSQ(self):
        """ Assumes base_dir is string containing directory with all subject
        files and num is an integer referring to a valid subject number
        contained within the study.
        Will gather the SSSQ survey data.
        1 = Not at all, 2 = A little bit, 3 = Somewhat, 4 = Very much,
        5 = Extremely
        - I was committed to attaining my performance goals
        - I wanted to succeed on the task
        - I was motivated to do the task
        - I reflected about myself
        - I was worried about what other people think of me
        - I felt concerned about the impression I was making
        """

        sssq = pd.read_csv(
            os.path.join(self.base_dir, ('S'+str(self.num)),
                         ('S'+str(self.num)+'_quest.csv')),
            sep=";", skiprows=23, nrows=1, header=None)
        sssq = sssq.rename(columns={
            0: "test", 1: "attaining", 2: "succeed", 3: "motivated",
            4: "reflected", 5: "otherThink", 6: "impression"}
        )
        # drop unused columns
        sssq.drop(range(7, 27), axis=1, inplace=True)
        return sssq

    def _addEvent(self, metric_df):
        """ Will combine the descriptors from timing to metric dataframe """
        metric_df.insert(1, "event", list(self.timing.columns)[1:])
        return metric_df

    def _getRawRespi(self):
        """ Will read in the raw respiban data.
        Caution: This data contains up to 5 million rows and 10 columns. """
        raw_respi = pd.read_csv(
            os.path.join(self.base_dir, ('S'+str(self.num)),
                         ('S'+str(self.num)+'_respiban.txt')),
            sep="\t", skiprows=3, header=None)
        # drop unused columns
        raw_respi.drop(1, axis=1, inplace=True)  # from README
        raw_respi.dropna(axis='columns', inplace=True)  # trailing tab

        # parse second line of file containing column labels
        with open(os.path.join(self.base_dir, ('S'+str(self.num)),
                               ('S'+str(self.num)+'_respiban.txt'))) as fp:
            for i, line in enumerate(fp):
                if i == 1:
                    header = line
        sensor_start = header.find('sensor')
        col_start = header.find('[', sensor_start)
        col_end = header.find(']', 26) + 1
        cols = ast.literal_eval(header[col_start:col_end])

        # handle accelerometer columns
        xyz_cols_changed = 0
        while xyz_cols_changed < 3:
            # assumes accelerometer columns in order of X, Y, Z coordinates
            acc_ind = cols.index('XYZ')
            xyz_col_names = {
                0: 'ACC_X',
                1: 'ACC_Y',
                2: 'ACC_Z'
            }
            cols[acc_ind] = xyz_col_names[xyz_cols_changed]
            xyz_cols_changed += 1
        cols.insert(0, 'nSeq')
        raw_respi.columns = cols

        return raw_respi

    def _convertRespi(self, respi):
        """ this takes a raw respiban data frame and converts the metrics
        using the calculations described in the README """

        # clean up rows with zero values for temp
        # TODO: remove rows with any zero reading
        respi = respi.loc[respi['TEMP'] != 0].copy()

        vcc = 3
        chan_bit = 2 ** 16
        cmin = 28000
        cmax = 38000

        respi['ECG'] = respi['ECG'].apply(lambda x: ((x/chan_bit-0.5)*vcc))
        respi['EDA'] = respi['EDA'].apply(lambda x: (((x/chan_bit)*vcc)/0.12))
        respi['EMG'] = respi['EMG'].apply(lambda x: ((x/chan_bit-0.5)*vcc))
        # temp calculation more involved
        # NOTE: Why do they subtract this 1.0? In the reference doc they do not
        respi['vout'] = respi['TEMP'].apply(lambda x: (x*vcc)/(chan_bit-1.0))
        respi['rntc'] = respi['vout'].apply(lambda x: ((10 ** 4)*x)/(vcc-x))
        respi['TEMP'] = respi['rntc'].apply(
            lambda x: - 273.15 + 1./(1.12764514*(10 ** (-3)) +
                                     2.34282709*(10 ** (-4))*math.log(x) +
                                     8.77303013*(10 ** (-8))*(math.log(x) ** 3)
                                     ))
        respi.drop('vout', axis='columns', inplace=True)
        respi.drop('rntc', axis='columns', inplace=True)
        respi['ACC_X'] = respi['ACC_X'].apply(
            lambda x: (x-cmin)/(cmax-cmin)*2-1)
        respi['ACC_Y'] = respi['ACC_Y'].apply(
            lambda x: (x-cmin)/(cmax-cmin)*2-1)
        respi['ACC_Z'] = respi['ACC_Z'].apply(
            lambda x: (x-cmin)/(cmax-cmin)*2-1)
        respi['ACC'] = respi[['ACC_X', 'ACC_Y', 'ACC_Z']].apply(
            lambda x: [x], axis=1)
        respi = respi.drop(['ACC_X', 'ACC_Y', 'ACC_Z'], axis=1)
        respi['RESPIRATION'] = respi['RESPIRATION'].apply(
            lambda x: (x/chan_bit-0.5)*100)

        # Add time (at 770 Hz each row is 1/770 of a second)
        # NOTE: Person2 has less minutes here than max of timings data frame
        respi['seconds'] = respi['nSeq'].apply(lambda x: x*(1/770))
        respi['minutes'] = respi['seconds'].apply(lambda x: x/60)

        return respi

    def bucketRespi(self, num_buckets, metric):
        """ this will bucket rows and retrieve average for each metric
        within the buckets """
        respi_bucket['buckets'] = pd.cut(
            respi[metric], num_buckets, labels=False)
        respi_avgs = []
        for i in range(num_buckets):
            respi_avgs.append(respi_bucket[respi_bucket.buckets == i].mean(0))
        return respi_avgs

    def plotRespiMetric(self, metric, num_buckets):
        """ this will plot a single metric with a specified sample_perc
        to avoid plotting all data points.
        Assumes valid metric label """
        respi_avgs = self.bucketRespi(num_buckets)
        graph_data = []
        for i in range(len(respi_avgs)):
            graph_data.append(respi_avgs[i][metric])
        pylab.plot(graph_data, 'b-')
        return None

    def addFilter(self, metric, size):
        """ this will add a moving-average filter for a specified
        valid metric label in respi for the given window size
        (actual filter size is size*2+1)
        """
        # initialize filter with zeros
        n = len(self.respi[metric])
        filtsig = np.zeros(n)

        for i in range(size+1, n-size-1):
            filtsig[i] = np.mean(self.respi[metric][i-size:i+size])

        return filtsig

    def getTiming(self):
        return self.timing

    def getPANAS(self):
        return self.panas

    def getSTAI(self):
        return self.stai

    def getSAM(self):
        return self.sam

    def getSSSQ(self):
        return self.sssq

    def getRespi(self):
        return self.respi
