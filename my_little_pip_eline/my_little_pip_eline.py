"""
This is the main function of the my_little_pipeline program. It calls the main windows and necessary widgets

Classes: MainWindow(QMainWindow)
Functions:
initialize_user_interface(self)
create_menubar(self)
__create_menubar_item(self, text: str, action, shortcut_key: str = None,
                              icon: QIcon = None, checkable: bool = False, tip: str = None) -> QAction
__fill_menu(menu, items: list) -> None
create_dock_widgets(self)
open_pipeline(self)
save_pipeline(self)
clear_pipeline(self)
switch_screen_display(self, state)
closeEvent(self, event)

TODO :
- Figure out the Mac laptop touchpad problem (qt.pointer.dispatch: delivering touch release to same window QWindow(0x0)
not QWidgetWindow(0x6000014804e0, name="MainWindowClassWindow"))
"""

# import necessary modules
import sys
from PyQt6.QtWidgets import QApplication, QMessageBox, QMainWindow, QDockWidget, QStatusBar
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction
from bin.pip_gui.PipelineWidget import PipelineWidgetView
from bin.pip_gui.ThumbnailWidget import ThumbnailWidget


class MainWindow(QMainWindow):

    def __init__(self):
        """
        Create the main windows for the application
        """
        super().__init__()

        # Set window basic information (size, name, ...)
        desktop = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(int(desktop.width()/4), int(desktop.height()/4),
                         int(desktop.width()/2), int(desktop.height()/2))

        self.full_screen_act = None

        self.setWindowTitle("My little Problem Inverse Pipeline (PIP.eline)")

        # Initialize thumbnail, pipeline_view (main widget)
        self.thumbnail = ThumbnailWidget()
        self.pipeline_view = PipelineWidgetView()

        # Set other class parameter
        self.dock_widget = None

        # Allow mouse tracking
        self.setMouseTracking(True)

        # Initialize Graphic User Interface element
        self.initialize_user_interface()

    def initialize_user_interface(self):
        """
        Initialize the window with main widget (self.pipeline_view), dock widgets, menu bar and status bar
        """
        # Create Main widget for pipeline
        self.setCentralWidget(self.pipeline_view)

        # Create Dock widget for thumbnail
        self.create_dock_widgets()

        # Create Menubar
        self.create_menubar()

        # Create Status bar
        self.setStatusBar(QStatusBar(self))

    def create_menubar(self):
        """
         Initialize the menubar
        """
        # Create menubar
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        # Create actions for file menu : New, Open, Save, Exit
        file_action_list = [
            self.__create_menubar_item('New', self.clear_pipeline, 'Ctrl+N'),
            None,
            self.__create_menubar_item('Open', self.open_pipeline, 'Ctrl+O'),
            self.__create_menubar_item('Save', self.save_pipeline, 'Ctrl+S'),
            None,
            self.__create_menubar_item('Exit', self.close, 'Ctrl+Q')]

        # Create actions for view menu
        self.full_screen_act = self.__create_menubar_item('Full Screen', self.switch_screen_display, shortcut_key=None,
                                                          icon=None, checkable=True, tip="Change screen display")

        # Create file menu and add actions
        file_menu = menu_bar.addMenu('File')
        self.__fill_menu(file_menu, file_action_list)

        # Create view menu and add actions
        view_menu = menu_bar.addMenu('View')
        self.__fill_menu(view_menu, [self.dock_widget.toggleViewAction()])

    def __create_menubar_item(self, text: str, action, shortcut_key: str = None,
                              icon: QIcon = None, checkable: bool = False, tip: str = None) -> QAction:
        """Private function that create a menubar item
        :param text: name of the item displayed in the menu
        :type text: str
        :param action: function performed when the user clic on the item
        :type action: Union(None, Bool)
        :param shortcut_key: String with shortcut key for menubar item
            default: None
        :type shortcut_key: str
        :param icon: Icon for the menubar item
            default: None
        :type shortcut_key: QIcon
        :param checkable: Make the menubar item checkable
            default: False
        :type shortcut_key: bool
        :param tip: Tip to display on the status bar with mouse hover over the menubar item
            default: None
        :type shortcut_key: str
        :return: The object QAction that we can insert in the menubar
        :rtype: QAction
        """
        if icon is None:
            menubar_item = QAction(text, self)
        else:
            menubar_item = QAction(icon, text, self)

        if shortcut_key is not None:
            menubar_item.setShortcut(shortcut_key)

        if checkable:
            menubar_item.isCheckable()

        menubar_item.setStatusTip(tip)

        menubar_item.triggered.connect(action)

        return menubar_item

    @staticmethod
    def __fill_menu(menu, items: list) -> None:
        """Private static function that fill a menubar with menubar item list. A None element in the list makes a
        separator.
        :param menu: The menu object to fill
        :type menu: Any
        :param items: list with the different menubar items
        :type items: list
        """
        for item in items:
            if item is None:
                menu.addSeparator()
            else:
                menu.addAction(item)

    def create_dock_widgets(self):
        """
        Function to initialize the docked widget (thumbnail of icon)
        """
        self.dock_widget = QDockWidget()
        self.dock_widget.setWindowTitle('Functions')
        self.dock_widget.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)

        self.dock_widget.setWidget(self.thumbnail)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock_widget)

    def open_pipeline(self):
        """
        TODO: Open a pipeline
        """
        pass

    def save_pipeline(self):
        """
        TODO: Save a pipeline
        """
        pass

    def clear_pipeline(self):
        """
        If the new button is clicked, display dialog asking user if
        they want to clear the pipeline view.
        """
        answer = QMessageBox.question(self, "Clear pipeline",
                                      "Do you want to delete your pipeline?",
                                      QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes,
                                      QMessageBox.StandardButton.Yes)
        if answer == QMessageBox.StandardButton.Yes:
            self.pipeline_view.scene.clear()

    def switch_screen_display(self, state):
        """
        If state is True, then display the main window in full screen.
        Otherwise, return the window to normal.
        """
        if state:
            self.showFullScreen()
        else:
            self.showNormal()

    def closeEvent(self, event):
        """
        Overwrite closing windows event to ask confirmation
        :param event: Closing Event
        """
        answer = QMessageBox.question(self, "Close App",
                                      "Do you want to close my little PIP.eline?",
                                      QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes,
                                      QMessageBox.StandardButton.Yes)
        if answer == QMessageBox.StandardButton.Yes:
            event.accept()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
