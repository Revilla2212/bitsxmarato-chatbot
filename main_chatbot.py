#!/usr/bin/python3.6

import nltk
import random
import string
import re, string, unicodedata
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
import wikipedia as wk
from collections import defaultdict
import warnings
warnings.filterwarnings("ignore")
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel
from googletrans import Translator

data = open('./Datasource.txt','r',errors = 'ignore')
raw = data.read()
raw = raw.lower()

sent_tokens = nltk.sent_tokenize(raw)

_srclang='en'
_destlang='en'
def tr(og_msg):
    global _destlang
    global _srclang
    translator = Translator()
    msg = og_msg
    msg_tr= translator.translate(msg,src=_srclang, dest=_destlang).text
    return msg_tr

def Normalize(text):
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
    #word tokenization
    word_token = nltk.word_tokenize(text.lower().translate(remove_punct_dict))
    
    #remove ascii
    new_words = []
    for word in word_token:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    
    #Remove tags
    rmv = []
    for w in new_words:
        text=re.sub("&lt;/?.*?&gt;","&lt;&gt;",w)
        rmv.append(text)
        
    #pos tagging and lemmatization
    tag_map = defaultdict(lambda : wn.NOUN)
    tag_map['J'] = wn.ADJ
    tag_map['V'] = wn.VERB
    tag_map['R'] = wn.ADV
    lmtzr = WordNetLemmatizer()
    lemma_list = []
    rmv = [i for i in rmv if i]
    for token, tag in nltk.pos_tag(rmv):
        lemma = lmtzr.lemmatize(token, tag_map[tag[0]])
        lemma_list.append(lemma)
    return lemma_list

welcome_input = ("hello", "hi", "greetings", "sup", "what's up","hey",)
welcome_response = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]
def welcome(user_response):
    for word in user_response.split():
        if word.lower() in welcome_input:
            return random.choice(welcome_response)

def generateResponse(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=Normalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    #vals = cosine_similarity(tfidf[-1], tfidf)
    vals = linear_kernel(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0) or "tell me about" in user_response:
        print("Checking Wikipedia")
        if user_response:
            robo_response = wikipedia_data(user_response)
            return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response#wikipedia search

def wikipedia_data(input):
    reg_ex = re.search('tell me about (.*)', input)
    try:
        if reg_ex:
            topic = reg_ex.group(1)
            wiki = wk.summary(topic, sentences = 3)
            return wiki
    except Exception as e:
            print("No content has been found")

def diag_response(data,symptom,addif):
    user_response = input()
    user_response=user_response.lower()
    if user_response == addif:
        data=data+symptom+','
    elif user_response not in ['yes','no']:
        print("Chatterbot : Please type yes or no")
        diag_response(data,symptom,addif)
    return data

def start():
    data=''
    string_var="Chatterbot : Starting the diagnostic..."
    print(tr(string_var))
    string_var="Do you feel dizzy?"
    print(tr(string_var))
    data=diag_response(data,'dizziness','yes')
    string_var="Do you usually feel pain in the chest?"
    print(tr(string_var))
    data=diag_response(data,'chest pain','yes')
    string_var="Thank you, your anwers are being processed..."
    print(tr(string_var))
    if data != '':
        data=data[:-1]
    return data

def change_lang():
    global _destlang
    string_var="""Type the number that mathes the language you want to select:
    1 - English
    2 - Catalan
    3 - Spanish
    4 - Italian
    5 - French
    6 - Portuguese
    7 - Russian
    8 - Chinese
    9 - Japanese
    """
    print(tr(string_var))
    user_response = input()
    user_response=user_response.lower()
    if user_response == '1':
        _destlang='en'
    elif user_response == '2':
        _destlang='ca'
    elif user_response == '3':
        _destlang='es'
    elif user_response == '4':
        _destlang='it'
    elif user_response == '5':
        _destlang='fr'
    elif user_response == '6':
        _destlang='pt'
    elif user_response == '7':
        _destlang='ru'
    elif user_response == '8':
        _destlang='zh-cn'
    elif user_response == '9':
        _destlang='ja'
    else:
        string_var="Incorrect input. Please, select an existing option"
        print(tr(string_var))
        change_lang()

### MAIN

flag=True
initstr="""My name is Mirabot and I'm a chatbot. The available options are:
          - To begin the diagnostic, type start
          - To change the language, type lang
          - To ask a question, type 'tell me about' followed by the question
          - To exit, type bye"""
print(initstr)
while(flag==True):
    user_response = input()
    user_response=user_response.lower()
    if(user_response not in ['bye','shutdown','exit', 'quit']):
        if(user_response=='thanks' or user_response=='thank you' ):
            flag=False
            string_var="Chatterbot : You are welcome.."
            print(tr(string_var))
        elif user_response=='start':
            symptoms=start()
            if symptoms != '':
                user_response="tell me about "+symptoms
                print("Chatterbot : ",end="")
                string_var=generateResponse(user_response)
                print(tr(string_var))
                sent_tokens.remove(user_response)
            else:
                string_var="Chatterbot : Not enough data"
                print(tr(string_var))
        elif user_response=='lang':
            change_lang()
            string_var="Language changed"
            print(tr(string_var))
            print("\n")
            print(tr(initstr))
            #print(tr(string_var))
        elif user_response=='help':
            print(tr(initstr))
        else:
            if(welcome(user_response)!=None):
                print("Chatterbot : "+welcome(user_response))
            else:
                print("Chatterbot : ",end="")
                string_var=generateResponse(user_response)
                try:
                    print(tr(string_var))
                except:
                    print(tr("Nothing found"))
                sent_tokens.remove(user_response)
    else:
        flag=False
        print("Chatterbot : Bye!!! ")
