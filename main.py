"""PySide6 WebEngineWidgets Example"""

import sys
from bookmarkwidget import BookmarkWidget
from browsertabwidget import BrowserTabWidget
from downloadwidget import DownloadWidget
from findtoolbar import FindToolBar
from webengineview import WebEngineView
from PySide6 import QtCore
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QAction, QKeySequence, QIcon
from PySide6.QtWidgets import (QApplication, QDockWidget, QLabel,
                               QLineEdit, QMainWindow, QToolBar)
from PySide6.QtWebEngineCore import QWebEngineDownloadRequest, QWebEnginePage

main_windows = []


def create_main_window():
    """Creates a MainWindow using 75% of the available screen resolution."""
    main_win = webBrowser()
    main_windows.append(main_win)
    available_geometry = main_win.screen().availableGeometry()
    main_win.resize(available_geometry.width() * 2 / 3,
                    available_geometry.height() * 2 / 3)
    main_win.show()
    return main_win


def create_main_window_with_browser():
    """Creates a MainWindow with a BrowserTabWidget."""
    main_win = create_main_window()
    return main_win.add_browser_tab()


class webBrowser(QMainWindow):
    """Provides the parent window that includes the BookmarkWidget,
    BrowserTabWidget, and a DownloadWidget, to offer the complete
    web browsing experience."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle('lamon internet')
        self.setWindowIcon(QIcon('lemon.png'))

        self._tab_widget = BrowserTabWidget(create_main_window_with_browser)
        self._tab_widget.enabled_changed.connect(self._enabled_changed)
        self._tab_widget.download_requested.connect(self._download_requested)
        self.setCentralWidget(self._tab_widget)
        self.connect(self._tab_widget, QtCore.SIGNAL("url_changed(QUrl)"),
                     self.url_changed)

        self._bookmark_dock = QDockWidget()
        self._bookmark_dock.setWindowTitle('Bookmarks')
        self._bookmark_widget = BookmarkWidget()
        self._bookmark_widget.open_bookmark.connect(self.load_url)
        self._bookmark_widget.open_bookmark_in_new_tab.connect(self.load_url_in_new_tab)
        self._bookmark_dock.setWidget(self._bookmark_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._bookmark_dock)

        self._find_tool_bar = None

        self._actions = {}
        self._create_menu()

        self._tool_bar = QToolBar()
        self.addToolBar(self._tool_bar)
        for action in self._actions.values():
            if not action.icon().isNull():
                self._tool_bar.addAction(action)

        self._addres_line_edit = QLineEdit()
        self._addres_line_edit.setClearButtonEnabled(True)
        self._addres_line_edit.returnPressed.connect(self.load)
        self._tool_bar.addWidget(self._addres_line_edit)
        self._tool_bar.addWidget(self.menu)
        self._zoom_label = QLabel()
        self.statusBar().addPermanentWidget(self._zoom_label)
        self._update_zoom_label()

        self._bookmarksToolBar = QToolBar()
        self.addToolBar(Qt.TopToolBarArea, self._bookmarksToolBar)
        self.insertToolBarBreak(self._bookmarksToolBar)
        self._bookmark_widget.changed.connect(self._update_bookmarks)
        self._update_bookmarks()

    def _update_bookmarks(self):
        self._bookmark_widget.populate_tool_bar(self._bookmarksToolBar)
        self._bookmark_widget.populate_other(self.file_menu, 34)

    def _create_menu(self):
        self.menu=self.menuBar()
        self.file_menu = self.menu.addMenu("&⁝")
        exit_action = QAction(QIcon.fromTheme("application-exit"), "E&xit",
                              self, shortcut="Ctrl+Q", triggered=QApplication.quit)
        self.file_menu.addAction(exit_action)

        style_icons = ':/qt-project.org/styles/commonstyle/images/'
        back_action = QAction(QIcon.fromTheme("go-previous",
                                              QIcon(style_icons + 'left-32.png')),
                              "Back", self,
                              shortcut=QKeySequence(QKeySequence.Back),
                              triggered=self._tab_widget.back)
        self._actions[QWebEnginePage.Back] = back_action
        back_action.setEnabled(False)
        self.file_menu.addAction(back_action)
        forward_action = QAction(QIcon.fromTheme("go-next",
                                                 QIcon(style_icons + 'right-32.png')),
                                 "Forward", self,
                                 shortcut=QKeySequence(QKeySequence.Forward),
                                 triggered=self._tab_widget.forward)
        forward_action.setEnabled(False)
        self._actions[QWebEnginePage.Forward] = forward_action

        self.file_menu.addAction(forward_action)
        reload_action = QAction(QIcon(style_icons + 'refresh-32.png'),
                                "Reload", self,
                                shortcut="Ctrl+R",
                                triggered=self._tab_widget.reload)
        self._actions[QWebEnginePage.Reload] = reload_action
        reload_action.setEnabled(False)
        self.file_menu.addAction(reload_action)

        self.file_menu.addSeparator()

        new_tab_action = QAction("New Tab", self,
                                 shortcut='Ctrl+T',
                                 triggered=self.add_browser_tab)
        self.file_menu.addAction(new_tab_action)

        close_tab_action = QAction("Close Current Tab", self,
                                   shortcut="Ctrl+W",
                                   triggered=self._close_current_tab)
        self.file_menu.addAction(close_tab_action)

        self.file_menu.addSeparator()

        history_action = QAction("History...", self,
                                 triggered=self._tab_widget.show_history)
        self.file_menu.addAction(history_action)
        self.file_menu.addSeparator()

        find_action = QAction("Find", self,
                              shortcut=QKeySequence(QKeySequence.Find),
                              triggered=self._show_find)
        self.file_menu.addAction(find_action)

        self.file_menu.addSeparator()
        undo_action = QAction("Undo", self,
                              shortcut=QKeySequence(QKeySequence.Undo),
                              triggered=self._tab_widget.undo)
        self._actions[QWebEnginePage.Undo] = undo_action
        undo_action.setEnabled(False)
        self.file_menu.addAction(undo_action)

        redo_action = QAction("Redo", self,
                              shortcut=QKeySequence(QKeySequence.Redo),
                              triggered=self._tab_widget.redo)
        self._actions[QWebEnginePage.Redo] = redo_action
        redo_action.setEnabled(False)
        self.file_menu.addAction(redo_action)

        self.file_menu.addSeparator()

        cut_action = QAction("Cut", self,
                             shortcut=QKeySequence(QKeySequence.Cut),
                             triggered=self._tab_widget.cut)
        self._actions[QWebEnginePage.Cut] = cut_action
        cut_action.setEnabled(False)
        self.file_menu.addAction(cut_action)

        copy_action = QAction("Copy", self,
                              shortcut=QKeySequence(QKeySequence.Copy),
                              triggered=self._tab_widget.copy)
        self._actions[QWebEnginePage.Copy] = copy_action
        copy_action.setEnabled(False)
        self.file_menu.addAction(copy_action)

        paste_action = QAction("Paste", self,
                               shortcut=QKeySequence(QKeySequence.Paste),
                               triggered=self._tab_widget.paste)
        self._actions[QWebEnginePage.Paste] = paste_action
        paste_action.setEnabled(False)
        self.file_menu.addAction(paste_action)

        self.file_menu.addSeparator()

        select_all_action = QAction("Select All", self,
                                    shortcut=QKeySequence(QKeySequence.SelectAll),
                                    triggered=self._tab_widget.select_all)
        self._actions[QWebEnginePage.SelectAll] = select_all_action
        select_all_action.setEnabled(False)
        self.file_menu.addAction(select_all_action)
        self.file_menu.addSeparator()

        add_bookmark_action = QAction("&Add Bookmark", self,
                                      triggered=self._add_bookmark)
        self.file_menu.addAction(add_bookmark_action)
        add_tool_bar_bookmark_action = QAction("&Add Bookmark to Tool Bar", self,
                                               triggered=self._add_tool_bar_bookmark)
        self.file_menu.addAction(add_tool_bar_bookmark_action)
        self.file_menu.addSeparator()

        download_action = QAction("Open Downloads", self,
                                  triggered=DownloadWidget.open_download_directory)
        self.file_menu.addAction(download_action)
        self.file_menu.addSeparator()

        self.file_menu.addAction(self._bookmark_dock.toggleViewAction())

        self.file_menu.addSeparator()

        zoom_in_action = QAction(QIcon.fromTheme("zoom-in"),
                                 "Zoom In", self,
                                 shortcut=QKeySequence(QKeySequence.ZoomIn),
                                 triggered=self._zoom_in)
        self.file_menu.addAction(zoom_in_action)
        zoom_out_action = QAction(QIcon.fromTheme("zoom-out"),
                                  "Zoom Out", self,
                                  shortcut=QKeySequence(QKeySequence.ZoomOut),
                                  triggered=self._zoom_out)
        self.file_menu.addAction(zoom_out_action)

        reset_zoom_action = QAction(QIcon.fromTheme("zoom-original"),
                                    "Reset Zoom", self,
                                    shortcut="Ctrl+0",
                                    triggered=self._reset_zoom)
        self.file_menu.addAction(reset_zoom_action)
        self.file_menu.addSeparator()
        about_action = QAction("About Qt", self,
                               shortcut=QKeySequence(QKeySequence.HelpContents),
                               triggered=QApplication.aboutQt)
        self.file_menu.addAction(about_action)

    def add_browser_tab(self):
        return self._tab_widget.add_browser_tab()

    def _close_current_tab(self):
        if self._tab_widget.count() > 1:
            self._tab_widget.close_current_tab()
        else:
            self.close()

    def close_event(self, event):
        main_windows.remove(self)
        event.accept()

    def load(self):
        url_string = self._addres_line_edit.text().strip()
        if url_string:
            self.load_url_string(url_string)

    def load_url_string(self, url_s):
        url = QUrl.fromUserInput(url_s)
        if (url.isValid()):
            self.load_url(url)

    def load_url(self, url):
        self._tab_widget.load(url)

    def load_url_in_new_tab(self, url):
        self.add_browser_tab().load(url)

    def url_changed(self, url):
        self._addres_line_edit.setText(url.toString())

    def _enabled_changed(self, web_action, enabled):
        action = self._actions[web_action]
        if action:
            action.setEnabled(enabled)

    def _add_bookmark(self):
        index = self._tab_widget.currentIndex()
        if index >= 0:
            url = self._tab_widget.url()
            title = self._tab_widget.tabText(index)
            icon = self._tab_widget.tabIcon(index)
            self._bookmark_widget.add_bookmark(url, title, icon)

    def _add_tool_bar_bookmark(self):
        index = self._tab_widget.currentIndex()
        if index >= 0:
            url = self._tab_widget.url()
            title = self._tab_widget.tabText(index)
            icon = self._tab_widget.tabIcon(index)
            self._bookmark_widget.add_tool_bar_bookmark(url, title, icon)

    def _zoom_in(self):
        new_zoom = self._tab_widget.zoom_factor() * 1.5
        if (new_zoom <= WebEngineView.maximum_zoom_factor()):
            self._tab_widget.set_zoom_factor(new_zoom)
            self._update_zoom_label()

    def _zoom_out(self):
        new_zoom = self._tab_widget.zoom_factor() / 1.5
        if (new_zoom >= WebEngineView.minimum_zoom_factor()):
            self._tab_widget.set_zoom_factor(new_zoom)
            self._update_zoom_label()

    def _reset_zoom(self):
        self._tab_widget.set_zoom_factor(1)
        self._update_zoom_label()

    def _update_zoom_label(self):
        percent = int(self._tab_widget.zoom_factor() * 100)
        self._zoom_label.setText(f"{percent}%")

    def _download_requested(self, item):
        # Remove old downloads before opening a new one
        for old_download in self.statusBar().children():
            if (type(old_download).__name__ == 'DownloadWidget' and
                old_download.state() != QWebEngineDownloadRequest.DownloadInProgress):
                self.statusBar().removeWidget(old_download)
                del old_download

        item.accept()
        download_widget = DownloadWidget(item)
        download_widget.remove_requested.connect(self._remove_download_requested,
                                                 Qt.QueuedConnection)
        self.statusBar().addWidget(download_widget)

    def _remove_download_requested(self):
            download_widget = self.sender()
            self.statusBar().removeWidget(download_widget)
            del download_widget

    def _show_find(self):
        if self._find_tool_bar is None:
            self._find_tool_bar = FindToolBar()
            self._find_tool_bar.find.connect(self._tab_widget.find)
            self.addToolBar(Qt.BottomToolBarArea, self._find_tool_bar)
        else:
            self._find_tool_bar.show()
        self._find_tool_bar.focus_find()

    def write_bookmarks(self):
        self._bookmark_widget.write_bookmarks()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = create_main_window()
    initial_urls = sys.argv[1:]
    if not initial_urls:
        initial_urls.append('http://google.com')
    for url in initial_urls:
        main_win.load_url_in_new_tab(QUrl.fromUserInput(url))
    exit_code = app.exec()
    main_win.write_bookmarks()
    sys.exit(exit_code)