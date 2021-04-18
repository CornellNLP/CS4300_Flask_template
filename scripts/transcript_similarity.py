def readTranscript (filePath):
    file = open(filePath)
    fileContents = file.read()
    file.close()
    return fileContents

