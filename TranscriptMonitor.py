import json
import os
import re

SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def main():
    transcriptContents = GetTranscriptFolderContents()
    if transcriptContents:
        blacklistedTerms = GetBlacklistedTerms()
        ParseTranscripts(transcriptContents, blacklistedTerms)

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
                print(f"Item {item} is not a file and cannot be processed")
            elif not item.endswith(".txt"):
                print(f"File {item} is not of type .txt and cannot be processed.")
            else:
                textFileContents = {}
                textFileName = os.path.basename(item)
                textFilepath = os.path.join(transcriptsDirectory, item)
                with open(textFilepath) as file:
                    timestampText = ""
                    for line in file:
                        line = line.strip()
                        if CheckIfLineIsTimestamp(line):
                            textFileContents[line] = timestampText
                        else:
                            timestampText = line

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
    for file in transcriptContents:
        for timeStamp in transcriptContents[file]:
            for blacklistedTerm in blacklistedTerms:
                if blacklistedTerm in transcriptContents[file][timeStamp]:
                    print(f"The blacklisted term \"{blacklistedTerm}\" exists in the file \"{file}\" at time stamp {timeStamp}")

if __name__ == '__main__':
    main()