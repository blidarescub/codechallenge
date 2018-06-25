from collections import Counter
from urllib.request import urlopen

from bs4 import BeautifulSoup

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from wordcloud import WordCloud


class URLProcessing(object):
    """docstring for URLProcessing"""
    def __init__(self, url):
        super(URLProcessing, self).__init__()
        nltk.download('stopwords')
        nltk.download('punkt')
        self.stop_words = set(stopwords.words('english'))
        self.url = url
        self.html = urlopen(url).read()
        self.soup = BeautifulSoup(self.html, "html.parser")
        self.filtered_words = []
        self.frequencies = None
        self.text = ""

    def get_filtered_words(self):
        for script in self.soup(["script", "style"]):
            script.extract()

        text = self.soup.get_text()

        lines = (line.strip() for line in text.splitlines())
        chunks = (
            phrase.strip() for line in lines for phrase in line.split("  ")
        )
        text = '\n'.join(chunk for chunk in chunks if chunk)
        self.text = text
        words = word_tokenize(text)
        wordsfiltered = [word.lower() for word in words if word.isalpha()]

        self.filtered_words = [
            word for word in wordsfiltered if word
            not in stopwords.words('english')
        ]
        return self.filtered_words

    def get_frequency(self):
        cnt = Counter()
        for word in self.filtered_words:
                cnt[word] += 1
        self.frequencies = cnt
        return self.frequencies

    def get_top_100(self):
        freq_clean = nltk.FreqDist(self.filtered_words)
        return list(freq_clean.items())[:100]

    def generate_word_cloud(self):
        wc = WordCloud(
            max_words=100, margin=10, background_color='white',
            scale=2, relative_scaling=0.5, width=500, height=400,
            random_state=1
        ).generate_from_frequencies(self.frequencies)
        # .to_file("wordcloud.png")
        return wc
