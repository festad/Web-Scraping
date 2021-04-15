import json

import pandas as pd
from matplotlib import pyplot as plt


class AnimeRanking:

    def __init__(self):
        self.anime_database = dict()
        self.load_anime_database()
        # self.plot_anime_ranking()

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
        df.plot.bar(rot=90, color={'scores': 'red'})
        plt.tight_layout()
        plt.show()


def main():
    a = AnimeRanking()
    while True:
        print('1 - Add title and score\n'
              '2 - Plot\n'
              '3 - Save\n'
              'E - Exit')
        choice = input('-> ')
        if choice == '1':
            title = input('Insert title:\n'
                          '-> ')
            score = float(input('Insert score [0 - 100]\n'
                              '-> '))
            a.add_anime(title, score)
        elif choice == '2':
            a.plot_anime_ranking()
        elif choice == '3':
            a.save_anime_database()
        elif choice.lower() == 'e':
            print('Exit!')
            exit(0)
        else:
            print('Invalid choice!')


if __name__ == '__main__':
    main()