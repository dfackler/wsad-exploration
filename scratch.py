import pickle
import pandas as pd
# handling the raw data pickle files
""" This file is a dictionary, with the following keys:
- ‘subject’: SX, the subject ID
- ‘signal’: includes all the raw data, in two fields:
- - ‘chest’: RespiBAN data (all the modalities: ACC, ECG, EDA, EMG, RESP, TEMP)
- - ‘wrist’:EmpaticaE4data(allthemodalities:ACC,BVP,EDA,TEMP)
- ‘label’: ID of the respective study protocol condition, sampled at 700 Hz.
The following IDs
are provided: 0 = not defined / transient, 1 = baseline, 2 = stress,
3 = amusement, 4 = meditation,
5/6/7 = should be ignored in this dataset
"""

with open('/Users/david/Desktop/WESAD/S2/S2.pkl', 'rb') as f:
    # use latin1 to handle this python2 pickle object in python3
    data = pickle.load(f, encoding='latin1')
print(data)


# get the order and times of self-reporting
questHead = pd.read_csv(
    '/Users/david/Desktop/WESAD/S2/S2_quest.csv', sep=";", skiprows=1, nrows=2)
# from README: Please ignore the elements “bRead”, “fRead”, and “sRead”
questHead.drop(['bRead', 'fRead', 'sRead'],
               axis='columns', errors='ignore', inplace=True)
questHead.drop(list(questHead.filter(regex='Unnamed')), axis=1, inplace=True)

# get the PANAS data
# panas questionnaire items
# 1 = Not at all, 2 = A little bit, 3 = Somewhat, 4 = Very much, 5 = Extremely
panas = pd.read_csv(
    '/Users/david/Desktop/WESAD/S2/S2_quest.csv', sep=";", skiprows=5, nrows=5,
    header=None)
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

# get the STAI data
# 1 = Not at all, 2 = Somewhat, 3 = Moderately so, 4 = Very much so
stai = pd.read_csv(
    '/Users/david/Desktop/WESAD/S2/S2_quest.csv', sep=";", skiprows=11,
    nrows=5, header=None)
stai = stai.rename(columns={
    0: "test", 1: "atEase", 2: "nervous", 3: "jittery",
    4: "relaxed", 5: "worried", 6: "pleasant"}
)
# drop unused columns
stai.drop(range(7, 27), axis=1, inplace=True)

# get the SAM data
# scale 1-9
sam = pd.read_csv(
    '/Users/david/Desktop/WESAD/S2/S2_quest.csv', sep=";", skiprows=17,
    nrows=5, header=None)
sam = sam.rename(columns={
    0: "test", 1: "valence", 2: "arousal"}
)
# drop unused columns
sam.drop(range(3, 27), axis=1, inplace=True)

# get the SSSQ data
# 1 = Not at all, 2 = A little bit, 3 = Somewhat, 4 = Very much, 5 = Extremely
# - I was committed to attaining my performance goals
# - I wanted to succeed on the task
# - I was motivated to do the task
# - I reflected about myself
# - I was worried about what other people think of me
# - I felt concerned about the impression I was making
sssq = pd.read_csv(
    '/Users/david/Desktop/WESAD/S2/S2_quest.csv', sep=";", skiprows=23,
    nrows=1, header=None)
sssq = sssq.rename(columns={
    0: "test", 1: "attaining", 2: "succeed", 3: "motivated",
    4: "reflected", 5: "otherThink", 6: "impression"}
)
# drop unused columns
sssq.drop(range(7, 27), axis=1, inplace=True)
