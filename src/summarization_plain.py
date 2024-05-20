import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import os


# Download NLTK data
nltk.download('stopwords')
nltk.download('punkt')

# Load and prepare the data
data_dir = 'outputs/'
file_path = os.path.join(data_dir, 'cleaned_output_updated.csv')
df = pd.read_csv(file_path)
df['combined_text'] = df.apply(lambda row: ' '.join(row.dropna().astype(str)), axis=1)


def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text, re.I|re.A)
    text = text.lower()
    tokens = text.split()
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    return ' '.join(tokens)

df['processed_text'] = df['combined_text'].apply(preprocess_text)

vectorizer = TfidfVectorizer(max_features=1000)
X_tfidf = vectorizer.fit_transform(df['processed_text'])

num_topics = 5
lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
lda.fit(X_tfidf)

# Assign topics to each document
topic_distribution = lda.transform(X_tfidf)
df['Cluster'] = topic_distribution.argmax(axis=1)


def get_topic_words(model, feature_names, num_top_words):
    topics = []
    for topic_idx, topic in enumerate(model.components_):
        topic_words = " ".join([feature_names[i] for i in topic.argsort()[:-num_top_words - 1:-1]])
        topics.append(topic_words)
    return topics


# Get the top words for each topic
topics = get_topic_words(lda, vectorizer.get_feature_names_out(), 10)


# Summarize text function
def summarize_text(text, num_sentences=1):
    sentences = sent_tokenize(text)
    if len(sentences) <= num_sentences:
        return text  # If the text is shorter than the number of sentences needed, return the whole text

    vectorizer = TfidfVectorizer()
    sentence_vectors = vectorizer.fit_transform(sentences)

    # Sum the TF-IDF scores for each sentence
    sentence_scores = sentence_vectors.sum(axis=1).A1  # .A1 converts matrix to a 1D array

    # Get the indices of the top-ranked sentences
    top_sentence_indices = sentence_scores.argsort()[-num_sentences:][::-1]

    # Select and return the top-ranked sentences
    ranked_sentences = [sentences[i] for i in top_sentence_indices]
    return ' '.join(ranked_sentences)


# Summarize text
df['Summary'] = df['combined_text'].apply(summarize_text)
cluster_topic_map = {i: topic for i, topic in enumerate(topics)}
df['Cluster_Topics'] = df['Cluster'].map(cluster_topic_map)

# Create the summary table
summary_table = df[['CIK', 'Cluster', 'Cluster_Topics', 'Summary']]
summary_table.to_csv(os.path.join(data_dir, 'summary_table.csv'), index=False)
print("Summary table saved to 'summary_table.csv'")