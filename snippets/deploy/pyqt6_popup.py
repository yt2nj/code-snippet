import os, sys

from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout


WINDOW_ICON_PATH = __file__.replace(".py", ".ico")
LAST_TIME_PATH = __file__.replace(".py", ".txt")


def read_last_time():
    if os.path.exists(LAST_TIME_PATH):
        with open(LAST_TIME_PATH, "r") as file:
            text = file.read(20)
        utc_datetime = QDateTime.fromString(text, Qt.DateFormat.ISODate)
        if utc_datetime.isValid():
            return utc_datetime
    return None


def write_this_time():
    utc_datetime = QDateTime.currentDateTimeUtc()
    with open(LAST_TIME_PATH, "w") as file:
        file.write(utc_datetime.toString(Qt.DateFormat.ISODate))


def get_secs_diff():
    last_time = read_last_time()
    if last_time is None:
        return 1024 * 1024
    this_time = QDateTime.currentDateTimeUtc()
    secs_diff = last_time.secsTo(this_time)
    return secs_diff


class ReminderText(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        if os.path.exists(WINDOW_ICON_PATH):
            self.setWindowIcon(QIcon(WINDOW_ICON_PATH))
        self.setWindowTitle("提醒休息")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)

        layout = QVBoxLayout()

        label = QLabel("[补水运动]\n[保护视力]")
        font = label.font()
        font.setFamily("SimSun")
        font.setBold(True)
        font.setPointSize(128)
        label.setFont(font)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(label)

        self.setLayout(layout)


def run_qt_app():
    app = QApplication([])
    win = ReminderText()
    win.show()
    app.exec()

    write_this_time()


if __name__ == "__main__":
    secs_diff = get_secs_diff()

    if secs_diff < 0 or secs_diff > 3456:
        run_qt_app()
