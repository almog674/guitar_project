from .auth import Auth

from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QGroupBox, QLineEdit, QToolButton
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QIcon, QPixmap
from ..gui_helper import Gui_Helper
from global_state import Global_State

from ..style import *
import random


class Signup(Auth):
    def __init__(self, width, height):
        super().__init__(width=width, height=height)
        self.UI()

    #################### Sing Up Page #####################
    def UI(self):
        self.main_page, self.main_page_box = Gui_Helper.make_layout_full(
            background, self.width(), self.height())

        self.sing_up_Widgets()
        self.sing_up_layouts()

    def make_singup_avatar(self):
        number = random.randint(1, 4)
        label = QLabel()
        label.setPixmap(QPixmap(f'assets/undraw-{number}.svg'))
        label.setStyleSheet(singup_avatar())
        return label

    def make_singup_mini_profile(self):
        profile = QLabel('Profile')
        profile.setPixmap(QPixmap('assets/headphone_image.png'))
        profile.setAlignment(Qt.AlignHCenter)
        profile.setFixedSize(100, 100)
        return profile

    def sing_up_Widgets(self):
        ### Right Side Widget ###
        self.sing_up_title = QLabel('Create New User')
        self.sing_up_title.setAlignment(Qt.AlignHCenter)
        self.sing_up_title.setStyleSheet(title())

        self.sing_up_username_field = QHBoxLayout()
        self.sing_up_username_field_box = QGroupBox()
        self.sing_up_username_field_box.setStyleSheet(login_feild())
        self.sing_up_username_field_box.setFixedSize(300, 40)
        self.sing_up_username_field_box.setLayout(self.sing_up_username_field)

        self.sing_up_email_field = QHBoxLayout()
        self.sing_up_email_field_box = QGroupBox()
        self.sing_up_email_field_box.setStyleSheet(login_feild())
        self.sing_up_email_field_box.setFixedSize(300, 40)
        self.sing_up_email_field_box.setLayout(self.sing_up_email_field)

        self.sing_up_password_field = QHBoxLayout()
        self.sing_up_password_field_box = QGroupBox()
        self.sing_up_password_field_box.setStyleSheet(login_feild())
        self.sing_up_password_field_box.setFixedSize(300, 40)
        self.sing_up_password_field_box.setLayout(self.sing_up_password_field)

        self.sing_up_pre_password_field = QHBoxLayout()
        self.sing_up_pre_password_field_box = QGroupBox()
        self.sing_up_pre_password_field_box.setStyleSheet(login_feild())
        self.sing_up_pre_password_field_box.setFixedSize(300, 40)
        self.sing_up_pre_password_field_box.setLayout(
            self.sing_up_pre_password_field)

        self.sing_up_authentication = QPushButton('Sing Up')
        self.sing_up_authentication.setCursor(Qt.PointingHandCursor)
        self.sing_up_authentication.setFixedSize(300, 40)
        # self.sing_up_authentication.clicked.connect(self.create_user_db)
        self.sing_up_authentication.setStyleSheet(login_submit_button())

        self.sing_up_return_button = QPushButton(
            'Already have a user? go to login')
        self.sing_up_return_button.setCursor(Qt.PointingHandCursor)
        self.sing_up_return_button.setStyleSheet(bottom_label())
        # self.sing_up_return_button.clicked.connect(lambda: self.go_to_page(0))

        ### Sing Up Fields Widgets ###
        self.singup_username_line_edit = QLineEdit()
        self.singup_username_line_edit.setPlaceholderText('Username')
        self.singup_username_line_edit.setStyleSheet(login_field())
        self.singup_username_icon = QToolButton()
        self.singup_username_icon.setStyleSheet(field_icon())
        self.singup_username_icon.setDisabled(True)
        self.singup_username_icon.setIcon(QIcon('assets/user-solid.svg'))

        self.singup_email_line_edit = QLineEdit()
        self.singup_email_line_edit.setPlaceholderText('Email')
        self.singup_email_line_edit.setStyleSheet(login_field())
        self.singup_email_icon = QToolButton()
        self.singup_email_icon.setStyleSheet(field_icon())
        self.singup_email_icon.setDisabled(True)
        self.singup_email_icon.setIcon(QIcon('assets/user-solid.svg'))

        self.singup_password_line_edit = QLineEdit()
        self.singup_password_line_edit.setPlaceholderText('password')
        self.singup_password_line_edit.setEchoMode(QLineEdit.Password)
        self.singup_password_line_edit.setStyleSheet(login_field())
        self.singup_password_icon = QToolButton()
        self.singup_password_icon.setStyleSheet(field_icon())
        self.singup_password_icon.setDisabled(True)
        self.singup_password_icon.setIcon(QIcon('assets/lock-solid.svg'))

        self.singup_prepasswprd_line_edit = QLineEdit()
        self.singup_prepasswprd_line_edit.setPlaceholderText(
            'Validate Password')
        self.singup_prepasswprd_line_edit.setStyleSheet(login_field())
        self.singup_prepasswprd_line_edit.setEchoMode(QLineEdit.Password)
        self.singup_prepasswprd_icon = QToolButton()
        self.singup_prepasswprd_icon.setStyleSheet(field_icon())
        self.singup_prepasswprd_icon.setDisabled(True)
        self.singup_prepasswprd_icon.setIcon(QIcon('assets/lock-solid.svg'))

        ### Left Side Widgets ###
        self.singup_avatar = self.make_singup_avatar()

    def sing_up_layouts(self):
        ##### Sing Up Layouts #####
        self.content_part, self.content_part_box = Gui_Helper.make_layout_full(
            background, self.width(), Global_State.HEIGHT - 75, direction=1)
        self.content_part_box.setObjectName('main_page_box')
        self.content_part_box.setAlignment(Qt.AlignCenter)

        self.guitar_image = self.create_image()

        self.singup_layout = QHBoxLayout()
        self.singup_layout.setAlignment(Qt.AlignCenter)

        self.singup_layout_box = QGroupBox()
        self.singup_layout_box.setStyleSheet(login_layout_box())
        self.singup_layout_box.setFixedSize(650, 450)
        self.singup_layout_box.setLayout(self.singup_layout)

        self.sing_up_left = QVBoxLayout()
        self.sing_up_right = QVBoxLayout()

        ### Create The Right Part ###
        self.sing_up_title_section = QVBoxLayout()
        self.sing_up_form_section = QVBoxLayout()
        self.sing_up_bottom_section = QVBoxLayout()

        ### Create The Left Part ###
        self.sing_up_left.addWidget(self.singup_avatar)

        ### Create The Fields ###

        ### Adding the nested Layouts ###
        self.main_page.addWidget(self.singup_layout_box)

        self.singup_layout.addLayout(self.sing_up_left, 50)
        self.singup_layout.addLayout(self.sing_up_right, 50)

        self.sing_up_right.addLayout(self.sing_up_title_section, 20)
        self.sing_up_right.addLayout(self.sing_up_form_section, 60)
        self.sing_up_right.addLayout(self.sing_up_bottom_section, 20)

        # Right Part #
        self.sing_up_title_section.addStretch()
        self.sing_up_title_section.addWidget(self.sing_up_title)
        self.sing_up_title_section.addStretch()

        self.sing_up_form_section.addStretch()
        self.sing_up_form_section.addWidget(self.sing_up_username_field_box)
        self.sing_up_form_section.addStretch()
        self.sing_up_form_section.addWidget(self.sing_up_email_field_box)
        self.sing_up_form_section.addStretch()
        self.sing_up_form_section.addWidget(self.sing_up_password_field_box)
        self.sing_up_form_section.addStretch()
        self.sing_up_form_section.addWidget(
            self.sing_up_pre_password_field_box)
        self.sing_up_form_section.addStretch()
        self.sing_up_form_section.addWidget(self.sing_up_authentication)
        self.sing_up_right.addStretch()

        self.sing_up_bottom_section.addStretch()
        self.sing_up_bottom_section.addWidget(self.sing_up_return_button)
        self.sing_up_bottom_section.addStretch()

        self.sing_up_username_field.addWidget(self.singup_username_icon)
        self.sing_up_username_field.addWidget(self.singup_username_line_edit)

        self.sing_up_email_field.addWidget(self.singup_email_icon)
        self.sing_up_email_field.addWidget(self.singup_email_line_edit)

        self.sing_up_password_field.addWidget(self.singup_password_icon)
        self.sing_up_password_field.addWidget(self.singup_password_line_edit)

        self.sing_up_pre_password_field.addWidget(self.singup_prepasswprd_icon)
        self.sing_up_pre_password_field.addWidget(
            self.singup_prepasswprd_line_edit)

        self.content_part.addWidget(self.singup_layout_box)

        self.main_page.addWidget(self.content_part_box)
        self.main_page.addWidget(self.guitar_image)
