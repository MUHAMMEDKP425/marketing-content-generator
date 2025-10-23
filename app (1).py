import streamlit as st
import pandas as pd
import random
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')

# Load CSV from Google Drive
file_id = "1Nz5_63fpog9O5ejPErbTmxgWtqM1eLRr"
url = f"https://drive.google.com/uc?export=download&id={file_id}"
df = pd.read_csv(url)

# Detect text column
text_col = df.select_dtypes(include='object').columns[0]

# Build simple Markov chain model
def build_markov_chain(text_list, n=1):
    model = {}
    for text in text_list:
        words = word_tokenize(str(text))
        if len(words) <= n:
            continue
        for i in range(len(words)-n):
            key = tuple(words[i:i+n])
            next_word = words[i+n]
            if key not in model:
                model[key] = []
            model[key].append(next_word)
    return model

def generate_markov_text(model, length=30, n=1):
    if not model:
        return "No data to generate ads."
    start = random.choice(list(model.keys()))
    output = list(start)
    for _ in range(length):
        key = tuple(output[-n:])
        next_word = random.choice(model.get(key, random.choice(list(model.keys()))))
        output.append(next_word)
    return ' '.join(output)

markov_model = build_markov_chain(df[text_col].tolist(), n=1)

# Streamlit UI
st.title("Marketing Content Generator")
length = st.slider("Length of ad (words)", 10, 100, 30)

if st.button("Generate Ad"):
    ad = generate_markov_text(markov_model, length)
    st.success(ad)
