import re
import os
import numpy as np


def readTranscript(filePath):
    """
    given a string filePath, return the relevant part of the transcript file
    """
    file = open(filePath, encoding='utf-8')
    fileContents = file.read()
    file.close()
    # print(fileContents)

    start = fileContents.index('Print')
    end = fileContents.rfind("Transcripts")
    return fileContents[start+5: end]

# readTranscript('../transcripts/Avatar The Last Airbender/avatar_scripts_s1_e1.txt')


# transcript = readTranscript('../transcripts/Avatar The Last Airbender/avatar_scripts_s1_e1.txt')


def tokenize(transcript):
    """
    given a string transcript, return a list of tokens
    """
    text = transcript.lower()
    regex = r'[a-z]+'
    # print("words:" , re.findall(regex,text))
    return re.findall(regex, text)

# tokenize(transcript)


def listTranscripts(showFolder):
    """
    given a string showFolder (path to show folder), return a list of the transcript files for that show
    """
    result = []
    for sub, dirs, transcripts in os.walk(showFolder):
        for file in transcripts:
            filepath = sub + os.sep + file
            result.append(filepath)
    # print(result)
    return (result)


# listTranscripts("../transcripts/American Crime Story")


def showTokens(showFolder):
    """
    given a string showFolder (path to show folder), return a dict of form {token: count}
    """
    episodes = listTranscripts(showFolder)
    result = {}
    episodeCount = {}
    for episode in episodes:
        # print(episode)
        fileContents = readTranscript(episode)

        tokenList = tokenize(fileContents)
        tokenSet = set(tokenList)
        for token in tokenSet:
            if (token in episodeCount.keys()):
                episodeCount[token] += 1
            else:
                episodeCount[token] = 1
        for token in tokenList:
            if(token in result.keys()):
                result[token] += 1
            else:
                result[token] = 1
    sortedResult = dict(
        sorted(result.items(), key=lambda item: item[1], reverse=True))
    sortedEpisodes = dict(
        sorted(episodeCount.items(), key=lambda item: item[1], reverse=True))
    # print (sortedEpisodes)
    return sortedResult, sortedEpisodes


# showTokens("../transcripts/American Crime Story")


def allShowTokens(transcriptsFolder):
    """
    given a string path to the transcriptsFolder, return a dictionary of form {show:{token:count}}
    """

    result = {}
    for sub, dirs, shows in os.walk(transcriptsFolder):
        for file in shows:
            filepath = sub + os.sep
            folder = filepath[:-1]
            tokenDict, episodeDict = showTokens(folder)

            name = folder[(folder.rfind("\\")) + 1:]
            # print(name)
            result[name] = tokenDict
    # print(result)
    return result


allShowToks = allShowTokens("transcripts")
# print(allShowToks.keys())


def wordsToAnalyze(showFolder):
    """
    given string path to showFolder, return a dict of the form {token:count} of words that appear in more than one episode of the show
    """
    # print(showFolder)
    result = {}
    tokenDict, episodeDict = showTokens(showFolder)
    name = showFolder[(showFolder.rfind("/")) + 1:]
    allToks = allShowToks[name]

    for token in episodeDict.keys():
        if episodeDict[token] > 1:
            count = allToks[token]
            result[token] = count
    sortedResult = dict(
        sorted(result.items(), key=lambda item: item[1], reverse=True))
    # print(sortedResult)
    return sortedResult


#wordsToAnalyze("../transcripts/American Crime Story")


def allWordsToAnalyze(transcriptsFolder):
    """
    given string path to transcriptsFolder, return dict of form {show: {token: count}} contain wordsToAnalyze for each show
    """
    ans = {}

    for sub, dirs, shows in os.walk(transcriptsFolder):
        for file in shows:
            filepath = sub
            folder = filepath.replace("\\", "/")
            x = wordsToAnalyze(folder)
            name = folder[(folder.rfind("/")) + 1:]
            ans[name] = x

    return ans


allWordsToAnalyze = allWordsToAnalyze("transcripts")
shows = list(allWordsToAnalyze.keys())
# print(shows)


def jaccardSimMat(wordsToAnalyze=allWordsToAnalyze):
    """
    given allWordsToAnalyze, return an np array of size nShows x nShows with the jaccard similarity between shows
    """
    nShows = len(wordsToAnalyze)
    result = np.zeros((nShows, nShows))
    for i in range(nShows):
        for j in range(nShows):
            and_count = 0
            or_count = 0

            showA = shows[i]
            showB = shows[j]

            lenA = len(wordsToAnalyze[showA].keys())
            lenB = len(wordsToAnalyze[showB].keys())
            for x in range(min(lenA, lenB)):
                word = list(wordsToAnalyze[showA].keys())[x]
                if(word in wordsToAnalyze[showA] or word in wordsToAnalyze[showB]):
                    or_count += 1
                    if (word in wordsToAnalyze[showA] and word in wordsToAnalyze[showB]):
                        and_count += 1
                result[i, j] = and_count/or_count
    # print(result)
    return result


jaccSimMat = jaccardSimMat()

<<<<<<< HEAD

def jaccardRanking(show, N, simMat=jaccSimMat):
=======
def jaccardRanking (show, N = 3 , simMat = jaccSimMat) :
>>>>>>> 7f084332ebf994bd171c43fe4187846becf90e02
    """
    given an input string show name, return a ranked list of the N most similar shows using the jaccSimMat (using N = 3 for demo)
    """
    showInd = shows.index(show)
    scores = jaccSimMat[showInd]

    result = sorted(range(len(scores)), key=lambda substr: scores[substr])[
        (-N-1): -1]
    result.reverse()

    ranking = []
    for x in result:
        name = shows[x]
        ranking.append(name)

    # print(ranking)
    return ranking

<<<<<<< HEAD
# jaccardRanking ("Friends", 3)
=======
#jaccardRanking ("Friends")

    
>>>>>>> 7f084332ebf994bd171c43fe4187846becf90e02
