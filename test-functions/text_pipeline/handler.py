import json
from text_cleaner import clean_text
from keyword_extractor import extract_keywords
from word_counter import count_words

def handler(event):
    if isinstance(event, str):
        event = json.loads(event) 
   
    text = event.get("text", "")
    cleaned_text = clean_text(text)
    keywords = extract_keywords(cleaned_text)
    word_frequencies = count_words(keywords)
    
    result = {
        "cleaned_text": cleaned_text,
        "keywords": keywords,
        "word_frequencies": dict(word_frequencies)
    }
   
    print(json.dumps(result))  # Print the result for container output
    return result
