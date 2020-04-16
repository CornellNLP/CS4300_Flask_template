This folder is for formatting all of the transcripts before they go in the database. Once it is working, it will be run once, the data put in the database, and it won't be run again. 
How the files in this folder work:

1. run scraping.py (done - the files are in output)
This file pulls all debate links from the 2020 election and debates categories. It then makes sure there are no duplicates and removes bad transcripts (no times, etc.).
   
2. Make sure scraping is final before starting step!! Now, the output is manually checked (can use the url):
    - the title is descriptive
    - the date is correct ("YYYY-MM-DD")
    - the candidates and moderators are correctly classified
    - any duplicates in candidates and moderators are removed and the correct (full, no title) name is inputted (ie. if there's E. Warren and Sen. Warren delete both and replace with Elizabeth Warren)
    - the description is helpful, remove any references to rev.com
    - there is text for all parts (list isn't empty)* 
* If the list is empty, check the url b/c that may mean there are no timestamps or the formatting is weird in some other way. If so, delete the file and add the url to 'bad_debates' in scraping.py

3. run formatting.py
This is still under construction, but ideally it will:
    - replace all speakers in the text with the correct name from part 2
    - match all questions with responses
