import sys
import sqlite3
import datetime
from PyQt5.QtWidgets import *
from PyQt5 import sip
from PyQt5.QtCore import Qt


def create_connection():

    '''function to connect to the database or create one if not exist.

    :return: Connection
    '''
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname TEXT NOT NULL,
            name TEXT NOT NULL,
            phone_number STR,
            email STR,
            birthdate DATE
            notes STR
        )
    ''')
    conn.commit()
    return conn


# ===========================================================================================================
#                                          ContactApp() CLASS
# ===========================================================================================================


class ContactApp(QMainWindow):
    

    def __init__(self):
        super().__init__()

        self.conn = create_connection()
        self.setWindowTitle("Contacts")
        self.setGeometry(300, 200, 400, 600)
        self.setMaximumSize(400, 600)
        self.setMinimumSize(400, 600)

        self.layout_principal = QVBoxLayout()

        self.load_contacts()

        container = QWidget()
        container.setLayout(self.layout_principal)
        self.setCentralWidget(container)


    # ===========================================================================================================
    #                                               FONCTIONS
    # ===========================================================================================================


    def add_contact_menu(self):
        
        #First Name
        self.firstname_input = QLineEdit()
        self.firstname_input.setPlaceholderText("First Name")
        self.layout_principal.addWidget(self.firstname_input, 1)

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
        self.remove_email_button.clicked.connect(self.remove_email)

        self.add_email_button = QPushButton("Add Email")
        self.add_email_button.clicked.connect(self.add_email)
        self.email_layout.addWidget(self.add_email_button)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("you@example.com")

        #Birth Date
        self.birthdate_layout = QVBoxLayout()
        self.layout_principal.addLayout(self.birthdate_layout)
        
        self.dateedit = QDateEdit()

        self.remove_birthdate_button = QPushButton("Remove Birth Date")
        self.remove_birthdate_button.clicked.connect(self.remove_birthdate)

        self.add_birthdate_button = QPushButton("Add Birth Date")
        self.add_birthdate_button.clicked.connect(self.add_birthdate)
        self.birthdate_layout.addWidget(self.add_birthdate_button)

        #Notes
        self.text_box = QTextEdit()
        self.text_box.setPlaceholderText("Notes")
        self.layout_principal.addWidget(self.text_box)

        #Add Contact Button
        self.add_button = QPushButton("Add Contact")
        self.add_button.clicked.connect(self.add_contact)
        self.layout_principal.addWidget(self.add_button)

        #Remove New Contact Button and Contacts List and Edit Contact Button
        self.layout_principal.removeWidget(self.new_contact_button)
        self.new_contact_button.deleteLater()
        self.layout_principal.removeWidget(self.edit_contact_button)
        self.edit_contact_button.deleteLater()
        self.layout_principal.removeWidget(self.contact_list)
        self.contact_list.deleteLater()


    def remove_email(self):

        self.email_layout.removeWidget(self.email_input)
        self.email_input.deleteLater()
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("you@example.com")
        
        self.email_layout.removeWidget(self.remove_email_button)
        self.remove_email_button.deleteLater()
        self.remove_email_button = QPushButton("Remove Email")
        self.remove_email_button.clicked.connect(self.remove_email)

        self.email_layout.addWidget(self.add_email_button)

    def add_email(self):

        self.email_layout.removeWidget(self.add_email_button)
        self.add_email_button.deleteLater()
        self.add_email_button = QPushButton("Add Email")
        self.add_email_button.clicked.connect(self.add_email)

        self.email_layout.addWidget(self.email_input)
        self.email_layout.addWidget(self.remove_email_button)


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

         self.dateedit = QDateEdit()
         self.birthdate_layout.addWidget(self.dateedit)
         self.birthdate_layout.addWidget(self.remove_birthdate_button)


    def add_contact(self):
        firstname = self.firstname_input.text()
        name = self.name_input.text()
        phone_number = self.phone_number_input.text().strip()
        email = self.email_input.text().strip()
        birthdate = None if not self.dateedit.isVisible() else self.dateedit.date().toPyDate()
        notes = self.text_box.toPlainText()

        #Validate fields
        if not firstname:
            QMessageBox.warning(self, "Input Error", "First name is required.")
            return

        if not phone_number.isdigit() or len(phone_number) != 10 or phone_number[0] != '0':
            QMessageBox.warning(self, "Input Error", "Invalid phone number format.")
            return
        
        #Remove the birthdate if self.dateedit() is'nt visible
        birthdate = self.dateedit.date().toPyDate()
        if not self.dateedit.isVisible():
             birthdate = 0

        if firstname != "" and phone_number != None:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO contacts (firstname, name, phone_number, email, birthdate, notes) VALUES (?, ?, ?, ?, ?)", (firstname, name, phone_number, email, birthdate, notes))
            self.conn.commit()
            QMessageBox.information(self, "Succes !", f"Succefully add {firstname} {name} to your contacts.")
            self.firstname_input.clear()
            self.name_input.clear()
            self.phone_number_input.clear()
            self.remove_email()
            self.remove_birthdate()
            self.load_contacts()
        else:
             if firstname == "": QMessageBox.warning(self, "Missing First Name", "You forgot to enter a first name.")
             elif phone_number != None: QMessageBox.warning(self, "Invalid Phone Number", "Please check if the phone number is write correctly.")
    
    def edit_contact(self):

        #Get the selected item
        item = self.contact_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Edit Contact", "No contact selected!")
            return

        #Retrieve the unique ID stored in the item
        contact_id = item.data(32)

        #Fetch the contact from the database using the ID
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
        contact = cursor.fetchone()
        if not contact:
            QMessageBox.critical(self, "Error", "Failed to find contact in the database!")
            return

        #Clear main layout and create edit form
        self.clear_layout(self.layout_principal)

        #First Name
        self.firstname_input = QLineEdit()
        self.firstname_input.setPlaceholderText("First Name")
        self.firstname_input.setText(contact[1])
        self.layout_principal.addWidget(self.firstname_input)

        #Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Last Name")
        self.name_input.setText(contact[2])
        self.layout_principal.addWidget(self.name_input)

        #Phone Number
        self.phone_number_input = QLineEdit()
        self.phone_number_input.setPlaceholderText("Phone Number")
        phone_number_text = f"0{str(contact[3])}"
        self.phone_number_input.setText(phone_number_text)
        self.layout_principal.addWidget(self.phone_number_input)

        #Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setText(contact[4] if contact[4] else "")
        self.layout_principal.addWidget(self.email_input)

        # Birth Date
        self.dateedit = QDateEdit()
        self.dateedit.setCalendarPopup(True)
        if contact[5] and contact[5] != 0:
            self.dateedit.setDate(datetime.datetime.strptime(contact[5], "%Y-%m-%d"))
            self.birthdate_layout = QVBoxLayout()

            self.layout_principal.addLayout(self.birthdate_layout)

            self.birthdate_layout.addWidget(self.dateedit)

            self.remove_birthdate_button = QPushButton("Remove Birth Date")
            self.remove_birthdate_button.clicked.connect(self.remove_birthdate)
            self.birthdate_layout.addWidget(self.remove_birthdate_button)

            self.add_birthdate_button = QPushButton("Add Birth Date")
            self.add_birthdate_button.clicked.connect(self.add_birthdate)
        else:
            self.birthdate_layout = QVBoxLayout()

            self.layout_principal.addLayout(self.birthdate_layout)

            self.remove_birthdate_button = QPushButton("Remove Birth Date")
            self.remove_birthdate_button.clicked.connect(self.remove_birthdate)

            self.add_birthdate_button = QPushButton("Add Birth Date")
            self.add_birthdate_button.clicked.connect(self.add_birthdate)
            self.birthdate_layout.addWidget(self.add_birthdate_button)

        # Save Changes Button
        self.save_changes_button = QPushButton("Save Changes")
        self.save_changes_button.clicked.connect(lambda: self.save_contact_changes(contact_id))
        self.layout_principal.addWidget(self.save_changes_button)

        # Cancel Button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.load_contacts)
        self.layout_principal.addWidget(self.cancel_button)
    
    def save_contact_changes(self, contact_id):

        #Collect updated data
        firstname = self.firstname_input.text().strip()
        name = self.name_input.text().strip()
        phone_number = self.phone_number_input.text().strip()
        email = self.email_input.text().strip()
        birthdate = self.dateedit.date().toPyDate()

        #Validation
        if not firstname:
            QMessageBox.warning(self, "Input Error", "First name is required.")
            return

        if not phone_number.isdigit() or len(phone_number) != 10 or phone_number[0] != '0':
            QMessageBox.warning(self, "Input Error", "Invalid phone number format.")
            return

        #Update the database
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE contacts SET firstname = ?, name = ?, phone_number = ?, email = ?, birthdate = ? WHERE id = ?",
                (firstname, name, phone_number, email, birthdate, contact_id)
            )
            self.conn.commit()
            QMessageBox.information(self, "Success", "Contact updated successfully!")
            self.load_contacts()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to update contact: {e}")
    
    def delete_contact(self):
         pass
    
    def load_contacts(self):
         layout = self.layout_principal
         self.clear_layout(layout)
         self.contact_list = QListWidget()
         self.contact_list.clear()
         cursor = self.conn.cursor()
         cursor.execute("SELECT * FROM contacts")
         contacts = cursor.fetchall()

         for contact in contacts:
            item_text = f"{contact[1]} {contact[2]}\n0{contact[3]}"
            item = QListWidgetItem(item_text)
            item.setData(32, contact[0])
            self.contact_list.addItem(item)
        
         self.layout_principal.addWidget(self.contact_list)

         self.edit_contact_button = QPushButton("✏️ Edit Contact")
         self.edit_contact_button.clicked.connect(self.edit_contact)
         self.layout_principal.addWidget(self.edit_contact_button)

         self.new_contact_button = QPushButton("➕ New Contact")
         self.new_contact_button.clicked.connect(self.add_contact_menu)
         self.layout_principal.addWidget(self.new_contact_button)


    def clear_layout(self, cur_lay):
        if cur_lay is not None:
            while cur_lay.count():
                item = cur_lay.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())
        

    def closeEvent(self, event):
            self.conn.close()
            event.accept()


app = QApplication(sys.argv)
fenetre = ContactApp()
fenetre.show()
sys.exit(app.exec_())