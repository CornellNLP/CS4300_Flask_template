import re
import os

def readTranscript (filePath):
    """
    given a string filePath, return the relevant part of the transcript file
    """
    file = open(filePath)
    fileContents = file.read()
    file.close()
    #print(fileContents)

    start = fileContents.index('Print')
    end = fileContents.rfind("Transcripts")
    return fileContents[start+5 : end]

#readTranscript("/Users/siddhichordia/cs4300sp2020-rj356-dd492-sc2538-sv352-kal255-1/transcripts/Avatar: The Last Airbender/avatar_scripts_s1_e2.txt")

transcript = readTranscript("/Users/siddhichordia/cs4300sp2020-rj356-dd492-sc2538-sv352-kal255-1/transcripts/Avatar: The Last Airbender/avatar_scripts_s1_e2.txt")
#print(transcript)
def tokenize (transcript):
    """
    given a string transcript, return a list of tokens
    """
    text = transcript.lower()
    regex = r'[a-z]+'
    #print("words:" , re.findall(regex,text))
    return re.findall(regex,text)

#tokenize(transcript)

def listTranscripts(showFolder):
    """
    given a string showFolder (path to show folder), return a list of the transcript files for that show
    """
    result = []
    for sub, dirs, transcripts in os.walk(showFolder):
        for file in transcripts:
            filepath = sub + os.sep + file
            result.append(filepath)
    #print(result)
    return (result)
    
#listTranscripts("/Users/siddhichordia/cs4300sp2020-rj356-dd492-sc2538-sv352-kal255-1/transcripts/American Crime Story")

def showTokens(showFolder):
    """
    given a string showFolder (path to show folder), return a dict of form {token: count}
    """
    episodes = listTranscripts(showFolder)
    result = {}
    episodeCount = {}
    for episode in episodes:
        #print(episode)
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
    sortedResult = dict(sorted(result.items(), key=lambda item: item[1], reverse = True))
    sortedEpisodes = dict(sorted(episodeCount.items(), key=lambda item: item[1], reverse = True))
    #print (sortedEpisodes)
    return sortedResult, sortedEpisodes

#showTokens("/Users/siddhichordia/cs4300sp2020-rj356-dd492-sc2538-sv352-kal255-1/transcripts/American Crime Story")

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
            
            name = folder[(folder.rfind("/")) + 1 :]
            #print(name)
            result[name] = tokenDict
    #print(result)
    return result

allShowToks = allShowTokens("/Users/siddhichordia/cs4300sp2020-rj356-dd492-sc2538-sv352-kal255-1/transcripts")

def wordsToAnalyze(showFolder):
    """
    given string path to showFolder, return a dict of the form {token:count} of words that appear in more than one episode of the show
    """
    result = {}
    tokenDict, episodeDict = showTokens(showFolder)
    name = showFolder[(showFolder.rfind("/")) + 1 :]
    allToks = allShowToks[name]

    for token in episodeDict.keys():
        if episodeDict[token] > 1 :
            count = allToks[token]
            result[token] = count
    sortedResult = dict(sorted(result.items(), key=lambda item: item[1], reverse = True))
    #print(sortedResult)
    return sortedResult

#wordsToAnalyze("/Users/siddhichordia/cs4300sp2020-rj356-dd492-sc2538-sv352-kal255-1/transcripts/American Crime Story")


def allWordsToAnalyze(transcriptsFolder):
    """
    given string path to transcriptsFolder, return dict of form {show: {token: count}} contain wordsToAnalyze for each show
    """
    ans = {}

    for sub, dirs, shows in os.walk(transcriptsFolder):
        for file in shows:
            filepath = sub + os.sep 
            folder = filepath[:-1]
            x = wordsToAnalyze(folder)#
            name = folder[(folder.rfind("/")) + 1 :]
            ans[name] = x

    return ans     


allWords = allWordsToAnalyze("/Users/siddhichordia/cs4300sp2020-rj356-dd492-sc2538-sv352-kal255-1/transcripts")
#print(allWords)


