
import streamlit as st
import pandas as pd
import nltk
import random
from nltk.tokenize import word_tokenize
nltk.download('punkt')

file_name = 'Social_Media_Advertising.csv'
df = pd.read_csv(file_name)

text_col = 'Target_Audience'
category_col = 'Campaign_Goal' if 'Campaign_Goal' != 'None' else None

# Create a Markov chain dictionary
def build_markov_chain(text_list, n=2):
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

# Generate text using Markov chain
def generate_markov_text(model, length=30, n=2):
    if not model:
        return "Markov model is empty. Check your dataset or n value."
    start = random.choice(list(model.keys()))
    output = list(start)
    for _ in range(length):
        key = tuple(output[-n:])
        next_word = random.choice(model.get(key, random.choice(list(model.keys()))))
        output.append(next_word)
    return ' '.join(output)

def generate_ad_by_category(cat, length=30, n=1):
    if not category_col:
        # If no category column, use the overall model
        model = build_markov_chain(df[text_col].tolist(), n)
        return generate_markov_text(model, length, n)

    filtered_texts = df[df[category_col] == cat][text_col].tolist()
    if not filtered_texts:
        return "No ads found for this category."

    model = build_markov_chain(filtered_texts, n)
    return generate_markov_text(model, length, n)


st.title("Marketing Content Generator")

# Determine appropriate n based on average word count
avg_word_count = df[text_col].apply(lambda x: len(str(x).split())).mean()
suggested_n = 1 if avg_word_count < 3 else 2

n_value = st.slider("Markov Chain Order (n)", 1, 3, suggested_n)
length_value = st.slider("Generated Text Length", 10, 100, 30)


if category_col:
    sample_cat = st.selectbox("Select Category", df[category_col].unique())
    if st.button("Generate Ad for Category"):
        ad_text = generate_ad_by_category(sample_cat, length=length_value, n=n_value)
        st.write(ad_text)
else:
    if st.button("Generate Ad"):
        # Build model using all texts
        markov_model = build_markov_chain(df[text_col].tolist(), n=n_value)
        ad_text = generate_markov_text(markov_model, length=length_value, n=n_value)
        st.write(ad_text)

