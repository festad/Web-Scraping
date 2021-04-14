import pandas as pd
# import spacy
from matplotlib import pyplot as plt
import tokenize as tk


class TextAnalyzer:
    def __init__(self, language='pl', source='source.txt'):
        self.language = language
        self.source = source
        self.tokenized_text = dict()
        # self.read_from_file(source)
        self.tokenize()
        self.plot()

    # def read_from_file(self, filename: str):
    #     self.text = '\n'.join(list(open(filename, 'r')))
    #     self.tokenize()

    def tokenize(self):
        # nlp = spacy.load(f'{self.language}_core_news_sm')
        # doc = nlp(self.text)
        # tokenized_text = {}

        # for token in doc:
        #     if not token.text.isalnum():
        #         continue
        #     if token.text.lower() in tokenized_text:
        #         tokenized_text[token.text.lower()] += 1
        #     else:
        #         tokenized_text[token.text.lower()] = 1
        self.tokenized_text = {}
        tokens = tk.generate_tokens(open(self.source, 'r').readline)
        k = 0
        for token in tokens:
            # print(token)
            token = token.string
            if not token.isalnum():
                continue
            if token.lower() in self.tokenized_text:
                self.tokenized_text[token.lower()] += 1
            else:
                self.tokenized_text[token.lower()] = 1
            k += 1
        print(f'#ALL_WORDS:      {k}')
        print(f'#DISTINCT_WORDS: {len(self.tokenized_text)}')
        # self.tokenized_text = tokenized_text

    def plot(self):
        words = [word for word in self.tokenized_text]
        occurrences = [self.tokenized_text[word] for word in words]

        df = pd.DataFrame({'occurrences': occurrences},
                          index=words)

        # the following indexes may or not generate errors depending
        # on the size and shape of the file you are analyzing,
        # so they are meant to be adjusted to fit your needs,
        # ex: - df = df.sort_values(...)[:n_elements]
        #     - df = df.sort_values(...)[begin:end]

        n_elements = 50
        begin = 100
        end = 150
        df = df.sort_values(by=['occurrences'], ascending=False)[begin:end]
        df.plot.bar(rot=90, color={'occurrences': 'red'})
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    print('You need to have a source file to analyze though...')
    TextAnalyzer(source='source.txt')