import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import streamlit as st

stopwords = list(STOP_WORDS)
nlp = spacy.load('en_core_web_sm')


def word_frequency_analysis(text):
    doc = nlp(text)
    word_frequencies = {}

    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1

    return word_frequencies


def generate_summary(text):
    doc = nlp(text)
    word_frequencies = word_frequency_analysis(text)

    # Calculate the summary length as a fixed percentage of total sentences
    sentence_tokens = [sent for sent in doc.sents]
    select_length_percentage = 30  # You can adjust this percentage
    select_length = int(len(sentence_tokens) * (select_length_percentage / 100))

    # Use sentence scores based on word frequencies
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]

    # Generate summary using nlargest
    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    final_summary = ' '.join([word.text for word in summary])
    return final_summary


def main():
    st.title("Text Summarization")

    # Input text from user
    user_input = st.text_area("Enter your text here:")

    if st.button("Run"):
        # Get the length of the original text
        original_length = len(user_input)

        # Generate and display summary
        final_summary = generate_summary(user_input)
        st.subheader("Summary:")
        st.write(final_summary)

        # Get the length of the summary
        summary_length = len(final_summary)

        # Show the lengths
     

        st.markdown(f"Original Text Length: <span style='color:red'>{original_length} characters</span>", unsafe_allow_html=True)
        st.markdown(f"Summary Length: <span style='color:blue'>{summary_length} characters</span>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()

