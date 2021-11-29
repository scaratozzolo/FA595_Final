import spacy
import contextualSpellCheck # pip install contextualSpellCheck
from textblob import TextBlob
  

def spellcheck(text):
    
    nlp = spacy.load('en_core_web_sm')
    contextualSpellCheck.add_to_pipe(nlp)
    
    # Check spelling and grammar of text
    spelled = nlp(text)
    spelled = spelled._.outcome_spellCheck
    
    return {"spellchecked": spelled}

def translate(text, language):
    
    blob = TextBlob(text)
    
    # Translate text to another language (automatically spellchecks)
    '''Add reference to language codes in README'''
    translated = str(blob.translate(to=language))

    return {"translated": translated}

if __name__ == '__main__':
#     print(spellcheck(text))
    text = "The brown fox laeped over the hole."
    language = 'fr' 
    print(translate(text, language))
