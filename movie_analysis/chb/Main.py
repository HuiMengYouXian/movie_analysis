import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from main_view import Ui_MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)  # 新建一个QT应用
    win = QMainWindow()  # 新建一个QT窗口
    ui_main = Ui_MainWindow()  # 创建生成的UI主窗口对象
    ui_main.setupUi(win)  # 设置在主窗口上显示UI控件
    win.show()  # 显示窗口
    sys.exit(app.exec_())