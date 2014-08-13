"""
Program to store and search commands and tricks, 
instead of constantly searching Stackoverflow for the same things

"""
__version__ = 0.1
__date__ = "August 2014"
__author__ = "alonsofonseca.angel@gmail.com"
__licence__  = "Public Domain"


import pyperclip

import sys

from ttk import Button, Entry, Frame, Label, Style
from Tkinter import BOTH, END, Listbox, Tk, Text
import tkMessageBox as box

# I'd say globals are the way to go this, but it's just that I am lazy 
entries_list = []
file_to_search = "/home/aaf/Dev/comm/commands.txt"

class CommandEntry(object):
    title = ""
    tags = ""
    text = ""

    # The class "constructor" - It's actually an initializer 
    def __init__(self, title, tags, text):
        self.title = title
        self.tags = tags
        self.text = text

""" ---------------------------------
    GUI part for the Command search
    ---------------------------------""" 

class CommSearch(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent        
        self.initUI()
        
    def initUI(self):
      
        self.parent.title("Search your command cards")
        self.style = Style()
        self.style.theme_use("default")        
        self.pack()
        
	self.input_title = Label(self, text="Enter your command below")
        self.input_title.grid(row=0, columnspan=2)
	self.input_box = Entry(self, width=90)
        self.input_box.grid(row=1, column=0)
        self.input_box.focus()
        self.input_box.bind("<Key>", self.onUpdateSearch)
        self.search_btn = Button(self, text="Search", command=self.onSearch)
        self.search_btn.grid(row=1, column=1)
        self.output_box = Text(self, width=98, height=34)
        self.output_box.grid(row=3, columnspan=2)

    def onUpdateSearch(self,key):
    # Somehow calling self.onSearch() does not register last key
    # And we need to correct "special chars"
        entries = ""
        self.output_box.delete(1.0, END)
        search_terms = self.input_box.get() + key.char
    # ...like, for instance, deleting last character
        if key.char == '\b':
            search_terms = self.input_box.get()[:-1]
        else: 
            search_terms = self.input_box.get() + key.char
        for item in onSearchFiles(search_terms):
            entries = "-----------------------------------------------------\n"
            entries = entries + "              -- " + item.title.split('\n')[0] + " -- \n"
            entries = entries + "          (Tags: " + item.tags.split('\n')[0] + " )\n"
            entries = entries + "-----------------------------------------------------\n\n"
            entries = entries + item.text
            for line in entries.split('\n'):
                self.output_box.insert(END, line + '\n')
            self.output_box.insert(END, "-----------------------------------------------------\n")


    def onSearch(self):
        entries = ""
        self.output_box.delete(1.0, END)
        search_terms = self.input_box.get()
        for item in onSearchFiles(search_terms):
            entries = "-----------------------------------------------------\n"
            entries = entries + "              -- " + item.title.split('\n')[0] + " -- \n"
            entries = entries + "          (Tags: " + item.tags.split('\n')[0] + " )\n"
            entries = entries + "-----------------------------------------------------\n\n"
            entries = entries + item.text
            for line in entries.split('\n'):
                self.output_box.insert(END, line + '\n')
            self.output_box.insert(END, "-----------------------------------------------------\n")


""" ---------------------------------
    GUI part for the Command add
    ---------------------------------""" 

class CommAdd(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent        
        self.initUI()
        
    def initUI(self):
      
        command_in = pyperclip.getcb()
        self.parent.title("Add a command card")
        self.style = Style()
        self.style.theme_use("default")        
        self.pack()
        
	self.note_title = Label(self, text="Enter a title for this command")
        self.note_title.grid(row=0)
	self.title_box = Entry(self, width=98)
        self.title_box.grid(row=1)
        self.title_box.focus()
	self.note_tags = Label(self, text="Enter some tags this command (space-separated)")
        self.note_tags.grid(row=2)
	self.tags_box = Entry(self, width=98)
        self.tags_box.grid(row=3)
        self.command_box = Text(self, width=98, height=30)
        self.command_box.insert(END, command_in)
        self.command_box.grid(row=4)
        self.add_btn = Button(self, text="Add", command=self.onAdd)
        self.add_btn.grid(row=5)


    def onAdd(self):
	title = self.title_box.get()
	tags = self.tags_box.get()
        command = self.command_box.get(1.0,END)

        onAddToFile(title,tags,command)
        self.parent.destroy()

""" ---------------------------------
    Other functions
    ---------------------------------""" 

   
def onLoadFiles():
    global entries_list
    del entries_list[:]

    with open(file_to_search) as file_open:
        lines = [line for line in file_open]

    read_status = "start"
    title = ""
    tags = ""
    text = ""

    for line_to_check in lines:
        if line_to_check[:2] == "= ":
            read_status = "title"
        elif line_to_check[:5] == "==== ":
            read_status = "tags"
        elif line_to_check[:3] == "{{{":
            read_status = "start_text"
        elif line_to_check[:3] == "}}}":
            read_status = "end_text"

        if read_status == "title":
            title = line_to_check.split("= ")[1]
        elif read_status == "tags":
            tags = line_to_check.split("==== ")[1]
        elif read_status == "getting_text":
            text = text + '    '.join(line_to_check.split('\t'))
        elif read_status == "start_text":
            read_status = "getting_text"
        elif read_status == "end_text":
            new_comm = CommandEntry(title,tags,text)
            title = ""
            tags = ""
            text = ""
            entries_list.append(new_comm)
            read_status = "start"


def onSearchFiles(search_terms):

    result = []
    for entry in entries_list:
        found = False
        for word in search_terms.split(' '):
            if (word in entry.title or
              word in entry.tags or
              word in entry.text):
                found = True
        if found:
            result.append(entry)
    
    return result
        
def onAddToFile(title,tags,command):
    with open(file_to_search, "a") as f:
        f.write("= " + title + "\n")
        f.write("==== " + tags + "\n")
        f.write("{{{\n")
        f.write(command)
        f.write("}}}\n")

def main():
    
    try:
        if sys.argv[1] == "-import" or sys.argv[1] == "-i":
            root = Tk()
            comm = CommAdd(root)
            root.geometry("800x600+0+0")
            root.mainloop()  
    except IndexError:
        onLoadFiles()
        root = Tk()
        comm = CommSearch(root)
        root.geometry("800x600+0+0")
        root.mainloop()  


if __name__ == '__main__':
    main()  

