# TranscriptMonitor
Takes in a text file of a video transcript, and parses the document for any profanity. This will return either a pass, or a list of bad words paired with their time stamps

## Steps
1. Add 1 or more .txt transcript files to the `Transcripts` folder (Ensure your transcript has timestamps)
2. Create a json with your list of blacklisted terms with the filename `BlacklistedTerms.json`. The current repo does not have a blacklist file yet, so you will need to make your own.
3. Run!
4. Remove added transcript files after use

## Disclaimer
Do not add anything to the downloaded repo except .txt trascript files in the `Transcripts` folder. 
Do not delete anything from the repo except the .txt trascript files you added in the `Transcripts` folder.
If for any reason you did not follow these steps, the script might not work as expected