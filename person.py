# person.py
import pandas as pd
import os


def getTiming(base_dir, num):
    """ Assumes base_dir is string containing directory with all subject files
    and num is an integer referring to a valid subject number contained within 
    the study.
    Will gather the order of studies and timings in minutes. """
    timing = pd.read_csv(
        os.path.join(base_dir, ('S'+str(num)), ('S'+str(num)+'_quest.csv')),
        sep=";", skiprows=1, nrows=2)
    # from README: Please ignore the elements “bRead”, “fRead”, and “sRead”
    timing.drop(['bRead', 'fRead', 'sRead'],
                axis='columns', errors='ignore', inplace=True)
    timing.drop(list(timing.filter(regex='Unnamed')),
                axis=1, inplace=True)
    return timing


def getPANAS(base_dir, num):
    """ Assumes base_dir is string containing directory with all subject files
    and num is an integer referring to a valid subject number contained within
    the study.
    Will gather the PANAS survey data. 
    1 = Not at all, 2 = A little bit, 3 = Somewhat, 4 = Very much, 
    5 = Extremely
    """
    panas = pd.read_csv(
        os.path.join(base_dir, ('S'+str(num)), ('S'+str(num)+'_quest.csv')),
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


def getSTAI(base_dir, num):
    """ Assumes base_dir is string containing directory with all subject files
    and num is an integer referring to a valid subject number contained within
    the study.
    Will gather the STAI survey data. 
    1 = Not at all, 2 = Somewhat, 3 = Moderately so, 4 = Very much so
    """
    stai = pd.read_csv(
        os.path.join(base_dir, ('S'+str(num)), ('S'+str(num)+'_quest.csv')),
        sep=";", skiprows=11, nrows=5, header=None)
    stai = stai.rename(columns={
        0: "test", 1: "atEase", 2: "nervous", 3: "jittery",
        4: "relaxed", 5: "worried", 6: "pleasant"}
    )
    # drop unused columns
    stai.drop(range(7, 27), axis=1, inplace=True)
    return stai


def getSAM(base_dir, num):
    """ Assumes base_dir is string containing directory with all subject files
    and num is an integer referring to a valid subject number contained within
    the study.
    Will gather the SAM survey data. 
    Scale 1-9
    """
    sam = pd.read_csv(
        os.path.join(base_dir, ('S'+str(num)), ('S'+str(num)+'_quest.csv')),
        sep=";", skiprows=17, nrows=5, header=None)
    sam = sam.rename(columns={
        0: "test", 1: "valence", 2: "arousal"}
    )
    # drop unused columns
    sam.drop(range(3, 27), axis=1, inplace=True)
    return sam


def getSSSQ(base_dir, num):
    """ Assumes base_dir is string containing directory with all subject files
    and num is an integer referring to a valid subject number contained within
    the study.
    Will gather the SSSQ survey data. 
    1 = Not at all, 2 = A little bit, 3 = Somewhat, 4 = Very much, 5 = Extremely
    - I was committed to attaining my performance goals
    - I wanted to succeed on the task
    - I was motivated to do the task
    - I reflected about myself
    - I was worried about what other people think of me
    - I felt concerned about the impression I was making
    """

    sssq = pd.read_csv(
        os.path.join(base_dir, ('S'+str(num)), ('S'+str(num)+'_quest.csv')),
        sep=";", skiprows=23, nrows=1, header=None)
    sssq = sssq.rename(columns={
        0: "test", 1: "attaining", 2: "succeed", 3: "motivated",
        4: "reflected", 5: "otherThink", 6: "impression"}
    )
    # drop unused columns
    sssq.drop(range(7, 27), axis=1, inplace=True)
    return sssq


class Person(object):
    """ Class for holding data on a person in the study
    Assumes all files exist in correct format for subject num """

    def __init__(self, base_dir, num):
        self.num = num
        # read in the readme and parse to get demographics
        self.timing = getTiming(base_dir, num)
        self.panas = getPANAS(base_dir, num)
        self.stai = getSTAI(base_dir, num)
        self.sam = getSAM(base_dir, num)
        self.sssq = getSSSQ(base_dir, num)
