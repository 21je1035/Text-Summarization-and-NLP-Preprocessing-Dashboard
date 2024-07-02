# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1iZtgVF2AhhRegVfhRmnMMtiU7ybDWzVr

In this notebook preprocessing of movie decriptions is done for further nlp projects.
The steps are as follows:

1.Data Acquisition

    -retrieving the data from api
    -converting json data in dataframe
2.Text Preparation

    -Lowercasing
    -removing html tags and urls
    -removing punctuations
    -changing short chat words
    -spelling corrections
    -removing stop words
    -replacing emojis with their meanings
    -tokenizing
    -stemming/lemmitization
"""

import requests
import pandas as pd
df=pd.DataFrame()

#dataset used is from the moviedb website so create your own api id and run this code
for page_number in range(1, 472):
    url = f"https://api.themoviedb.org/3/movie/top_rated?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US&page={page_number}"

    response = requests.get(url)
    temp_df = pd.DataFrame(response.json()['results'])[['genre_ids','title','overview']]
    df = pd.concat([df,temp_df],ignore_index=True)

df['genre_ids'].head()

response=requests.get("https://api.themoviedb.org/3/genre/movie/list?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US")

empty={}
for i in range(len(response.json()['genres'])):
    empty[response.json()['genres'][i]['id']]=response.json()['genres'][i]['name']

empty

#exchange the genre ids with genre names
for i in range(len(df['genre_ids'])):
    for j in range(len(df['genre_ids'][i])):
        df['genre_ids'][i][j]=empty[df['genre_ids'][i][j]]
df['genre_ids']

df.size

#change to lowercase
df['overview']=df['overview'].str.lower()

#to remove html tags
import re
CLEANR = re.compile('<.*?>')

def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext

df['overview']=df['overview'].apply(cleanhtml)

df['overview']

#to remove urls from list
def remove_url(text):
  pattern = re.compile(r'https?://\S+|www.\.\S+')
  return pattern.sub(r'',text)

df['overview']=df['overview'].apply(remove_url)

#to remove punctuations
import string
def remove_punct(text):
  return text.translate(str.maketrans('', '', string.punctuation))

df['overview']=df['overview'].apply(remove_punct)

#chat_words full forms
chat_words = {
    "AFAIK": "As Far As I Know",
    "AFK": "Away From Keyboard",
    "ASAP": "As Soon As Possible",
    "ATK": "At The Keyboard",
    "ATM": "At The Moment",
    "A3": "Anytime, Anywhere, Anyplace",
    "BAK": "Back At Keyboard",
    "BBL": "Be Back Later",
    "BBS": "Be Back Soon",
    "BFN": "Bye For Now",
    "B4N": "Bye For Now",
    "BRB": "Be Right Back",
    "BRT": "Be Right There",
    "BTW": "By The Way",
    "B4": "Before",
    "CU": "See You",
    "CUL8R": "See You Later",
    "CYA": "See You",
    "FAQ": "Frequently Asked Questions",
    "FC": "Fingers Crossed",
    "FWIW": "For What It's Worth",
    "FYI": "For Your Information",
    "GAL": "Get A Life",
    "GG": "Good Game",
    "GN": "Good Night",
    "GMTA": "Great Minds Think Alike",
    "GR8": "Great!",
    "G9": "Genius",
    "IC": "I See",
    "ICQ": "I Seek you",
    "ILU": "I Love You",
    "IMHO": "In My Honest/Humble Opinion",
    "IMO": "In My Opinion",
    "IOW": "In Other Words",
    "IRL": "In Real Life",
    "KISS": "Keep It Simple, Stupid",
    "LDR": "Long Distance Relationship",
    "LMAO": "Laugh My A.. Off",
    "LOL": "Laughing Out Loud",
    "LTNS": "Long Time No See",
    "L8R": "Later",
    "MTE": "My Thoughts Exactly",
    "M8": "Mate",
    "NRN": "No Reply Necessary",
    "OIC": "Oh I See",
    "PITA": "Pain In The Ass",
    "PRT": "Party",
    "PRW": "Parents Are Watching",
    "QPSA?": "Que Pasa?",
    "ROFL": "Rolling On The Floor Laughing",
    "ROFLOL": "Rolling On The Floor Laughing Out Loud",
    "ROTFLMAO": "Rolling On The Floor Laughing My Ass Off",
    "SK8": "Skate",
    "STATS": "Your sex and age",
    "ASL": "Age, Sex, Location",
    "THX": "Thank You",
    "TTFN": "Ta-Ta For Now!",
    "TTYL": "Talk To You Later",
    "U": "You",
    "U2": "You Too",
    "U4E": "Yours For Ever",
    "WB": "Welcome Back",
    "WTF": "What The Fuck",
    "WTG": "Way To Go!",
    "WUF": "Where Are You From?",
    "W8": "Wait...",
    "7K": "Sick:-D Laugher",
    "TFW": "That feeling when",
    "MFW": "My face when",
    "MRW": "My reaction when",
    "IFYP": "I feel your pain",
    "LOL": "Laughing out loud",
    "TNTL": "Trying not to laugh",
    "JK": "Just kidding",
    "IDC": "I don’t care",
    "ILY": "I love you",
    "IMU": "I miss you",
    "ADIH": "Another day in hell",
    "ZZZ": "Sleeping, bored, tired",
    "WYWH": "Wish you were here",
    "TIME": "Tears in my eyes",
    "BAE": "Before anyone else",
    "FIMH": "Forever in my heart",
    "BSAAW": "Big smile and a wink",
    "BWL": "Bursting with laughter",
    "LMAO": "Laughing my ass off",
    "BFF": "Best friends forever",
    "CSL": "Can’t stop laughing"
}

def replace_short_forms(text):
  for short_form, long_form in chat_words.items():
    text = text.replace(short_form, long_form)
  return text
df['overview']=df['overview'].apply(replace_short_forms)

#this is used to remove stopwords
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
def remove_stopwords(text):
  new_text=[]
  for word in text.split():
    if word not in stopwords.words('english'):
      new_text.append(word)
  return ' '.join(new_text)
df['overview']=df['overview'].apply(remove_stopwords)

#to replace emojis with their meaning
!pip install emoji
import emoji
df["overview"]=df["overview"].apply(lambda x: emoji.demojize(x))

#applying tokenizer using spacy library
!pip install spacy
import spacy
nlp=spacy.load('en_core_web_sm')
def tokenizer(text):
  doc=nlp(text)
  return [token.lemma_ for token in doc]
df['overview']=df['overview'].apply(tokenizer)

#this is used to replace word with correct spellings
#takes a lot of time, so if not required skip this part
!pip install autocorrect
from autocorrect import Speller
def spellingchecker(text):
  spell=Speller(lang='en')
  for word in text:
    word=spell(word)
  return text
df['overview']=df['overview'].apply(spellingchecker)

#(stemming process)lemmatizing using nltk.stem
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
def lemmatizing(text):
   for word in text:
      word=lemmatizer.lemmatize(word)
   return text
df['overview']=df['overview'].apply(lemmatizing)

"""And your description is ready for further NLP processing"""

df['overview'].head()