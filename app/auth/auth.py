from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from ..style import *
from global_state import Global_State
from ..gui_helper import Gui_Helper


class Auth(QWidget):
    def __init__(self, width, height):
        super().__init__()
        self.setFixedSize(width, height)
        self.setStyleSheet(background())
        self.create_image()

    #################### Dealing With Multiple Pages #####################
    def insert_page(self, widget, index=-1):
        self.page_system.insertWidget(index, widget)

    def go_to_page(self, number):
        self.page_system.setCurrentIndex(number)
    #################### Dealing With Multiple Pages #####################

    #################### Database Stuff #####################

    #################### Database Stuff #####################

    #################### Logistic Functions #####################
    def create_image(self):
        image_width = self.width()
        image_height = self.height() - Global_State.HEIGHT + 75
        guitar_picture = QLabel()
        pixmap = QPixmap('assets\\background-1.jpg')
        pixmap = pixmap.scaled(image_width, image_height)
        guitar_picture.setPixmap(pixmap)
        return guitar_picture

    def make_message_box(self, text):
        msg = QMessageBox()
        msg.setText(text)
        msg.setFixedSize(100, 100)
        msg.exec_()

    def clear_auth_fields(self):
        # Clear the fields of the singup and login #
        self.singup_username_line_edit.setText('')
        self.singup_email_line_edit.setText('')
        self.singup_password_line_edit.setText('')
        self.singup_prepasswprd_line_edit .setText('')

        self.user_field.setText('')
        self.password_field.setText('')
    #################### Logistic Functions #####################
