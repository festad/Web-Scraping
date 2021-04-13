import sys

from PySide2.QtWidgets import (QApplication,
                               QMainWindow,
                               QVBoxLayout,
                               QWidget,
                               QPushButton,
                               QTextBrowser,
                               QScrollArea)

import radiopolskie as rp

radiopolskie_url = 'https://www.polskieradio.pl/395/7989'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PolskieRadio - PL")
        self.setGeometry(100, 100, 800, 600)

        self.scroll = QScrollArea()
        self.layout = QVBoxLayout()

        widget = QWidget()
        widget.setLayout(self.layout)

        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(widget)
        self.setCentralWidget(self.scroll)

        self.current_article_window = None

    def add_button_with_text(self, pre_article):
        print(pre_article.link)
        button_title = f'{pre_article.datetime}\n{pre_article.title}'
        button = QPushButton(button_title)
        button.clicked.connect(lambda: self.button_action(pre_article))
        self.layout.addWidget(button)

    def button_action(self, pre_article):
        print('\n\nBefore getting full article\n')
        print(f'Pre article: {pre_article.link}\n')
        article = pre_article.get_full_article()
        print(article.body)
        self.current_article_window = ArticleWindow(article)
        self.current_article_window.show()


class ArticleWindow(QWidget):
    def __init__(self, article):
        super().__init__()
        layout = QVBoxLayout()
        textbrowser = QTextBrowser()
        article_text = f'{article.title}\n\n{article.datetime}\n\n{article.body}'
        textbrowser.setPlainText(article_text)
        layout.addWidget(textbrowser)
        self.setWindowTitle(article.title)
        self.setLayout(layout)
        self.setGeometry(150, 150, 600, 600)


app = QApplication(sys.argv)
window = MainWindow()

top_news = rp.TopNews(radiopolskie_url)
for pa in top_news.pre_articles:
    print(pa.link)
    window.add_button_with_text(pa)

window.show()
app.exec_()
