"""Graphical User Interface for the project."""

# --- PyQt Compatibility Layer -------------------------------------------------
try:
    from PyQt6.QtCore import QSize
    from PyQt6.QtGui import QIcon
    from PyQt6.QtWidgets import (
        QApplication,
        QCheckBox,
        QFileDialog,
        QHBoxLayout,
        QLabel,
        QLineEdit,
        QMainWindow,
        QMessageBox,
        QPushButton,
        QSizePolicy,
        QSpacerItem,
        QStackedWidget,
        QTextEdit,
        QVBoxLayout,
        QWidget,
    )

    QT_API = 6
except ImportError:
    try:
        from PyQt5.QtCore import QSize
        from PyQt5.QtGui import QIcon
        from PyQt5.QtWidgets import (
            QApplication,
            QCheckBox,
            QFileDialog,
            QHBoxLayout,
            QLabel,
            QLineEdit,
            QMainWindow,
            QMessageBox,
            QPushButton,
            QSizePolicy,
            QSpacerItem,
            QStackedWidget,
            QTextEdit,
            QVBoxLayout,
            QWidget,
        )

        QT_API = 5
    except ImportError:
        try:
            from PyQt4.QtCore import QSize
            from PyQt4.QtGui import (
                QApplication,
                QCheckBox,
                QFileDialog,
                QHBoxLayout,
                QIcon,
                QLabel,
                QLineEdit,
                QMainWindow,
                QMessageBox,
                QPushButton,
                QSizePolicy,
                QSpacerItem,
                QStackedWidget,
                QTextEdit,
                QVBoxLayout,
                QWidget,
            )

            QT_API = 4
        except ImportError:
            raise ImportError(
                "No PyQt bindings could be found. Please install PyQt4 or newer:"
                "\n- For PyQt4: See manual installation instructions"
                "\n- For PyQt5: pip install AnimeSnap[qt5]"
                "\n- For PyQt6: pip install AnimeSnap[qt6]"
            )
# ------------------------------------------------------------------------------

QApplication = QApplication

import mimetypes
import webbrowser

from qdarkstyle import load_stylesheet  # type: ignore

from AnimeSnap.consts import (
    AUTHOR,
    GITHUB,
    HEIGHT,
    ICON_SIZE,
    ICONS_PATH,
    PACKAGE,
    TWITTER_LINK,
    WIDTH,
    X,
    Y,
)
from AnimeSnap.consts import __desc__ as DESC
from AnimeSnap.consts import __version__ as VERSION
from AnimeSnap.json_operations import json_to_tabular, save_to_json
from AnimeSnap.search import search_anime


def get_open_file_name(
    parent: QWidget,
    title: str,
    directory: str,
    file_filter: str,
    options=None,
) -> str:
    """Cross-version QFileDialog.getOpenFileName"""
    if QT_API >= 5:
        file_path, _ = QFileDialog.getOpenFileName(
            parent=parent,
            caption=title,
            directory=directory,
            filter=file_filter,
            options=options or QFileDialog.Option.ReadOnly,
        )
        return file_path
    else:  # PyQt4
        return QFileDialog.getOpenFileName(parent, title, directory, file_filter)


def get_save_file_name(
    parent: QWidget,
    title: str,
    directory: str,
    file_filter: str,
):
    """Cross-version QFileDialog.getSaveFileName"""
    if QT_API >= 5:
        file_path, _ = QFileDialog.getSaveFileName(
            parent=parent,
            caption=title,
            directory=directory,
            filter=file_filter,
        )
        return file_path, _
    else:  # PyQt4
        return QFileDialog.getSaveFileName(parent, title, directory, file_filter)


def get_image_extensions() -> list:
    """
    Returns a list of common image file extensions.
    """
    image_extensions = []
    for ext, mime in mimetypes.types_map.items():
        if mime.startswith("image/"):
            image_extensions.append("*" + ext)
    return sorted(image_extensions)


class Window(QMainWindow):
    """
    Graphical User Interface for the AnimeSnap project.

    This class provides the main user interface for the AnimeSnap application.
    It includes methods for switching between the main menu and results views,
    searching for anime information, and displaying results in a user-friendly
    format. Additional methods offer functionality to interact with the UI,
    manage themes, and open social media links.

    Attributes:
        current_page (QWidget): The current page of the application.
        result (dict): The JSON result from the API.
        stacked_widget (QStackedWidget): The stacked widget.

    Methods:
        get_image_extensions(): Get a list of valid image extensions for file filters.
        social_media_links(layout): Create buttons to open social media links in the UI.
        open_github(): Open the GitHub repository in the default web browser.
        open_twitter(): Open the Twitter link in the default web browser.
        show_about(): Display an about message with application details.
        show_help(): Display a help message with instructions on how to use the application.
        create_main_menu_widget(): Create the main menu widget with user interface elements.
        create_result_widget(): Create the result widget for displaying search results.
        resize_to_main_menu(): Adjust the window size and title for the main menu.
        resize_to_result_page(): Adjust the window size and title for the results page.
        switch_to_page(page): Switch between main menu and results views.
        open_image(): Open a file dialog to select and set an image file.
        return_to_menu(): Return to the main menu view.
        on_click_theme_icon(): Toggle the dark and light themes.
        switch_theme_name(): Toggle between "dark" and "light" themes.
        on_click_search(): Perform an anime search based on user input.
        write_to_json(): Write the search result to a JSON file.
        run(): Run the application, displaying the main window and user interface.

    Args:
        QMainWindow (QMainWindow): The main window of the application.
    """

    def __init__(self) -> None:
        """Constructor of the class"""
        super().__init__()

        # Set the window icon
        icon_name = str(ICONS_PATH) + "/" + PACKAGE + ".ico"
        self.setWindowIcon(QIcon(icon_name))

        # Apply the dark theme stylesheet
        if QT_API >= 5:
            qt_api_name = "pyqt" + str(QT_API)
            self.setStyleSheet(load_stylesheet(qt_api=qt_api_name))
        else:
            self.setStyleSheet(load_stylesheet(pyside=False))

        self.ctheme = "dark"
        self.search_result = None

        # Create a stacked widget
        self.stacked_widget = QStackedWidget()

        # Create and add different pages (widgets) to the stacked widget
        self.main_menu_widget = self.create_main_menu_widget()
        self.result_widget = self.create_result_widget()

        # Add the pages to the stacked widget
        self.stacked_widget.addWidget(self.main_menu_widget)
        self.stacked_widget.addWidget(self.result_widget)

        # Set the stacked widget as central widget
        self.setCentralWidget(self.stacked_widget)

        # Set the current page to the main menu
        self.resize_to_main_menu()

    def social_media_links(self, layout: QVBoxLayout) -> None:
        """
        Create the social media links.

        Args:
            layout (QVBoxLayout): The layout to add the buttons to.
        """
        # Create a QPushButton for the GitHub button
        github_button = QPushButton()
        icon_name = str(ICONS_PATH) + "/github_logo.png"
        github_button.setIcon(QIcon(icon_name))
        github_button.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
        github_button.clicked.connect(self.open_github)

        # Create a QPushButton for the Telegram button
        telegram_button = QPushButton()
        icon_name = str(ICONS_PATH) + "/twitter_logo.png"
        telegram_button.setIcon(QIcon(icon_name))
        telegram_button.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
        telegram_button.clicked.connect(self.open_twitter)

        # Create buttons for "About" and "Help"
        about_button = QPushButton("About")
        help_button = QPushButton("Help")

        about_button.clicked.connect(self.show_about)
        help_button.clicked.connect(self.show_help)

        # Create a layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(github_button)
        button_layout.addStretch(1)  # Add space between buttons

        button_layout.addWidget(about_button)
        button_layout.addWidget(help_button)

        button_layout.addStretch(1)  # Add space between buttons
        button_layout.addWidget(telegram_button)

        # Add the button layout to the provided layout
        layout.addLayout(button_layout)

    @staticmethod
    def open_github() -> None:
        """Open the GitHub repository in the default browser."""
        webbrowser.open(GITHUB, new=1)

    @staticmethod
    def open_twitter() -> None:
        """Open the Twitter profile in the default browser."""
        webbrowser.open(TWITTER_LINK, new=1)

    def show_about(self) -> None:
        """Show the about message."""
        about_message = """\
{PACKAGE} - {DESC}\n
Version: {VERSION}\n
Author: {AUTHOR}\n
Website: https://www.animesnapapp.com""".format(
            PACKAGE=PACKAGE, DESC=DESC, VERSION=VERSION, AUTHOR=AUTHOR
        )

        QMessageBox.about(self, "About", about_message)

    def show_help(self) -> None:
        """Show the help message."""
        help_message = (
            "How to Use AnimeSnap:\n"
            "1. Enter the image URL or upload an image.\n"
            "2. Optionally, enter an Anilist Anime ID.\n"
            "3. Check 'Remove Black Borders' and 'Include All Details' as needed.\n"
            "4. Click the 'Search' button to start the search.\n\n"
            "AnimeSnap will provide you with detailed information about the scene!"
        )
        QMessageBox.information(self, "Help", help_message)

    def create_main_menu_widget(self) -> QWidget:
        """
        Create the main menu widget.

        Returns:
            QWidget: The main menu widget.
        """
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # Add a vertical spacer with a specified height (e.g., 20 pixels)
        if QT_API >= 5:
            spacer = QSpacerItem(
                20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
            )
        else:
            spacer = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout.addItem(spacer)

        theme = self.switch_theme_name()

        # Create a horizontal layout for the top of the window
        top_layout = QHBoxLayout()
        self.themes_button = QPushButton()
        icon_name = str(ICONS_PATH) + "/" + theme + ".png"
        self.themes_button.setIcon(QIcon(icon_name))
        self.themes_button.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
        self.themes_button.setFixedSize(ICON_SIZE, ICON_SIZE)
        self.themes_button.clicked.connect(self.on_click_theme_icon)
        top_layout.addStretch()
        top_layout.addWidget(self.themes_button)
        layout.addLayout(top_layout)

        # Create a horizontal layout for the image source
        button_layout = QHBoxLayout()

        layout.addItem(spacer)
        self.img_source_entry = QLineEdit(self)
        self.img_source_entry.setPlaceholderText("Enter image URL or Upload a image")
        button_layout.addWidget(self.img_source_entry)

        self.open_image_button = QPushButton()
        icon_name = str(ICONS_PATH) + "/folder.png"
        self.open_image_button.setIcon(QIcon(icon_name))
        self.open_image_button.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
        self.open_image_button.setFixedSize(ICON_SIZE, ICON_SIZE)
        self.open_image_button.clicked.connect(self.open_image)
        button_layout.addWidget(self.open_image_button)
        layout.addLayout(button_layout)  # Add the button layout to the main layout

        # Create a horizontal layout for the checkboxes
        checkbox_layout = QHBoxLayout()

        layout.addItem(spacer)
        layout.addLayout(checkbox_layout)  # Add the checkbox layout to the main layout

        self.checkbox_rbb = QCheckBox("Remove Black Borders")
        checkbox_layout.addWidget(self.checkbox_rbb)

        self.checkbox_iad = QCheckBox("Include All Details")
        checkbox_layout.addWidget(self.checkbox_iad)

        layout.addItem(spacer)

        layout.addWidget(QLabel("Anilist Anime ID [OPTIONAL] [https://anilist.co/]"))

        self.anilist_entry = QLineEdit(self)
        self.anilist_entry.setPlaceholderText(
            "Use this if you know what anime it is and you just need the scene details"
        )
        layout.addWidget(self.anilist_entry)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.on_click_search)
        layout.addWidget(search_button)

        layout.addItem(spacer)
        layout.addItem(spacer)

        self.social_media_links(layout)

        central_widget.setLayout(layout)
        return central_widget

    def create_result_widget(self) -> QWidget:
        """
        Create the result widget.

        Returns:
            QWidget: The result widget.
        """
        widget = QWidget()
        layout = QVBoxLayout()

        self.textbox = QTextEdit()
        self.textbox.setReadOnly(True)
        layout.addWidget(self.textbox)

        json_button = QPushButton("Write to JSON")
        json_button.clicked.connect(lambda: self.write_to_json())
        layout.addWidget(json_button)

        another_image_button = QPushButton("Search Another Image")
        another_image_button.clicked.connect(self.return_to_menu)
        layout.addWidget(another_image_button)

        widget.setLayout(layout)
        return widget

    def resize_to_main_menu(self) -> None:
        """Resize the window to the main menu."""
        self.setWindowTitle("AnimeSnap")
        self.setGeometry(X, Y, 450, 150)

    def resize_to_result_page(self) -> None:
        """Resize the window to the result page."""
        self.setWindowTitle("AnimeSnap - Results")
        self.setGeometry(X, Y, WIDTH, HEIGHT)

    def switch_to_page(self, page: QWidget) -> None:
        """Switch to the specified page.

        Args:
            page (QWidget): The page to switch to.
        """
        self.stacked_widget.setCurrentWidget(page)

        if page == self.result_widget:
            self.resize_to_result_page()
        else:
            self.resize_to_main_menu()

    def open_image(self) -> None:
        """Open a file dialog to select an image file."""
        extensions = " ".join(get_image_extensions())
        file_path = get_open_file_name(
            self,
            "Open Image to Search",
            "",
            "Images ({extensions})".format(extensions=extensions),
        )
        if file_path:
            self.img_source_entry.setText(file_path)

    def return_to_menu(self) -> None:
        """Return to the main menu."""
        self.switch_to_page(self.main_menu_widget)

        self.img_source_entry.clear()
        self.anilist_entry.clear()

    def on_click_theme_icon(self) -> None:
        """Switch the theme of the application."""
        # We set the icon to the opposite of the current theme
        icon_name = str(ICONS_PATH) + "/" + self.ctheme + ".png"
        self.themes_button.setIcon(QIcon(icon_name))
        self.ctheme = self.switch_theme_name()

        try:
            from qdarkstyle.light.palette import LightPalette
        except Exception:
            LightPalette = None

        if QT_API >= 5:
            palette = (
                LightPalette if (self.ctheme == "light" and LightPalette) else None
            )
            qt_api_name = "pyqt" + str(QT_API)
            self.setStyleSheet(load_stylesheet(palette=palette, qt_api=qt_api_name))
        else:
            self.setStyleSheet(load_stylesheet(pyside=False))

    def switch_theme_name(self) -> str:
        """
        Switch the theme name.

        Returns:
            str: The name of the theme.
        """
        return "light" if self.ctheme == "dark" else "dark"

    def on_click_search(self) -> None:
        """Conduct an anime search."""
        anilist_id = None
        if self.anilist_entry.text():
            try:
                anilist_id = int(self.anilist_entry.text())
            except ValueError:
                QMessageBox.critical(self, "Error", "Invalid Anilist ID")
                return

        iad_status = self.checkbox_iad.isChecked()
        img_source = self.img_source_entry.text()

        try:
            self.search_result = search_anime(img_source, anilist_id)["result"]
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return

        self.switch_to_page(self.result_widget)
        self.textbox.setPlainText(
            json_to_tabular(data=self.search_result, include_all_details=iad_status)
        )

    def write_to_json(self) -> None:
        """Write the JSON result to a file."""
        file_path, _ = get_save_file_name(
            self, "Save JSON File", "", "JSON Files (*.json);;All Files (*)"
        )
        if not file_path:
            return

        try:
            save_to_json(file_path, self.search_result)
            QMessageBox.information(
                self, "File Saved", "The file has been saved successfully."
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def run(self) -> None:
        """Run the application."""
        self.show()
        self.raise_()
        self.activateWindow()
