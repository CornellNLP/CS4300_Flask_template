import re


def readTranscript (filePath):
    """
    given a file path, return the relevant part of the transcript file
    """
    file = open(filePath)
    fileContents = file.read()
    file.close()
    #print(fileContents)
    return fileContents

transcript = readTranscript("/Users/siddhichordia/cs4300sp2020-rj356-dd492-sc2538-sv352-kal255-1/transcripts/Avatar: The Last Airbender/avatar_scripts_s1_e2.txt")

def tokenize (transcript):
    text = transcript.lower()
    regex = r'[a-z]+'
    #print("words:" , re.findall(regex,text))
    return re.findall(regex,text)

tokenize(transcript)
