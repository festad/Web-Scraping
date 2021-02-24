import sys
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextBrowser, QScrollArea
from polish_news import get_news, news_to_article



class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Polish News")
		self.setGeometry(100, 100, 800, 600)
		
		self.scroll = QScrollArea()
		self.layout = QVBoxLayout()
		
		widget = QWidget()
		widget.setLayout(self.layout)
		
		self.scroll.setWidgetResizable(True)
		self.scroll.setWidget(widget)
		self.setCentralWidget(self.scroll)
		
		self.article_window = None
		
		
	def add_button_with_text(self, news):
		button = QPushButton(news[1])
		button.setCheckable(True)
		button.clicked.connect(lambda: self.button_action(news))
		self.layout.addWidget(button)
		
		
	def button_action(self, news):
		article_tuple = news_to_article(news)
		print(article_tuple[1])
		self.article_window = ArticleWindow(article_tuple)
		self.article_window.show()
		
		
class ArticleWindow(QWidget):
	def __init__(self, article_tuple):
		super().__init__()
		layout = QVBoxLayout()
		textbrowser = QTextBrowser()
		textbrowser.setPlainText(article_tuple[1])
		layout.addWidget(textbrowser)
		self.setLayout(layout)
		self.setGeometry(150, 150, 600, 600)
		
		
		

app = QApplication(sys.argv)
window = MainWindow()

news = get_news()
for n in news[0]:
	window.add_button_with_text(n)

window.show()
app.exec_()
