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
    return fileContents

#transcript = readTranscript("/Users/siddhichordia/cs4300sp2020-rj356-dd492-sc2538-sv352-kal255-1/transcripts/Avatar: The Last Airbender/avatar_scripts_s1_e2.txt")

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
    print(result)
    return (result)
    
listTranscripts("/Users/siddhichordia/cs4300sp2020-rj356-dd492-sc2538-sv352-kal255-1/transcripts/American Crime Story")




