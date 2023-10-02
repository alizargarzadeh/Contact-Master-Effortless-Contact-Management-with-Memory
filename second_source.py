from tkinter import *
import re
import os.path
import tkinter.ttk as ttk
from tkinter import messagebox

class Contact:
    def __new__(cls, *args):
        obj = super().__new__(cls)
        obj.__firstName = None
        obj.__lastName = None
        obj.__phoneNumber = None
        obj.__email = None
        return obj

    @property
    def firstName(self):
        return self.__firstName

    @firstName.setter
    def firstName(self, value):
        if len(str(value)) > 0:
            self.__firstName = value

    @property
    def lastName(self):
        return self.__lastName

    @lastName.setter
    def lastName(self, value):
        if len(str(value)) > 0:
            self.__lastName = value

    @property
    def phoneNumber(self):
        return self.__phoneNumber

    @phoneNumber.setter
    def phoneNumber(self, value):
        if value=="" or value.isdigit():
            self.__phoneNumber = value
        else:
            raise InvalidNumber("Phone Number Must Be Digit.")          

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if value== "" or re.findall("\w+@{1}\w+.com{1}",value):
            self.__email = value
        else:
            raise InvalidEmail("Email Is Not Correct")

    def __init__(self, f, l, c=None, e=None):
        self.__firstName = f
        self.__lastName = l
        if c=="" or c.isdigit():
            self.__phoneNumber = c
        else:
            raise InvalidNumber("Phone Number Must Be Digit.")
        if  e == "" or re.findall("\w+@{1}\w+.com{1}",e):
            self.__email = e
        else:
            raise InvalidEmail("Email Is Not Correct")

    def match(self, filter):
        if filter in self.__firstName:
            return self.__firstName
        elif filter in self.__lastName:
            return self.__lastName
        elif filter in self.__phoneNumber:
            return self.__phoneNumber
        elif filter in self.__email:
            return self.__email
        else:
            return None
        
    def show(self):
        print(f"{self.__firstName}\t{self.__lastName}\t{self.__phoneNumber}\t{self.__email}")



class ContactBook():
    def __new__(cls, *args):
        obj = super().__new__(cls)
        obj.__contacts = None
        return obj

    @property
    def contacts(self):
        return self.__contacts

    def __init__(self):
        self.__contacts = []

    def show_all_contact(self):
        for contact in self.__contacts:
            contact.show()

    def add_contact(self, f,l,c=None,e=None):
            contact = Contact(f,l,c,e)
            self.__contacts.append(contact)

    def remove_contact(self, contact):
        self.__contacts.remove(contact)

    def search_contact(self, f):
        return [contact for contact in self.__contacts if contact.match(f)]

    def find_contact(self, f, l):
        for contact in self.__contacts:
            if contact.firstName == f and contact.lastName == l:
                return contact

    def save_phonebook(self):
        with open("MyPhoneBook", "w") as f1:
            for contact in self.__contacts:
                f1.write(f"{contact.firstName}\t")
                f1.write(f"{contact.lastName}\t")
                f1.write(f"{contact.phoneNumber}\t")
                f1.write(f"{contact.email}\t")
                f1.write(f"\n")

class GUI:
    def __new__(cls, *args):
        obj = super().__new__(cls)
        obj.my_phone_book = None
        obj.tree = None
        obj.ent_fName = None
        obj.ent_lName = None
        obj.ent_pNumber = None
        obj.ent_email = None
        obj.win_add = None
        obj.win_edit = None
        obj.ent_search = None
        obj.selected_contact = None
        obj.selected_contacts_details = None
        return obj

    def __init__(self,root):
        super().__init__()
        self.my_phone_book = ContactBook()
        self._create_window(root)
        self._load_data()

    def _create_window(self,root):
        root.title("Contact Book")
        root.resizable(width=False, height=False)
        root.config(bg="#F8F4EC")
        frm_title = Frame(root, bg="#F5DEB3")
        frm_title.pack(side=TOP, fill=X)
        frm_lbl = Label(frm_title, text="CONTACT BOOK")
        frm_lbl.config(font=("Times", 16, "bold"), bg="#F5DEB3", fg="#8B4513")
        frm_lbl.pack()

        frm_search = Frame(root, bg="#F8F4EC")
        frm_search.pack(side=TOP, fill=X, pady=10)
        self.ent_search = Entry(frm_search, width=35, font=("Times", 14))
        self.ent_search.pack(side=LEFT, padx=10)
        btn_cancel = Button(frm_search, text="\N{Cross Mark}", command=(self.restore))
        btn_cancel.pack(side=LEFT, padx=10)
        btn_search = Button(frm_search, text="\N{Right-Pointing Magnifying Glass}", font=("Times", 11))
        btn_search.config(bg="#7FFFD4", fg="black", command=self.search, padx=30,pady=2)
        btn_search.pack(side=LEFT, padx=10)

        frm_tableButton = Frame(root, width=1000, bg="#F8F4EC")
        frm_tableButton.pack(side=TOP)

        frm_table = Frame(frm_tableButton, width=800, bg="#F8F4EC")
        frm_table.pack(side=LEFT)

        frm_space = Frame(frm_tableButton, width=20, bg="#F8F4EC")
        frm_space.pack(side=LEFT)

        frm_button = Frame(frm_tableButton, width=60, bg="#F8F4EC")
        frm_button.pack(side=TOP)

    # Create buttons
        btn_add = Button(frm_button, text="Add", font=("Times", 12,"bold"))
        btn_add.config(fg="#000080", bg="white",command=(self.create_add_window), padx=36)
        btn_add.pack(pady=10, padx=20)

        btn_edit = Button(frm_button, text="Edit", font=("Times", 12,"bold"))
        btn_edit.config(fg="#00BFFF", bg="white",command=self.create_revise_window, padx=37)
        btn_edit.pack(pady=10, padx=20)

        btn_delete = Button(frm_button, text="Delete", font=("Times", 12,"bold"))
        btn_delete.config(fg="#FF4500", bg="white",command=self.delete, padx=30)
        btn_delete.pack(pady=10, padx=20)

    # Table
        scrollbar = Scrollbar(frm_table, orient=VERTICAL)
        self.tree = ttk.Treeview(frm_table, columns=("First name", "Last name", "Phone number", "Email"))
        self.tree.config(height=20, yscrollcommand=scrollbar.set, selectmode=BROWSE)
        self.tree.heading("#0", text="Id", anchor=CENTER)
        self.tree.heading("First name", text="First name", anchor=CENTER)
        self.tree.heading("Last name", text="Last name", anchor=CENTER)
        self.tree.heading("Phone number", text="Phone number", anchor=CENTER)
        self.tree.heading("Email", text="Email", anchor=CENTER)
        self.tree.column("#0", stretch=FALSE, minwidth=0, width=0)
        self.tree.column("#1", stretch=FALSE, minwidth=0, width=110)
        self.tree.column("#2", stretch=FALSE, minwidth=0, width=160)
        self.tree.column("#3", stretch=FALSE, minwidth=0, width=140)
        self.tree.column("#4", stretch=FALSE, minwidth=0, width=200)
        scrollbar.config(command=self.tree.yview)
        scrollbar.pack(side=RIGHT, fill=Y, pady=10)
        self.tree.pack(padx=10, pady=10)

    def _load_data(self):
        if os.path.exists("MyPhoneBook"):
            with open("MyPhoneBook", "r") as f1:
                for line in f1.readlines():
                    word = line.split("\t")
                    if len(word) == 2:
                        self.my_phone_book.add_contact(word[0], word[1])
                        self.tree.insert("", index=END, value=(
                            word[0], word[1]))
                    elif len(word) == 3:
                        if word[2].isdigit():
                            self.my_phone_book.add_contact(
                                word[0], word[1], word[2])
                            self.tree.insert("", index=END, value=(
                                word[0], word[1], word[2]))
                        else:
                            self.my_phone_book.add_contact(
                                word[0], word[1], None, word[2])
                            self.tree.insert("", index=END, value=(
                                word[0], word[1], None, word[2]))
                    else:
                        self.my_phone_book.add_contact(
                            word[0], word[1], word[2], word[3])
                        self.tree.insert("", index=END, value=(
                            word[0], word[1], word[2], word[3]))
        else:
            with open("MyPhoneBook", "w") as f1:
                f1.write("")

    def create_add_window(self):
        self.win_add = Toplevel()
        self.win_add.title("Add")
        self.win_add.resizable(0, 0)
        frm_content = Frame(self.win_add, bg="#E0FFFF")
        frm_content.grid(column=0, row=0)

        # Create labels
        lbl_title = Label(frm_content, text="Add Contact", font=(
            "Helvetica", 13), fg="#0000FF", bg="White")
        lbl_title.grid(column=0, row=0, columnspan=4, sticky=EW)
        lbl_fName = Label(frm_content, text="First name:", font=(
            "Helvetica", 13), fg="#0000FF", bg="#E0FFFF")
        lbl_fName.grid(column=0, row=1, sticky=E)
        lbl_lName = Label(frm_content, text="Last name:", font=(
            "Helvetica", 13), fg="#0000FF", bg="#E0FFFF")
        lbl_lName.grid(column=0, row=2, sticky=E)
        lbl_pNumber = Label(frm_content, text="Phone Number:", font=(
            "Helvetica", 13), fg="#0000FF", bg="#E0FFFF")
        lbl_pNumber.grid(column=0, row=3, sticky=E)
        lbl_email = Label(frm_content, text="Email:", font=(
            "Helvetica", 13), fg="#0000FF", bg="#E0FFFF")
        lbl_email.grid(column=0, row=4, sticky=E)

        # create entries
        self.ent_fName = Entry(frm_content, font=("Helvetica", 13))
        self.ent_fName.grid(column=1, row=1, columnspan=2)
        self.ent_lName = Entry(frm_content, font=("Helvetica", 13))
        self.ent_lName.grid(column=1, row=2, columnspan=2)
        self.ent_pNumber = Entry(frm_content, font=("Helvetica", 13))
        self.ent_pNumber.grid(column=1, row=3, columnspan=2)
        self.ent_email = Entry(frm_content, font=("Helvetica", 13))
        self.ent_email.grid(column=1, row=4, columnspan=2)

        # create button
        btn_save = Button(frm_content, text="save", font=(
            "Helvetica", 13), bg="#F0E68C", command=self.save)
        btn_save.grid(column=0, row=5, columnspan=3,
                           sticky=EW, padx=10, pady=10)

    def save(self):
        first_name = self.ent_fName.get()
        last_name = self.ent_lName.get()
        try:
            if first_name and last_name:
                phone_number = self.ent_pNumber.get()
                email = self.ent_email.get()
                if self.my_phone_book.find_contact(first_name, last_name):
                    raise AbortSave("This Contact has been saved already.")                                   
                self.my_phone_book.add_contact(first_name, last_name,
                                    phone_number, email)
                self.tree.insert("", index=END, value=(
                    first_name, last_name, phone_number, email))
                self.win_add.destroy()
            else:
                msg = messagebox.showinfo(
                    message="First Name and Last Name must be completed.", icon="warning")
        except AbortSave as text:
            messagebox.showerror(message=text)
        except InvalidNumber as text:
            messagebox.showerror(message=text)
        except InvalidEmail as text:
            messagebox.showerror(message=text)

    def delete(self):
        if self.tree.focus():
            msg = messagebox.askyesno(
                message="Are you sure you want to delete this contact?", icon="question")
            if msg:
                selected_details = self.tree.item(self.tree.focus())
                selected_contacts_details = selected_details["values"]
                tagert_contact = self.my_phone_book.find_contact(
                    selected_contacts_details[0], selected_contacts_details[1])
                self.my_phone_book.remove_contact(tagert_contact)
                self.tree.delete(self.tree.focus())

        else:
            msg = messagebox.showinfo(message="Nobody has been selected.", icon="warning",
                                      detail="(Please select a contact from the chart)")

    def create_revise_window(self):
        self.selected_contact = self.tree.focus()
        if self.selected_contact:
            selected_details = self.tree.item(self.selected_contact)
            self.selected_contacts_details = selected_details["values"]

            self.win_edit = Toplevel()
            self.win_edit.title("Edit")
            self.win_edit.resizable(0, 0)
            frm_content = Frame(self.win_edit, bg="#B0C4DE")
            frm_content.grid(column=0, row=0)

            # Create labels
            lbl_title = Label(frm_content, text="Edit Contact", font=(
                "Helvetica", 13), bg="#F0F8FF")
            lbl_title.grid(column=0, row=0, columnspan=4, sticky=EW)
            lbl_fName = Label(frm_content, text="First name:", font=(
                "Helvetica", 13), bg="#B0C4DE")
            lbl_fName.grid(column=0, row=1, sticky=E)
            lbl_lName = Label(frm_content, text="Last name:", font=(
                "Helvetica", 13), bg="#B0C4DE")
            lbl_lName.grid(column=0, row=2, sticky=E)
            lbl_pNumber = Label(
                frm_content, text="Phone Number:", font=("Helvetica", 13), bg="#B0C4DE")
            lbl_pNumber.grid(column=0, row=3, sticky=E)
            lbl_email = Label(frm_content, text="Email:", font=(
                "Helvetica", 13), bg="#B0C4DE")
            lbl_email.grid(column=0, row=4, sticky=E)

            # create entries
            self.ent_fName = Entry(frm_content, font=("Helvetica", 13))
            self.ent_fName.grid(column=1, row=1, columnspan=2)
            self.ent_fName.insert(0, self.selected_contacts_details[0])
            self.ent_lName = Entry(frm_content, font=("Helvetica", 13))
            self.ent_lName.grid(column=1, row=2, columnspan=2)
            self.ent_lName.insert(0, self.selected_contacts_details[1])
            self.ent_pNumber = Entry(frm_content, font=("Helvetica", 13))
            self.ent_pNumber.grid(column=1, row=3, columnspan=2)
            self.ent_pNumber.insert(0, self.selected_contacts_details[2])
            self.ent_email = Entry(frm_content, font=("Helvetica", 13))
            self.ent_email.grid(column=1, row=4, columnspan=2)
            self.ent_email.insert(0, self.selected_contacts_details[3])

            # create button
            btn_save = Button(frm_content, text="Update", font=(
                "Helvetica", 13), bg="#708090", fg="White", command=self.update)
            btn_save.grid(column=0, row=5, columnspan=3,
                               sticky=EW, padx=10, pady=10)
        else:
            msg = messagebox.showinfo(message="Nobody has been selected.", icon="warning",
                                      detail="(Please select a contact from the chart)")

    def update(self):
        first_name = self.ent_fName.get()
        last_name = self.ent_lName.get()
        phone_number = self.ent_pNumber.get()
        email = self.ent_email.get()
        tagert_contact = self.my_phone_book.find_contact(
            self.selected_contacts_details[0], self.selected_contacts_details[1])
        try:
            tagert_contact.firstName = first_name
            tagert_contact.lastName = last_name
            tagert_contact.phoneNumber = phone_number
            tagert_contact.email = email
            id = self.selected_contact[2:]
            self.tree.insert("", index=id, values=(
                first_name, last_name, phone_number, email))
            self.tree.delete(self.selected_contact)
            self.win_edit.destroy()
        except InvalidNumber as text:
            messagebox.showerror(message=text)
        except InvalidEmail as text:
            messagebox.showerror(message=text)

    def search(self):
        data = self.ent_search.get()
        contacts = self.my_phone_book.search_contact(data)
        if contacts != None:
            items = self.tree.get_children(item="")
            for item in items:
                self.tree.delete(item)
            for p in contacts:
                self.tree.insert("", index=END, value=(
                    p.firstName, p.lastName, p.phoneNumber, p.email))

    def restore(self):
        items = self.tree.get_children(item="")
        self.ent_search.delete(0, END)
        for item in items:
            self.tree.delete(item)
        for contact in self.my_phone_book.contacts:
            if contact.phoneNumber == None and contact.email == None:
                self.tree.insert("", index=END, value=(
                    contact.firstName, contact.lastName))
            elif contact.phoneNumber != None and contact.email == None:
                self.tree.insert("", index=END, value=(
                    contact.firstName, contact.lastName, contact.phoneNumber))
            elif contact.phoneNumber == None and contact.email != None:
                self.tree.insert("", index=END, value=(
                    contact.firstName, contact.lastName, None, contact.email))
            else:
                self.tree.insert("", index=END, value=(
                    contact.firstName, contact.lastName, contact.phoneNumber, contact.email))

    def __del__(self):
        self.my_phone_book.save_phonebook()


class InvalidNumber(Exception):
    pass

class InvalidEmail(Exception):
    pass

class AbortSave(Exception):
    pass