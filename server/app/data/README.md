This folder is for formatting the transcripts before they go in the database. Once it is working, it will be run once, the data put in the database, and it won't be run again. 
How the files in this folder work:

1. run scraping.py (done - the files are in debates and others)
This file pulls all debate links from the 2020 election and debates categories. It then makes sure there are no duplicates and removes bad transcripts (no times, etc.).
   
2. Make sure scraping is final before starting step!! Now, the files are manually checked (can use the url):
    - the title is descriptive
    - the date is correct ("YYYY-MM-DD")
    - the candidates and other_speakers are correctly classified
    - any duplicates in candidates and other_speakers are removed and the correct (full, no title) name is inputted (ie. if there's E. Warren and Sen. Warren delete both and replace with Elizabeth Warren)
    - the description is helpful, remove any references to rev.com
    - there is text for all parts (list isn't empty)* 
*If the list is empty, check the url b/c that may mean there are no timestamps or the formatting is weird in some other way. If so, delete the file and add the url to 'bad_debates' in scraping.py

3. run formatting.py
This is mostly done. Some updates may be made later, but for now:
    - replace all speakers in the text with the correct name from part 2
    - combine speakers' responses when they are briefly interrupted
    - label all responses as questions or not
    - match all responses with questions
    - random fixes to prevent rerunning scraping (ex. converting sets to lists)


Debate Info Structure:

{

    "url": str, 
    "title": str, 
    "tags": list of str,
    "date": "YYYY-MM-DD", 
    "candidates": list of str, 
    "other_speakers": list of str, 
    "description": str, 
    "parts": [
        {
            "number": null (only one part) or int, 
            "video": str (not the actual video link since that expires), 
            "text": [
                {
                    "speaker": str, 
                    "time": str, 
                    "text": str,
                    "question": bool,
                    "response": list of int (if question) or int
                }, 
            ]
        },
    ]
}


Right now there are two folders: debates and others. I think we should focus on debates for the first prototype.