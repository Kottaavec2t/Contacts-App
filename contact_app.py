import sys
import sqlite3
import datetime
from PyQt5.QtWidgets import *

def create_connection():
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INT,
            first_name STR,
            name STR,
            phone_number STR,
            email_adress STR,
            birthdate INT
        )
    ''')
    conn.commit()
    return conn

class ContactApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.visible = True

        self.conn = create_connection()
        self.setWindowTitle("Contacts")
        self.setGeometry(300, 200, 400, 400)
        self.setMaximumSize(400, 400)
        self.setMinimumSize(400, 400)

        self.layout_principal = QVBoxLayout()
        
        #First Name
        self.firstname_input = QLineEdit()
        self.firstname_input.setPlaceholderText("Name")
        self.layout_principal.addWidget(self.firstname_input)

        #Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")
        self.layout_principal.addWidget(self.name_input)

        #Phone Number
        self.phone_number_input = QLineEdit()
        self.phone_number_input.setPlaceholderText("Phone Number")
        self.layout_principal.addWidget(self.phone_number_input)

        #Email
        self.email_layout = QVBoxLayout()
        self.layout_principal.addLayout(self.email_layout)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email Adress")
        self.layout_principal.addWidget(self.email_input)

        #Birth Date
        self.birthdate_layout = QVBoxLayout()
        self.layout_principal.addLayout(self.birthdate_layout)
        
        self.dateedit = QDateEdit()

        self.remove_birthdate_button = QPushButton("Remove Birth Date")
        self.remove_birthdate_button.clicked.connect(self.remove_birthdate)

        self.add_birthdate_button = QPushButton("Add Birth Date")
        self.add_birthdate_button.clicked.connect(self.add_birthdate)
        self.birthdate_layout.addWidget(self.add_birthdate_button)

        #Ad Contact
        self.add_button = QPushButton("Add Contact")
        self.add_button.clicked.connect(self.add_contact)
        self.layout_principal.addWidget(self.add_button)

        container = QWidget()
        container.setLayout(self.layout_principal)
        self.setCentralWidget(container)

    def remove_birthdate(self):
         self.birthdate_layout.removeWidget(self.remove_birthdate_button)
         self.remove_birthdate_button.deleteLater()
         self.remove_birthdate_button = QPushButton("Remove Birth Date")
         self.remove_birthdate_button.clicked.connect(self.remove_birthdate)
         self.birthdate_layout.removeWidget(self.dateedit)
         self.dateedit.deleteLater()
         self.dateedit = QDateEdit()
         self.birthdate_layout.addWidget(self.add_birthdate_button)

    def add_birthdate(self):
         self.birthdate_layout.removeWidget(self.add_birthdate_button)
         self.add_birthdate_button.deleteLater()
         self.add_birthdate_button = QPushButton("Add Birth Date")
         self.add_birthdate_button.clicked.connect(self.add_birthdate)
         self.birthdate_layout.addWidget(self.dateedit)
         self.birthdate_layout.addWidget(self.remove_birthdate_button)

    def add_contact(self):
        name = self.name_input.text()
        phone_number = self.phone_number_input.text()
        email_adress = self.email_input.text()

        self.load_contacts()
    
    def delete_contact(self):
         pass
    
    def load_contacts(self):
         self.contact_list = QListWidget()
         self.contact_list.clear()
         cursor = self.conn.cursor()
         cursor.execute("SELECT * FROM contacts")
         contacts = cursor.fetchall()

         for contact in contacts:
              self.contact_list.addItem(f"{contact[1]} - {contact[2]}")
        
         self.layout_principal.addWidget(self.contact_list)
    def closeEvent(self, event):
            self.conn.close()
            event.accept()
            
app = QApplication(sys.argv)
fenetre = ContactApp()
fenetre.show()
sys.exit(app.exec_())