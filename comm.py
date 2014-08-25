"""
Program to store and search commands and tricks, 
instead of constantly searching Stackoverflow for the same things

"""
__version__ = 0.2
__date__ = "August 2014"
__author__ = "alonsofonseca.angel@gmail.com"
__licence__  = "Public Domain"


from ttk import Button, Entry, Frame, Label, Scrollbar, Style, Treeview
from Tkinter import BOTH, END, Listbox, NO, Tk, Text, YES

import pyperclip

import comm_data as data

""" ---------------------------------
    I believe these are better off being global
    ---------------------------------"""
entries = []
entries_map = {}

""" ---------------------------------
    GUI part for the Command search
    ---------------------------------""" 

class CommSearch(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent        
        self.initUI()
        
    def initUI(self):

        self.entries_found = []

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
        self.output_box = Treeview(self, columns=("Example"))
        ysb = Scrollbar(self, orient='vertical', command=self.output_box.yview)
        xsb = Scrollbar(self, orient='horizontal', command=self.output_box.xview)
        self.output_box.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.output_box.heading('Example', text='Example', anchor='w')
        self.output_box.column("#0",minwidth=0,width=0, stretch=NO)
        self.output_box.column("Example",minwidth=0,width=785)
        self.output_box.bind("<Button-1>", self.OnEntryClick)
        self.output_box.grid(row=3, columnspan=2)
        self.selected_box = Text(self, width=110, height=19)
        self.selected_box.grid(row=4, columnspan=2)
        self.gotoadd_btn = Button(self, text="Go to Add", command=self.onGoToAdd)
        self.gotoadd_btn.grid(row=5)

    def OnEntryClick(self, event):
        try:
            item = self.output_box.selection()[0]
        except IndexError:
            pass
        entry_title = self.output_box.item(item,"value")
        for item in self.entries_found:
            if str(entry_title) == str("('" + item.title.strip('\n') + "',)"):
                self.selected_box.delete(0.1, END)
                self.selected_box.insert(END, item.text + '\n')

    def onUpdateSearch(self, key):
    # Somehow calling self.onSearch() does not register last key
    # And we need to correct "special chars"
        global entries, entries_map
        text_entries = ""
        for item in self.output_box.get_children():
            self.output_box.delete(item)		
    # ...like, for instance, deleting last character
        if key.char == '\b':
            search_terms = str(self.input_box.get()[:-1])
        else: 
            search_terms = str(self.input_box.get() + key.char)
        self.entries_found = []
        self.entries_found = data.Search(search_terms,entries,entries_map)
        for item in range(len(self.entries_found)):
            aux = self.output_box.insert('', 'end', '', value=[self.entries_found[item].title.split('\n')[0]])

			
    def onSearch(self):
        global entries, entries_map
        text_entries = ""
        for item in self.output_box.get_children():
            self.output_box.delete(item)
        search_terms = str(self.input_box.get())
        for item in data.Search(search_terms,entries,entries_map):
            self.output_box.insert('', 'end', '', value=[self.entries_found[item].title.split('\n')[0]])
			
    def onGoToAdd(self):
        newroot = Tk()
        newcomm = CommAdd(newroot)
        newroot.geometry("800x600+0+0")
        newroot.mainloop()

""" ---------------------------------
    GUI part for Adding an Entry
    ---------------------------------""" 

class CommAdd(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent        
        self.initUI()
        
    def initUI(self):
        # This should be different if running on Windows....
        content = pyperclip.paste()
        print content  
        self.entries_found = []

        self.parent.title("Add a new command card")
        self.style = Style()
        self.style.theme_use("default")        
        self.pack()
        
        self.new_title_label = Label(self, text="Title")
        self.new_title_label.grid(row=0, columnspan=2)
        self.new_title_entry = Entry(self, width=90)
        self.new_title_entry.grid(row=1, column=0)
        self.new_title_entry.focus()
        self.new_content_label = Label(self, text="Card")
        self.new_content_label.grid(row=2, columnspan=2)
        self.new_content_text = Text(self, width=110, height=34)
        self.new_content_text.insert(END, content)
        self.new_content_text.grid(row=3, columnspan=2)
        self.add_new_btn = Button(self, text="Add New Card", command=self.onAddNew)
        self.add_new_btn.grid(row=4)

    def onAddNew(self):

        pass


def main():
    global entries, entries_map
    entries = data.LoadFiles()
    entries_map = data.MapData(entries)
    root = Tk()
    comm = CommSearch(root)
    root.geometry("800x600+0+0")
    root.mainloop()  


if __name__ == '__main__':
    main()  

