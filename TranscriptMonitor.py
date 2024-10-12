import json
import os
import re

SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def main():
    transcriptContents = GetTranscriptFolderContents()
    if transcriptContents:
        blacklistedTerms = GetBlacklistedTerms()
        errorMessages = ParseTranscripts(transcriptContents, blacklistedTerms)
        PrintResults(errorMessages)

def GetTranscriptFolderContents():
    transcriptContents = {}
    transcriptFolderName = "Transcripts"
    transcriptsDirectory = os.path.join(SCRIPT_DIRECTORY, transcriptFolderName)
    if not os.path.exists(transcriptsDirectory):
        print(f"The {transcriptFolderName} folder does not exist. Aborting Process.")
    elif not os.listdir(transcriptsDirectory):
        print(f"The {transcriptFolderName} folder does not contain any files. Aborting Process.")
    else:
        for item in os.listdir(transcriptsDirectory):
            if not os.path.isfile(os.path.join(transcriptsDirectory, item)):
                print(f"The item \"{item}\" in \"{transcriptsDirectory}\" is not a file and cannot be processed")
            elif not item.endswith(".txt"):
                print(f"The file \"{item}\" is not of type .txt and cannot be processed.")
            else:
                textFileContents = {}
                textFileName = os.path.basename(item)
                textFilepath = os.path.join(transcriptsDirectory, item)
                with open(textFilepath) as file:
                    # timestamp starts at -1 incase the file does not start with a timestamp
                    timestamp = "-1"
                    timestampText = ""
                    for line in file:
                        line = line.strip()
                        if line == "":
                            continue
                        elif CheckIfLineIsTimestamp(line):
                            textFileContents[timestamp] = timestampText
                            timestampText = ""
                            timestamp = line
                        else:
                            timestampText += line + " "

                    # Grabs final timestamp/text pair
                    if timestamp != "":
                        textFileContents[timestamp] = timestampText
                        
                transcriptContents[textFileName] = textFileContents

    return transcriptContents

def CheckIfLineIsTimestamp(line):
    return bool(re.fullmatch(r'[0-9:]*', line))

def GetBlacklistedTerms():
    blacklistedTerms = []

    blacklistedTermsDirectory = os.path.join(SCRIPT_DIRECTORY, "BlacklistedTerms.json")
    with open(blacklistedTermsDirectory, 'r') as file:
        blacklistedTerms = json.load(file)

    return blacklistedTerms

def ParseTranscripts(transcriptContents, blacklistedTerms):
    errorMessages = []
    for file in transcriptContents:
        for timeStamp in transcriptContents[file]:
            foundBlacklistedTerms = []
            for blacklistedTerm in blacklistedTerms:
                if blacklistedTerm in transcriptContents[file][timeStamp]:
                    foundBlacklistedTerms = AddBlacklistedTermToList(blacklistedTerm, foundBlacklistedTerms)
                    
            if len(foundBlacklistedTerms) > 0:
                errorMessages.append(f"The blacklisted term(s) {foundBlacklistedTerms} exists in the file \"{file}\" at time stamp {timeStamp}")

    return errorMessages

def AddBlacklistedTermToList(newBlacklistedTerm, foundBlacklistedTerms):
    needToUpdateList = True
    for index, foundBlacklistedTerm in enumerate(foundBlacklistedTerms):
        if newBlacklistedTerm in foundBlacklistedTerm:
            needToUpdateList = False
            break
        elif foundBlacklistedTerm in newBlacklistedTerm:
            foundBlacklistedTerms[index] = newBlacklistedTerm
            needToUpdateList = False

    if needToUpdateList:
        foundBlacklistedTerms.append(newBlacklistedTerm)
    
    return foundBlacklistedTerms

def PrintResults(errorMessages):
    if len(errorMessages) == 0:
        print("There were no blacklisted terms found within any of your transcripts")
    else:
        for message in errorMessages:
            print(message)

if __name__ == '__main__':
    main()