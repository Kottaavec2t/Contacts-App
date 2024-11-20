import sys
import sqlite3
import datetime
from PyQt5.QtWidgets import *
from PyQt5 import sip
from PyQt5.QtCore import Qt


def createConnection():
    '''
    Function to connect to the database or create one if not exist.

    :return: `Connection`
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
            birthdate DATE,
            notes STR
        )
    ''')
    conn.commit()
    return conn

def hideAllWidgetLayout(cur_lay):
    '''
    Function to hide all widgets in the given layout.

    :param cur_lay: QLayout(), the layout containing the widgets to hide.
    :return: None
    '''
    if cur_lay is not None:
        for i in range(cur_lay.count()):
            item = cur_lay.itemAt(i)
            widget = item.widget()
            if widget is not None:
                widget.hide()
            elif item.layout() is not None:
                hideAllWidgetLayout(item.layout())

class ContactApp(QMainWindow):
    

    def __init__(self):
        super().__init__()

        self.conn = createConnection()
        self.setWindowTitle("Contacts")
        self.setGeometry(300, 200, 400, 600)
        self.setMaximumSize(400, 600)
        self.setMinimumSize(400, 600)

        self.layout_principal = QVBoxLayout()

        container = QWidget()
        container.setLayout(self.layout_principal)
        self.setCentralWidget(container)


        # ===========================================================================================================
        #              CREATE ALL THE WIDGETS AND HIDE THEM (BE SURE THERE ARE IN THE ORDER YOU WANT)
        # ===========================================================================================================
        

        #------------------------Contact List------------------------
        self.contact_list = QListWidget()
        self.layout_principal.addWidget(self.contact_list)
        self.contact_list.hide()

        #------------------------First Name Input------------------------
        self.firstname_input = QLineEdit()
        self.firstname_input.setPlaceholderText("First Name")
        self.layout_principal.addWidget(self.firstname_input)
        self.firstname_input.hide()

        #------------------------Last Name Input------------------------
        self.lastname_input = QLineEdit()
        self.lastname_input.setPlaceholderText("Name")
        self.layout_principal.addWidget(self.lastname_input)
        self.lastname_input.hide()

        #------------------------Phone Number Input------------------------
        self.phone_number_input = QLineEdit()
        self.phone_number_input.setPlaceholderText("Phone Number")
        self.layout_principal.addWidget(self.phone_number_input)
        self.phone_number_input.hide()

        #------------------------Email Input------------------------
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("you@example.com")
        self.layout_principal.addWidget(self.email_input)
        self.email_input.hide()

        #------------------------Remove Email Button------------------------
        self.remove_email_button = QPushButton("Remove Email")
        self.remove_email_button.clicked.connect(lambda: self.changeVisibilityOfOptionalOption('email', False))
        self.layout_principal.addWidget(self.remove_email_button)
        self.remove_email_button.hide()

        #------------------------Add Email Button------------------------
        self.add_email_button = QPushButton("Add Email")
        self.add_email_button.clicked.connect(lambda: self.changeVisibilityOfOptionalOption('email', True))
        self.layout_principal.addWidget(self.add_email_button)
        self.add_email_button.hide()

        #------------------------Birthdate Input------------------------
        self.birthdate_dateedit = QDateEdit()
        self.layout_principal.addWidget(self.birthdate_dateedit)
        self.birthdate_dateedit.hide()

        #------------------------Remove Birthdate Button------------------------
        self.remove_birthdate_button = QPushButton("Remove Birth Date")
        self.remove_birthdate_button.clicked.connect(lambda: self.changeVisibilityOfOptionalOption('birthdate', False))
        self.layout_principal.addWidget(self.remove_birthdate_button)
        self.remove_birthdate_button.hide()

        #------------------------Add Birthdate Button------------------------
        self.add_birthdate_button = QPushButton("Add Birth Date")
        self.add_birthdate_button.clicked.connect(lambda: self.changeVisibilityOfOptionalOption('birthdate', True))
        self.layout_principal.addWidget(self.add_birthdate_button)
        self.add_birthdate_button.hide()
        
        #------------------------Notes Input------------------------
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Notes")
        self.layout_principal.addWidget(self.notes_input)
        self.notes_input.hide()

        #------------------------Add Contact Button------------------------
        self.add_button = QPushButton("✅ Add Contact")
        self.add_button.clicked.connect(self.addContact)
        self.layout_principal.addWidget(self.add_button)
        self.add_button.hide()

        #------------------------New Contact Button------------------------
        self.save_changes_button = QPushButton("💾 Save Changes")
        self.layout_principal.addWidget(self.save_changes_button)
        self.save_changes_button.hide()

        #------------------------Edit Contact Button------------------------
        self.edit_contact_button = QPushButton("✏️ Edit Contact")
        self.edit_contact_button.clicked.connect(self.editContact)
        self.layout_principal.addWidget(self.edit_contact_button)
        self.save_changes_button.hide()

        #------------------------New Contact Button------------------------
        self.new_contact_button = QPushButton("➕ New Contact")
        self.new_contact_button.clicked.connect(self.addContactMenu)
        self.layout_principal.addWidget(self.new_contact_button)
        self.save_changes_button.hide()

        #------------------------Cancel Button------------------------
        self.cancel_button = QPushButton("❌ Cancel")
        self.cancel_button.clicked.connect(self.loadContacts)
        self.layout_principal.addWidget(self.cancel_button)
        self.cancel_button.hide()

        self.loadContacts()


    # ===========================================================================================================
    #                                               FONCTIONS
    # ===========================================================================================================


    def addContactMenu(self):
        
        self.firstname_input.show()
        self.lastname_input.show()
        self.phone_number_input.show()
        self.add_birthdate_button.show()
        self.add_email_button.show()
        self.notes_input.show()
        self.add_button.show()
        self.cancel_button.show()

        self.new_contact_button.hide()
        self.edit_contact_button.hide()
        self.contact_list.hide()

    def changeVisibilityOfOptionalOption(self, field_type, visible):
        '''
        Function to change the visiblility of the field type define in input.

        :param: `field_type`, str, 'email' or 'birthdate' depend of the option you want to change the visibility.
        :param: `visible`, bool, True if you want to see the input or False if not.
        :return: `None`
        '''

        if field_type == 'email':
            self.email_input.setVisible(visible)
            self.remove_email_button.setVisible(visible)
            self.add_email_button.setVisible(not visible)

        if field_type == 'birthdate':
            self.birthdate_dateedit.setVisible(visible)
            self.remove_birthdate_button.setVisible(visible)
            self.add_birthdate_button.setVisible(not visible)

    def addContact(self):
        
        # Collect data
        firstname = self.firstname_input.text()
        name = self.lastname_input.text()
        phone_number = self.phone_number_input.text().strip()
        email = self.email_input.text().strip()
        birthdate = None if not self.birthdate_dateedit.isVisible() else self.birthdate_dateedit.date().toPyDate()
        notes = self.notes_input.toPlainText()

        # Validate fields
        if not firstname:
            QMessageBox.warning(self, "Input Error", "First name is required.")
            return

        if not phone_number.isdigit() or len(phone_number) != 10 or phone_number[0] != '0':
            QMessageBox.warning(self, "Input Error", "Invalid phone number format.")
            return
        
        # Remove the birthdate if self.birthdate_dateedit() is not visible
        birthdate = self.birthdate_dateedit.date().toPyDate()
        if not self.birthdate_dateedit.isVisible():
             birthdate = 0

        # Get, Add, Commit, Inform
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO contacts (firstname, name, phone_number, email, birthdate, notes) VALUES (?, ?, ?, ?, ?, ?)", 
                       (firstname, name, phone_number, email, birthdate, notes)
                       )
        self.conn.commit()
        QMessageBox.information(self, "Succes !", f"Succefully add {firstname} {name} to your contacts.")
        
        self.firstname_input.clear()
        self.lastname_input.clear()
        self.phone_number_input.clear()
        self.email_input.clear()
        
        self.changeVisibilityOfOptionalOption('email', False)
        self.changeVisibilityOfOptionalOption('birthdate', False)
        
        self.loadContacts()
    
    def editContact(self):

        # Get the selected item
        item = self.contact_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Edit Contact", "No contact selected!")
            return

        # Retrieve the unique ID stored in the item
        contact_id = item.data(32)

        # Fetch the contact from the database using the ID
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
        contact = cursor.fetchone()
        if not contact:
            QMessageBox.critical(self, "Error", "Failed to find contact in the database!")
            return

        # Update and show all inputs
        hideAllWidgetLayout(self.layout_principal)

        self.firstname_input.setText(contact[1])
        self.firstname_input.show()

        self.lastname_input.setText(contact[2])
        self.lastname_input.show()

        self.phone_number_input.setText(f"0{str(contact[3])}")
        self.phone_number_input.show()

        self.email_input.setText(contact[4] if contact[4] else "")
        self.email_input.show()
        
        self.birthdate_dateedit.setCalendarPopup(True)
        if contact[5] and contact[5] != 0:
            self.birthdate_dateedit.setDate(datetime.datetime.strptime(contact[5], "%Y-%m-%d"))
            self.changeVisibilityOfOptionalOption('birthdate', True)
        else:
            self.changeVisibilityOfOptionalOption('birthdate', False)

        self.notes_input.show()
        self.notes_input.setText(contact[6])

        self.save_changes_button.clicked.connect(lambda: self.saveContactChanges(contact_id))
        self.save_changes_button.show()

        self.cancel_button.show()
    
    def saveContactChanges(self, contact_id):

        # Collect updated data
        firstname = self.firstname_input.text().strip()
        name = self.lastname_input.text().strip()
        phone_number = self.phone_number_input.text().strip()
        email = self.email_input.text().strip()
        birthdate = self.birthdate_dateedit.date().toPyDate()

        # Validation
        if not firstname:
            QMessageBox.warning(self, "Input Error", "First name is required.")
            return

        if not phone_number.isdigit() or len(phone_number) != 10 or phone_number[0] != '0':
            QMessageBox.warning(self, "Input Error", "Invalid phone number format.")
            return
            
        # Update the database
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE contacts SET firstname = ?, name = ?, phone_number = ?, email = ?, birthdate = ? WHERE id = ?",
                (firstname, name, phone_number, email, birthdate, contact_id)
            )
            self.conn.commit()
            QMessageBox.information(self, "Success", "Contact updated successfully!")
            self.loadContacts()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to update contact: {e}")
    
    def deleteContact(self):
         pass
    
    def loadContacts(self):
       
        hideAllWidgetLayout(self.layout_principal)
        self.contact_list.clear()

        # Get contacts from the database
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM contacts")
        contacts = cursor.fetchall()

        # Add a new Item for every contact
        for contact in contacts:
            item_text = f"{contact[1]} {contact[2]}\n0{contact[3]}"
            item = QListWidgetItem(item_text)
            item.setData(32, contact[0])
            self.contact_list.addItem(item)

        # Show widgets
        self.contact_list.show()
        self.edit_contact_button.show()
        self.new_contact_button.show()
        
    def closeEvent(self, event):
            self.conn.close()
            event.accept()


app = QApplication(sys.argv)
fenetre = ContactApp()
fenetre.show()
sys.exit(app.exec_())
