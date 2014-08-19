import os
import re
import operator

file_dir="data"


class CommandEntry(object):
    title = ""
    tags = ""
    text = ""

    # The class "constructor" - It's actually an initializer 
    def __init__(self, title, tags, text):
        self.title = title
        self.tags = tags
        self.text = text
		

def LoadFiles():
    lines = [] 
    entries_list = []
    read_status = "start"
    title = ""
    tags = ""
    text = ""

    file_list = os.listdir(file_dir)

    for file_to_read in file_list:
        with open(file_dir + "/" + file_to_read) as file_open:
            for line in file_open:
                if line[:2] == "= ":
                    read_status = "title"
                elif line[:5] == "==== ":
                    read_status = "tags"
                elif line[:3] == "{{{":
                    read_status = "start_text"
                elif line[:3] == "}}}":
                    read_status = "end_text"
                    
                if read_status == "title":
                    title = line.split("= ")[1]
                elif read_status == "tags":
                    try:
                        tags = line.split("==== ")[1]
                    except IndexError:
                        print ("Warning - Omitting line: " + str(line))
                elif read_status == "getting_text":
                    text = text + '    '.join(line.split('\t'))
                elif read_status == "start_text":
                    read_status = "getting_text"
                elif read_status == "end_text":
                    new_comm = CommandEntry(title,tags,text)
                    title = ""
                    tags = ""
                    text = ""
                    entries_list.append(new_comm)
                    read_status = "start"
	
    return entries_list
	
def MapData(entries_list):
    wordmap = {}    
    for entry_nr in range(len(entries_list)):
        text = re.sub(r'\W+', ' ', entries_list[entry_nr].title + entries_list[entry_nr].tags + entries_list[entry_nr].text)
        for word in text.split():
            try:
                keys = wordmap[word]
                try:
                    keys[entry_nr] += 1
                except KeyError:
                    keys[entry_nr] = 1		
            except KeyError:
                keys = {}
                keys[entry_nr] = 1
            wordmap[word] = keys
    return wordmap

def Search(terms,entries,entries_map):
    entries_order = {}
    entries_list = []
    for word in terms.split(' '):
        keys_found = entries_map[word]
        keys = keys_found.keys()
        for key in keys:
            try:
                entries_order[key] += keys_found[key]
            except KeyError:
                entries_order[key] = keys_found[key]
    sorted_tuples = sorted(entries_order.iteritems(), key=operator.itemgetter(1),  reverse=True)
    for tuple in sorted_tuples:
	    key = tuple[0]
	    entries_list.append(entries[key])
    return entries_list
	
	
