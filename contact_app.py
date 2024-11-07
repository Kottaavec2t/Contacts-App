import sys
import sqlite3
import datetime
from PyQt5.QtWidgets import *

# ===========================================================================================================
#                               CONNECTION A LA BASE DE DONNEE "contacts.db"
# ===========================================================================================================


def create_connection():
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INT,
            firstname STR,
            name STR,
            phone_number STR,
            email STR,
            birthdate INT
        )
    ''')
    conn.commit()
    return conn


# ===========================================================================================================
#                                           CLASS ContactApp
# ===========================================================================================================


class ContactApp(QMainWindow):
    def __init__(self):
        super().__init__()


        # ===========================================================================================================
        #                               INITIALISATION DE LA ZONE D'AJOUT D'UN CONTACT
        # ===========================================================================================================


        self.conn = create_connection()
        self.setWindowTitle("Contacts")
        self.setGeometry(300, 200, 400, 400)
        self.setMaximumSize(400, 400)
        self.setMinimumSize(400, 400)

        self.layout_principal = QVBoxLayout()
        
        #First Name
        self.firstname_input = QLineEdit()
        self.firstname_input.setPlaceholderText("First Name")
        self.layout_principal.addWidget(self.firstname_input)

        #Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")
        self.layout_principal.addWidget(self.name_input)

        #Phone Number
        self.phone_number_layout = QVBoxLayout()
        self.layout_principal.addLayout(self.phone_number_layout)

        self.phone_number_input = QLineEdit()
        self.phone_number_input.setPlaceholderText("Phone Number")
        self.layout_principal.addWidget(self.phone_number_input)

        #Email
        self.email_layout = QVBoxLayout()
        self.layout_principal.addLayout(self.email_layout)

        self.remove_email_button = QPushButton("Remove Email")
        self.remove_email_button.clicked.connect(self._remove_email)

        self.add_email_button = QPushButton("Add Email")
        self.add_email_button.clicked.connect(self._add_email)
        self.email_layout.addWidget(self.add_email_button)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("you@example.com")

        #Birth Date
        self.birthdate_layout = QVBoxLayout()
        self.layout_principal.addLayout(self.birthdate_layout)
        
        self.dateedit = QDateEdit()

        self.remove_birthdate_button = QPushButton("Remove Birth Date")
        self.remove_birthdate_button.clicked.connect(self._remove_birthdate)

        self.add_birthdate_button = QPushButton("Add Birth Date")
        self.add_birthdate_button.clicked.connect(self._add_birthdate)
        self.birthdate_layout.addWidget(self.add_birthdate_button)

        #Add Contact
        self.add_button = QPushButton("Add Contact")
        self.add_button.clicked.connect(self.add_contact)
        self.layout_principal.addWidget(self.add_button)

        container = QWidget()
        container.setLayout(self.layout_principal)
        self.setCentralWidget(container)


    # ===========================================================================================================
    #                                               FONCTIONS
    # ===========================================================================================================


    def _remove_email(self):

        self.email_layout.removeWidget(self.email_input)
        self.email_input.deleteLater()
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("you@example.com")
        
        self.email_layout.removeWidget(self.remove_email_button)
        self.remove_email_button.deleteLater()
        self.remove_email_button = QPushButton("Remove Email")
        self.remove_email_button.clicked.connect(self._remove_email)

        self.email_layout.addWidget(self.add_email_button)

    def _add_email(self):

        self.email_layout.removeWidget(self.add_email_button)
        self.add_email_button.deleteLater()
        self.add_email_button = QPushButton("Add Email")
        self.add_email_button.clicked.connect(self._add_email)

        self.email_layout.addWidget(self.email_input)
        self.email_layout.addWidget(self.remove_email_button)

    def _remove_birthdate(self):
         self.birthdate_layout.removeWidget(self.remove_birthdate_button)
         self.remove_birthdate_button.deleteLater()
         self.remove_birthdate_button = QPushButton("Remove Birth Date")
         self.remove_birthdate_button.clicked.connect(self._remove_birthdate)

         self.birthdate_layout.removeWidget(self.dateedit)
         self.dateedit.deleteLater()
         self.dateedit = QDateEdit()

         self.birthdate_layout.addWidget(self.add_birthdate_button)

    def _add_birthdate(self):
         self.birthdate_layout.removeWidget(self.add_birthdate_button)
         self.add_birthdate_button.deleteLater()
         self.add_birthdate_button = QPushButton("Add Birth Date")
         self.add_birthdate_button.clicked.connect(self._add_birthdate)

         self.birthdate_layout.addWidget(self.dateedit)
         self.birthdate_layout.addWidget(self.remove_birthdate_button)

    def add_contact(self):
        firstname = self.firstname_input.text()
        name = self.name_input.text()
        phone_number = self.phone_number_input.text()
        email = self.email_input.text()
        birthdate = self.dateedit.date().toPyDate()

        if firstname != " " and phone_number != " ":
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO contacts (firstname, name, phone_number, email, birthdate) VALUES (?, ?, ?, ?, ?)", (firstname, name, phone_number, email, birthdate))
            self.conn.commit()
            QMessageBox.information(self, "Succes !", f"Succefully add {firstname} {name} to your contacts.")
            self.firstname_input.clear()
            self.name_input.clear()
            self.phone_number_input.clear()
            self._remove_email()
            self._remove_birthdate()
            self.load_contacts()
        else:
             if phone_number != "": QMessageBox.warning(self, "Error", "You need to enter a First Name")
             elif firstname != "": QMessageBox.warning(self, "Error", "You need to enter a Phone Number")
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