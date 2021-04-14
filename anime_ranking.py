import json

import pandas as pd
from matplotlib import pyplot as plt


class AnimeRanking:

    def __init__(self):
        self.anime_database = dict()
        self.load_anime_database()
        self.plot_anime_ranking()

    def add_anime(self, anime_title, anime_score):
        self.anime_database[anime_title] = anime_score

    def load_anime_database(self):
        self.anime_database = json.load(open('anime_database.json', mode='r'))

    def save_anime_database(self):
        json.dump(self.anime_database, open('anime_database.json', mode='w'), indent=4)

    def plot_anime_ranking(self):
        anime_titles = [title for title in self.anime_database if self.anime_database[title] is not None]
        anime_scores = [self.anime_database[title] for title in anime_titles]
        # x = np.arange(len(anime_scores))
        # width = 0.5
        # fig, ax = plt.subplots()
        # ax.bar(x, anime_scores, width)
        # ax.set_title('Anime ranking')
        # ax.set_xticks(x)
        # ax.set_xticklabels(anime_titles, rotation=75)
        df = pd.DataFrame({'scores': anime_scores},
                          index=anime_titles)
        df = df.sort_values(by=['scores'], ascending=False)
        df.plot.bar(rot=75, color={'scores': 'red'})
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    AnimeRanking()
