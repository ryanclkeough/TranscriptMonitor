import os
import re

TRANSCRIPT_FOLDER = "Transcripts"

def main():
    transcriptContents = GetTranscriptFolderContents()
    if transcriptContents:
        ParseTranscripts(transcriptContents)

def GetTranscriptFolderContents():
    transcriptContents = {}
    currentDirectory = os.path.dirname(os.path.abspath(__file__))
    transcriptsDirectory = os.path.join(currentDirectory, TRANSCRIPT_FOLDER)
    if not os.path.exists(transcriptsDirectory):
        print(f"The {TRANSCRIPT_FOLDER} folder does not exist. Aborting Process.")
    elif not os.listdir(transcriptsDirectory):
        print(f"The {TRANSCRIPT_FOLDER} folder does not contain any files. Aborting Process.")
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

def ParseTranscripts(transcriptContents):
    print(transcriptContents)

if __name__ == '__main__':
    main()