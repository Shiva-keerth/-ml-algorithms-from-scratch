import pandas as pd
import nltk
from nltk.util import ngrams
import random

nltk.download("punkt")
nltk.download("punkt_tab")

df=pd.read_csv("ngram.csv")
print("Columns:",df.columns)

TEXT_COLUMN = "sentence"

text_data=df[TEXT_COLUMN].dropna().astype(str)
full_text = " ".join(text_data).lower()

tokens = nltk.word_tokenize(full_text)

bigrams = list(ngrams(tokens, 2))

bigram_model = {}
for w1,w2 in bigrams:
    bigram_model.setdefault(w1, []).append(w2)

trigram =list(ngrams(tokens, 3))
trigram_model = {}
for w1,w2,w3 in trigram:
    trigram_model.setdefault((w1,w2), []).append(w3)

def generate_bigram(start_word,length=10):
    word =start_word.lower()
    sentence =[word]

    for _ in range(length):
        next_words = bigram_model.get(word)
        if not next_words:
            break
        next_word = random.choice(next_words)
        sentence.append(next_word)
        word = next_word

    return " ".join(sentence)

def generate_trigram(w1,w2,length=10):
    w1,w2 = w1.lower(), w2.lower()
    sentence =[w1,w2]

    for _ in range(length):
        next_words = trigram_model.get((w1,w2))
        if not next_words:
            break
        next_word = random.choice(next_words)
        sentence.append(next_word)
        w1,w2 = w2, next_word
    return " ".join(sentence)
print("N-gram Text Generator")


while True:
    print("Choose an option:")
    print("1. Bigram")
    print("2. Trigram")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        start = input("Enter a starting word: ")
        length = int(input("Enter the length of the sentence: "))
        print(generate_bigram(start,length))

    elif choice == "2":
        start1 = input("Enter the first word: ")
        start2 = input("Enter the second word: ")
        length= int(input("Enter the length of the sentence: "))
        print(generate_trigram(start1,start2,length))

    elif choice == "3":
        print("Exiting Program...")
        break

    else:
        print("Invalid choice. Please try again.")
