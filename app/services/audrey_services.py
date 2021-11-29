# create function to extract and classify named entities
import pandas
import spacy
NER = spacy.load("en_core_web_sm")

def entity_ext(text):
    Entities = []
    Labels = []
    Labels_Desc = []
    txt = NER(text)
    for i in txt.ents:
        Entities += [i.text]
        Labels += [i.label_]
        Labels_Desc += [spacy.explain(i.label_)]
    df = pandas.DataFrame(data={"Entity": Entities, "Label": Labels, "Label Desc": Labels_Desc})
    count = df['Entity'].value_counts()
    df = df.drop_duplicates()
    df = df.merge(count, how='left', left_on="Entity", left_index=False, right_index=True)
    df.columns = ["Entity", "Label", "Label Desc", "Count"]
    return df.to_json(orient = 'split')

# =====================================================================================
# create a function to split text string into sentences to score sentiment

import nltk
from nltk import sent_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def text_sentiment(text):
    scores = []
    sentences = nltk.sent_tokenize(text)
    analyzer = SentimentIntensityAnalyzer()
    for i in sentences:
        score_i = analyzer.polarity_scores(i)["compound"]
        scores += [score_i]
    df = pandas.DataFrame(data={"Sentence": sentences, "Score": scores})
    avg_score = sum(scores) / len(scores)
    if avg_score >= 0.5:
        sentiment = 'Positive'
    elif avg_score <= -0.5:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
    out_string = ("Overall text's sentiment is " + str(sentiment) + ", with an average compound score of " + str(avg_score))
    return [df.to_json(orient = 'split'), out_string]
