def readTranscript (filePath):
    file = open(filePath)
    fileContents = file.read()
    file.close()
    print(fileContents)
    return fileContents

readTranscript("/Users/siddhichordia/cs4300sp2020-rj356-dd492-sc2538-sv352-kal255-1/transcripts/Avatar: The Last Airbender/avatar_scripts_s1_e2.txt")