import get_transcripts
from time import sleep

letters = ["O"]

for letter in letters:
    get_transcripts.save_transcripts(letter)
    sleep(10)
    print("Transcripts downloaded for letter: " + letter)

print("\nEND OF MASTER TRANSCRIPT")