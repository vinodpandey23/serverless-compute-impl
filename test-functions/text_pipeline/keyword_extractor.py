def extract_keywords(text):
    words = text.split()
    keywords = [word for word in words if len(word) > 3]
    return keywords
