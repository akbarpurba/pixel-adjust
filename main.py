import sys
from ui_main import ImageEditor
from PyQt5.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    window = ImageEditor()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()