import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import os

# Constants
DATA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_PATH = os.path.join(DATA_DIR, 'outputs', 'cleaned_output_updated.csv')
NUM_TOPICS = 5
MAX_FEATURES = 1000

# Download NLTK data
nltk.download('stopwords')
nltk.download('punkt')


class TextProcessor:
    @staticmethod
    def preprocess_text(text):
        text = re.sub(r'[^a-zA-Z\s]', '', text, re.I|re.A)
        text = text.lower()
        tokens = text.split()
        tokens = [word for word in tokens if word not in stopwords.words('english')]
        return ' '.join(tokens)

    @staticmethod
    def summarize_text(text, num_sentences=1):

        #if 'swaps' not in text:
        #    return 'The document does not contain information on swaps.'

        sentences = sent_tokenize(text)
        if len(sentences) <= num_sentences:
            return text

        vectorizer = TfidfVectorizer()
        sentence_vectors = vectorizer.fit_transform(sentences)
        sentence_scores = sentence_vectors.sum(axis=1).A1
        top_sentence_indices = sentence_scores.argsort()[-num_sentences:][::-1]
        ranked_sentences = [sentences[i] for i in top_sentence_indices]
        return ' '.join(ranked_sentences)


class TopicModel:
    def __init__(self, num_topics):
        self.num_topics = num_topics
        self.model = None
        self.vectorizer = None

    def fit(self, documents):
        self.vectorizer = TfidfVectorizer(max_features=MAX_FEATURES)
        X_tfidf = self.vectorizer.fit_transform(documents)
        self.model = LatentDirichletAllocation(n_components=self.num_topics, random_state=42)
        self.model.fit(X_tfidf)

    def transform(self, documents):
        X_tfidf = self.vectorizer.transform(documents)
        return self.model.transform(X_tfidf)

    def get_topic_words(self, num_top_words):
        topics = []
        for topic_idx, topic in enumerate(self.model.components_):
            topic_words = " ".join([self.vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-num_top_words - 1:-1]])
            topics.append(topic_words)
        return topics


def main():
    df = pd.read_csv(FILE_PATH)
    df['combined_text'] = df.apply(lambda row: ' '.join(row.dropna().astype(str)), axis=1)
    df['processed_text'] = df['combined_text'].apply(TextProcessor.preprocess_text)

    topic_model = TopicModel(NUM_TOPICS)
    topic_model.fit(df['processed_text'])
    topic_distribution = topic_model.transform(df['processed_text'])
    df['Cluster'] = topic_distribution.argmax(axis=1)

    topics = topic_model.get_topic_words(10)
    cluster_topic_map = {i: topic for i, topic in enumerate(topics)}
    df['Cluster_Topics'] = df['Cluster'].map(cluster_topic_map)

    df['Summary'] = df['combined_text'].apply(TextProcessor.summarize_text)

    summary_table = df[['CIK', 'Cluster', 'Cluster_Topics', 'Summary']]
    summary_table.to_csv(os.path.join(DATA_DIR, 'outputs/summary_table.csv'), index=False)
    print("Summary table saved to 'summary_table.csv'")


if __name__ == "__main__":
    main()
