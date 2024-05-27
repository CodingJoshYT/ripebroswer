import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QToolBar, QVBoxLayout, QWidget, QAction, QComboBox, QHBoxLayout, QFileDialog, QMessageBox, QPushButton, QTabWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt

class RipeBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ripe Browser")
        self.setGeometry(100, 100, 1000, 700)

        self.setStyleSheet("""
            QToolBar {
                background-color: #F0F0F0;
                border: 1px solid #CCC;
            }
            QLineEdit, QComboBox {
                padding: 6px;
                font-size: 14px;
            }
            QPushButton {
                padding: 6px 10px;
                font-size: 14px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        self.setup_ui()

    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        layout.addWidget(self.tabs)

        # Add initial tab
        self.add_new_tab()

        # Toolbar
        self.toolbar = QToolBar()
        layout.addWidget(self.toolbar)

        # Back button
        back_button = QAction("Back", self)
        back_button.triggered.connect(self.tabs.currentWidget().back)
        self.toolbar.addAction(back_button)

        # Forward button
        forward_button = QAction("Forward", self)
        forward_button.triggered.connect(self.tabs.currentWidget().forward)
        self.toolbar.addAction(forward_button)

        # Refresh button
        refresh_button = QAction("Refresh", self)
        refresh_button.triggered.connect(self.tabs.currentWidget().reload)
        self.toolbar.addAction(refresh_button)

        # Home button
        home_button = QAction("Home", self)
        home_button.triggered.connect(self.go_home)
        self.toolbar.addAction(home_button)

        # Address bar and Go button
        address_layout = QHBoxLayout()
        self.address_bar = QLineEdit()
        self.address_bar.returnPressed.connect(self.navigate)
        self.address_bar.setPlaceholderText("Search or enter URL")
        address_layout.addWidget(self.address_bar)

        go_button = QPushButton("Go")
        go_button.clicked.connect(self.navigate)
        address_layout.addWidget(go_button)

        # Website selector
        self.website_selector = QComboBox()
        self.website_selector.addItems(["Google", "Discord", "Spotify", "Amazon", "YouTube"])
        self.website_selector.currentIndexChanged.connect(self.navigate_to_selected_website)
        address_layout.addWidget(self.website_selector)

        # Add address bar and website selector to toolbar
        self.toolbar.addWidget(self.address_bar)
        self.toolbar.addWidget(go_button)
        self.toolbar.addWidget(self.website_selector)

        self.add_tab_button = QPushButton("+")
        self.add_tab_button.clicked.connect(self.add_new_tab)
        self.toolbar.addWidget(self.add_tab_button)

    def add_new_tab(self):
        browser = QWebEngineView()
        browser.page().profile().downloadRequested.connect(self.download_requested)
        browser.load(QUrl("https://www.google.com"))
        index = self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentIndex(index)

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.close()

    def navigate(self):
        text = self.address_bar.text()
        url = QUrl(text)
        if not url.isValid() or url.scheme() == '':
            if ' ' in text:
                search_url = QUrl('https://www.google.com/search?q=' + '+'.join(text.split()))
            else:
                search_url = QUrl('https://www.google.com/search?q=' + text)
            self.tabs.currentWidget().setUrl(search_url)
        else:
            self.tabs.currentWidget().setUrl(url)

    def navigate_to_selected_website(self, index):
        websites = {
            "Google": "https://www.google.com",
            "Discord": "https://discord.com",
            "Spotify": "https://www.spotify.com",
            "Amazon": "https://www.amazon.com",
            "YouTube": "https://www.youtube.com"
        }
        website = self.website_selector.itemText(index)
        self.tabs.currentWidget().setUrl(QUrl(websites.get(website)))

    def download_requested(self, download):
        path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*)")
        if path:
            download.setPath(path)
            download.accept()

    def go_home(self):
        self.tabs.currentWidget().setUrl(QUrl("https://www.google.com"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RipeBrowser()
    window.show()
    sys.exit(app.exec_())
