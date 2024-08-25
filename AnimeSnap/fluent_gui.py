from PyQt6.QtCore import QSize, QUrl
from PyQt6.QtGui import QDesktopServices, QIcon
from PyQt6.QtWidgets import (QFileDialog, QHBoxLayout, QLabel, QMessageBox,
                             QPushButton, QStackedWidget, QVBoxLayout, QWidget)
from qfluentwidgets import (CaptionLabel, CheckBox, FluentIcon,  # type: ignore
                            LineEdit, MessageBox, MSFluentWindow,
                            NavigationItemPosition, PrimaryPushButton, Theme,
                            setTheme)
#from qframelesswindow import *  # type: ignore

from AnimeSnap.json_operations import json_to_tabular


class Window(MSFluentWindow):
    """Main window class. Uses MSFluentWindow to imitate the Windows 11 FLuent Design windows."""

    def __init__(self):
        # self.isMicaEnabled = False
        super().__init__()
        # self.setTitleBar(CustomTitleBar(self))
        # self.tabBar = self.titleBar.tabBar  # type: TabBar

        setTheme(Theme.DARK)

        # create sub interface
        self.homeInterface = App(self)
        # self.settingInterface = Settings()
        # self.settingInterface.setObjectName("markdownInterface")

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(
            self.homeInterface,
            FluentIcon.SEARCH,
            "Find Anime",
            FluentIcon.SEARCH,
            NavigationItemPosition.TOP,
        )
        # self.addSubInterface(self.settingInterface, FluentIcon.SETTING, 'Settings', FluentIcon.SETTING,  NavigationItemPosition.BOTTOM)
        self.navigationInterface.addItem(
            routeKey="Help",
            icon=FluentIcon.INFO,
            text="About",
            onClick=self.showMessageBox,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )

        self.navigationInterface.setCurrentItem(self.homeInterface.objectName())

    def initWindow(self):
        self.resize(500, 160)
        self.setWindowIcon(QIcon("icons/icon.png"))
        self.setWindowTitle("AnimeSnap")

        w, h = 1200, 800
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def showMessageBox(self):
        w = MessageBox(
            "AnimeSnap 🏯",
            (
                "Version : 3.0"
                + "\n"
                + "\n"
                + "\n"
                + "💝  I hope you'll enjoy using AnimeSnap as much as I did while coding it  💝"
                + "\n"
                + "\n"
                + "\n"
                + "Made with 💖 By Rohan Kishore"
            ),
            self,
        )
        w.yesButton.setText("GitHub")
        w.cancelButton.setText("Return")

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://github.com/rohankishore/AnimeSnap"))


class App(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("AnimeSnap")
        self.setGeometry(100, 100, 450, 150)

        self.mainApp = parent

        # Create a stacked widget to manage different screens
        self.stacked_widget = QStackedWidget(self)

        # Create the main menu widget
        self.main_menu_widget = QWidget(self)
        self.stacked_widget.addWidget(self.main_menu_widget)

        self.img_path = ""
        self.img_url = ""
        self.anilist_id = ""
        self.ctheme = "dark"

        layout = QVBoxLayout(self)
        layout.addStretch()
        self.setLayout(layout)

        self.buttons_frame = QWidget(self)
        layout.addWidget(self.buttons_frame)

        # Create a horizontal layout
        top_layout = QHBoxLayout()
        button_layout = QHBoxLayout()
        checkbox_layout = QHBoxLayout()

        layout.addLayout(top_layout)

        layout.addWidget(QLabel(""))

        self.img_url_entry = LineEdit(self)
        self.img_url_entry.setPlaceholderText("Enter image URL or Upload an image")

        self.file_path_label = CaptionLabel()

        button_layout.addWidget(self.img_url_entry)

        open_image_icon = QIcon("icons/folder.png")
        self.open_image_button = QPushButton(self)
        self.open_image_button.setStyleSheet(
            """
        QPushButton {
        border: none;
        }
        """
        )
        self.open_image_button.clicked.connect(self.open_image)
        self.open_image_button.setIcon(open_image_icon)
        self.open_image_button.setIconSize(QSize(23, 23))
        self.open_image_button.setFixedSize(28, 28)
        button_layout.addWidget(self.open_image_button)

        layout.addLayout(button_layout)  # Add the button layout to the main layout
        layout.addWidget(self.file_path_label)

        layout.addWidget(QLabel(""))

        layout.addLayout(checkbox_layout)  # Add the checkbox layout to the main layout

        self.checkbox_rbb = CheckBox()
        self.checkbox_rbb.setText("Remove Black Borders")
        checkbox_layout.addWidget(self.checkbox_rbb)

        self.checkbox_iad = CheckBox()
        self.checkbox_iad.setText("Include All Details")
        checkbox_layout.addWidget(self.checkbox_iad)

        layout.addWidget(QLabel(""))

        anilist_label = CaptionLabel()
        anilist_label.setText("Anilist Anime ID [OPTIONAL] [https://anilist.co/]")
        layout.addWidget(anilist_label)

        self.anilist_entry = LineEdit(self)
        self.anilist_entry.setPlaceholderText(
            "Use this if you know what anime it is and you just need the scene details"
        )
        layout.addWidget(self.anilist_entry)

        search_button = PrimaryPushButton()
        search_button.setText("Search")
        search_button.clicked.connect(self.onClickSearch)
        layout.addWidget(search_button)

    def open_image(self):
        # options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image to Search",
            "",
            "Image Files (*.jpg *.png *.bmp);;All Files (*)",
        )

        if file_path:
            self.img_path = file_path
            self.file_path_label.setText(file_path)

    def returnToMenu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu_widget)
        self.img_path = ""
        self.file_path_label.setText(
            ""
        )  # Use self.file_path_label instead of self.main_menu_widget.file_path_label

    def onClickSearch(self):
        self.img_url = self.img_url_entry.text()
        anilist_id = self.anilist_entry.text()
        iad_status = self.checkbox_iad.isChecked()
        rbb_status = self.checkbox_rbb.isChecked()
        anilist_status = anilist_id if anilist_id else None

        if self.img_url or self.img_path != "":
            while self.layout().count():
                item = self.layout().takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

            if self.checkbox_iad.isChecked():
                iad_status = True
            else:
                iad_status = False

            if self.checkbox_rbb.isChecked():
                rbb_status = True
            else:
                rbb_status = False

            if anilist_id == "":
                anilist_status = None
            else:
                anilist_status = anilist_id

            if self.img_url == "":
                # TODO: Call the search_anime function instead
                #search.search_img(self, anilist_info=anilist_status, rbb=rbb_status)
                pass
            else:
                # TODO: Call the search_anime function instead
                #search.search_url(self)
                pass

            if iad_status is True:
                json_to_tabular(self, include_all_details=True)
            else:
                json_to_tabular(self, include_all_details=False)

        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText("Select any Image or Enter any URL to search")
            dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
            button = dlg.exec()

            if button == QMessageBox.StandardButton.Ok:
                pass
            else:
                pass
