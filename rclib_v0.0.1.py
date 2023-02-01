from operator import index
from tkinter import CENTER, E, NE, VERTICAL, TclError, ttk
import pandas as pd
import datetime as dt
from datetime import date
import tkinter as tk
import csv
import math
from random import randint, randrange

#Basic init#

file = "sample.csv"
user_file = "usersample.csv"
data = pd.read_csv(file,sep="|",index_col=['ID'])
user_data = pd.read_csv(user_file,sep="|")
columns = ['title','name','type','status','holder','dt_added','dt_lil']

df_base = pd.DataFrame(data)

available = df_base[df_base['status'].isin([('home')])]
df_available = pd.DataFrame(available,columns=['title','name','type','status','holder','dt_added','dt_lil'])

unavailable = df_base[df_base['status'].isin([('borrowed')])]
df_unavailable = pd.DataFrame(unavailable,columns=['title','name','type','status','holder','dt_added','dt_lil'])

df_borrow_basket = pd.DataFrame(columns=['title','name','type','status','holder','dt_added','dt_lil'])

df_user_repository = pd.DataFrame(user_data)

checkout_content = []

class session_inventory:

    def __init__(self):
        self.inventory = pd.DataFrame(index=['ID'],columns=columns)
        
    def _get_inventory(self):
        self.inventory = pd.DataFrame(data)

    def _get_available(self):
        self.inventory = pd.DataFrame(available)

    def _get_unavailable(self):
        self.inventory = pd.DataFrame(unavailable)

    def _update_inventory(self):
        title = ttl.get()
        author = athr.get()
        type = btype.get()
        status = "home"
        holder = "redcafe"
        book_data = title,author,type,status,holder
        new_book = _make_book(book_data)
        self.inventory.update(new_book._show_book(new_book))

    def _save_inventory(self):
        inventory = session_inventory()
        df_base.loc[int(self.inventory.first_valid_index())] = [inventory.inventory['title'],
        inventory.inventory['name'],
        inventory.inventory['type'],
        inventory.inventory['status'],
        inventory.inventory['holder'],
        inventory.inventory['dt_added'],
        inventory.inventory['dt_lil']
        ]
        df_base.update(inventory.inventory)

    def _update_base_file(self):
        df_base.to_csv(file,mode='w',sep="|",columns=columns)

class Book():

    def __init__(self,init_data):
        self.title = init_data[0]
        self.name = init_data[1]
        self.type = init_data[2]
        self.status = init_data[3]
        self.holder = init_data[4]
        self.dt_added = date.today()
        self.dt_lil = self._borrow_time_check()
        self.book_id = self._generate_id()

    def _generate_id(self):
        book_id = randrange(1000000)
        while(book_id in df_base.index.values):
            book_id = randrange(1000000)
        self.book_id = book_id
        return book_id

    def _borrow_time_check(self):
        if self.status == 'home':
            dt_lil = date.today()
        else:
            dt_lil = self.dt_lil
        return dt_lil
            
    def _set_title(self, title:str):
        self.title = title
        
    def _set_name(self, name:str):
        self.name = name

    def _set_type(self, type: str):
        self.type = type

    def _set_status(self, status: str):
        self.status = status

    def _set_holder(self, holder: str):
        self.holder = holder

    def _show_book(self,init_data):
        title = ttl.get()
        author = athr.get()
        type = btype.get()
        status = "home"
        holder = "redcafe"
        book_data = [title,author,type,status,holder]
        book = book_data,self.book_id
        inventory.inventory.loc[int(self.book_id)] = [title,author,type,status,holder,self.dt_added,self.dt_lil]

    def _update_init(self):
        pass

def _make_book(init_data):
    if str(ttl.get()) in df_base['title'].to_list():
        statmsg.set(f"{ttl.get().title()} ist bereits in der Bibliothek")
        raise ValueError(f"ERROR CODE 42069 \t {tent.get().title()} {authent.get().title()} ALREADY IN LIBRARY")
    else:
        return Book(init_data)

inventory = session_inventory()

#frontend functions#

def avlist_row_content_getter(id):
    selection_display.delete(*selection_display.get_children())
    id = list1.selection()
    item_id = df_unavailable.loc[int(id[0])]
    item_content = item_id['title'],item_id['name'],item_id['type'],item_id['status'],item_id['holder'],item_id['dt_added'],item_id['dt_lil']
    selection_display.insert('','end',iid=int(id[0]),values=item_content)

def borrow_basket_append():
    id = list1.selection()
    item_id = df_available.loc[int(id[0])]
    item_content = item_id['title'],item_id['name'],item_id['type'],item_id['status'],item_id['holder'],item_id['dt_added'],item_id['dt_lil']
    borrow_basket_idx_len = int((df_borrow_basket.size)/len(df_borrow_basket.columns))
    if borrow_basket_idx_len == 0:
        df_borrow_basket.loc[int(id[0])] = [item_id['title'],item_id['name'],item_id['type'],item_id['status'],item_id['holder'],item_id['dt_added'],item_id['dt_lil']]
        list2.insert('','end',iid=int(id[0]),values=(item_content))
        df_available.drop(labels=int(id[0]),inplace=True,axis=0) 
    else:
        df_borrow_basket.loc[int(id[0])] = [item_id['title'],item_id['name'],item_id['type'],item_id['status'],item_id['holder'],item_id['dt_added'],item_id['dt_lil']]
        list2.insert('','end',iid=id[0],values=(item_content))
        df_available.drop(labels=int(id[0]),inplace=True)
    list1.delete(list1.selection())
    selection_display.delete(*selection_display.get_children())
    for i in df_borrow_basket.itertuples():
        checkout_list.insert('','end',iid=id[0],values=(item_id['title'],item_id['name'],item_id['type'],item_id['status'],item_id['holder'],item_id['dt_added'],item_id['dt_lil']))

def sellist_row_content_getter(selection_id_nr):
    selection_id_nr = list2.selection()
    global selection_content2
    selection_content2 = list2.set(selection_id_nr)
    return selection_content2

def borrow_basket_unappend():
    id = list2.selection()
    item_id = df_borrow_basket.loc[int(id[0])]
    item_content = item_id['title'],item_id['name'],item_id['type'],item_id['status'],item_id['holder'],item_id['dt_added'],item_id['dt_lil']
    df_av_idx_len = 0
    try:
        df_av_idx_len == int(df_available.size)/(len(df_available.index))
    except ZeroDivisionError:
        pass
    df_available.loc[int(id[0])] = item_id['title'],item_id['name'],item_id['type'],item_id['status'],item_id['holder'],item_id['dt_added'],item_id['dt_lil']
    list1.insert('','end',iid=id[0],values=item_content)
    df_borrow_basket.drop(labels=int(id[0]),inplace=True)
    list2.delete(list2.selection())
    checkout_list.delete(id[0])

def borrow_finish():
    list2.delete(*list2.get_children())
    checkout_window.state('withdraw')

def save_bb_selection():
    username = name_entry.get()
    email = email_entry.get()
    fieldnames = ['user','email_adress']
    with open(user_file,'a') as usfil:
        user_rep_writer = csv.DictWriter(usfil,fieldnames=fieldnames,delimiter="|")
        user_rep_writer.writerow({'user':username,'email_adress':email})
    for item in df_borrow_basket.itertuples():
        df_base.loc[int(item[0])]=[item[1],item[2],item[3],"borrowed",username,item[6],item[7]]
    df_base.to_csv(file,mode='w',sep="|",columns=columns)
    name_entry.delete(0,'end')
    email_entry.delete(0,'end')
    checkout_list.delete(*checkout_list.get_children())
    chstmsg.set("Ausgeliehen!")
    #write function to daily update dt_lil for status=home books
    
def add_new_book():
    title = ttl.get()
    author = athr.get()
    type = btype.get()
    status = "home"
    holder = "redcafe"
    book_data = title,author,type,status,holder
    new_book = _make_book(book_data)
    inventory._update_inventory()
    inventory._save_inventory()
    bkindex = int(inventory.inventory.first_valid_index())
    df_base.update(inventory.inventory.loc[[bkindex]])
    inventory._update_base_file()
    statmsg.set("Das Buch wurde gespeichert")
    inventory.inventory.drop([inventory.inventory.first_valid_index()],axis=0,inplace=True)
    ttl.set("")
    athr.set("")
    btype.set("")

def return_window_button():
    print(user_select.get())
    sel_user_bk_view.delete(*sel_user_bk_view.get_children())
    select_user_books = users_books[users_books['holder'].isin([(user_select.get())])]
    for i in select_user_books.itertuples():
        sel_user_bk_view.insert('','end',iid=i[0],values=(i[1],i[2],i[3],i[4],i[5]))
    print(select_user_books)
    #get user
    #select book/books
    #update df base & csv base
    #set status message, clear fields

def return_sel_book():
    sel_id = sel_user_bk_view.selection()
    item_id = users_books.loc[int(sel_id[0])]
    item_content = item_id['title'],item_id['name'],item_id['type'],"home","redcafe",item_id['dt_added'],item_id['dt_lil']
    df_base.loc[item_id.name] = item_content
    sel_user_bk_view.delete(sel_id)
    df_base.to_csv(file,mode='w',sep="|",columns=columns)
    df_base.update(df_base)
    #seperate base update function?

def delete_inv_book():
    sel_id = inv_list.selection()
    #item_id = df_base.loc[int(sel_id[0])]
    df_base.drop(int(sel_id[0]),inplace=True)
    print(int(sel_id[0]))
    inv_list.delete(sel_id)
    df_base.to_csv(file,mode='w',sep="|",columns=columns)

def lookup_av():
    list1.delete(*list1.get_children())
    query = search_entry.get()
    q_int = str(query.strip().lower())
    result = (df_available.loc[df_available['title'and'name'].str.contains(q_int,case=False)])
    for i in result.itertuples():
        list1.insert('','end',iid=i[0],values=(i[1],i[2],i[3],i[4],i[5]))
    bbstatmsg.set("Ergebnisse:")
    
def pw_check():
    if pw_entry.get() == "password123":
        _open_admin_window()
        pw_entry_stat_msg.set("")
        _close_pw_check()
    else:
        pw_entry_stat_msg.set("###VERFASSUNGSSCHUTZ DETECTED###")
    
#backend functions#

def _open_borrow_window():
    borrow_window.state('normal')

def _open_return_window():
    return_window.state('normal')

def _open_admin_window():
    admin_window.state('normal')

def _open_co_window():
    checkout_window.state('normal')

def _open_bkadd():
    bookadd_window.state('normal')

def _open_inv():
    inv_window.state('normal')
    try:
        for i in df_base.itertuples():
            inv_list.insert('','end',iid=i[0],values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]))
    except tk.TclError:
        pass

def _open_inv_conf():
    inv_conf_win.state('normal')

def _open_pw_check():
    access_check_win.state('normal')

def _bw_withdraw():
    borrow_window.state('withdraw')

def _rw_withdraw():
    return_window.state('withdraw')

def _aw_withdraw():
    admin_window.state('withdraw')

def _co_withdraw():
    checkout_window.state('withdraw')

def _bkadd_withdraw():
    bookadd_window.state('withdraw')

def _inv_withdraw():
    inv_window.state('withdraw')

def _disable_email_entry():
    if var.get() == 1:
        email_entry.state(['disabled'])
    else:
        email_entry.state(['!disabled'])

def _check_username_available():
    username = name_entry.get()
    print()

def _close_inv_conf():
    inv_conf_win.state('withdrawn')

def _close_pw_check():
    access_check_win.state('withdrawn')

def _update_base():
    for i in df_base['status'].items(): 
            if i[1] == 'home':
                item = df_base['dt_lil'].loc[i[0]]
                df_base['dt_lil'].loc[i[0]] = date.today()
    df_base.to_csv(file,mode='w',sep="|")

def _update_display():
    list1.delete(*list1.get_children())
    for i in df_available.itertuples():
        list1.insert('','end',iid=i[0],values=(i[1],i[2],i[3],i[4],i[5]))

def _test():
    print("test")

#tkinter interface: menu #

root = tk.Tk()
root.title("")
root.geometry("800x400-300+150")

mainframe_style = ttk.Style()
mainframe_style.configure(
    'MF_Style.TFrame',
    background='red',
    borderwidth=5,
    relief='raised'
    )
mainframe = ttk.Frame(
    root,
    padding="75 75 150 150",
    borderwidth=2,
    relief="solid",
    style='MF_Style.TFrame'
    )
mainframe.grid(column=0,row=0,sticky=("N,W,E,S"))

heading_frame = ttk.Frame(
    mainframe,
    padding="10 10 10 10",
    borderwidth=2,
    relief="solid",
    width=100,
    height=50,
    style='MF_Style.TFrame'
    )
heading_frame.grid(row=0,column=0,columnspan=3,sticky=("N"))

#menu styling#

menu_heading = ttk.Label(
    heading_frame,
    text="Willkommen in der Bibliothek des Roten Cafés -",
    relief="flat",
    justify='center'
    )
menu_heading.grid(row=0,column=0)
menu_heading['font']="TkMenuFont"

menu_subheading = ttk.Label(
    heading_frame,
    text="Stöbern, Bücher ausleihen und vieles mehr!",
    justify='left',
    anchor='w'
    )
menu_subheading.grid(row=0,column=1,sticky=("E"))

#populating the menu#

menu_items = ttk.PanedWindow(master=mainframe,orient='horizontal')

men1 = ttk.LabelFrame(
    menu_items,
    text="Buch ausleihen:",
    width=75,height=75,
    padding="10 10 10 10",
    labelanchor='n'
    )

ttk.Button(
    men1,
    command=_open_borrow_window,
    text="Zur Ausleihe"
    ).grid(row=0,
        column=0,
        columnspan=2
        )

men2 = ttk.LabelFrame(
    menu_items,
    text="Bücher zurückgeben:",
    width=75,
    height=75,
    padding="10 10 10 10",
    labelanchor='n'
    )

ttk.Button(
    men2,
    command=_open_return_window,
    text="Zur Rückgabe"
    ).grid(
        row=0,
        column=0,
        columnspan=2
        )

men3 = ttk.LabelFrame(
    menu_items,
    text="Nur für das Plenum:",
    width=75,
    height=75,
    padding="10 10 10 10",
    labelanchor='n'
    )

ttk.Button(
    men3,
    text="Bibliotheksverwaltung",
    command=_open_pw_check
    ).grid(
        row=0,
        column=0,
        columnspan=2
        )

menu_items.add(men1,weight=1)
menu_items.add(men2,weight=1)
menu_items.add(men3,weight=1)

#function windows#

#borrow window#

borrow_window = tk.Toplevel(root)
borrow_window.geometry('800x500-800+150')
borrow_window.state('withdrawn')
borrow_window.protocol("WM_DELETE_WINDOW",_bw_withdraw)
borrow_window.minsize(400,400)
borrow_window.title("Bücher ausleihen")

list1 = ttk.Treeview(borrow_window,
    show=['headings'],
    columns=['title','name','type','status','holder','dt_added','dt_lil'],
    displaycolumns=[0,1],
    selectmode=['browse']
    )

list1.grid(row=2,column=0,columnspan=2)
list1.heading('title',text='Titel')
list1.heading('name',text='Autor*in')
list1.heading('type',text='Typ')
list1.heading('status',text='Status')
list1.heading('holder',text='Halter*in')
list1.heading('dt_added',text="Hinzugefügt")
list1.heading('dt_lil',text="Ausgeliehen seit")
list1.bind('<<TreeviewSelect>>',avlist_row_content_getter)

for i in df_available.itertuples():
    list1.insert('','end',iid=i[0],values=(i[1],i[2],i[3],i[4],i[5]))

list2 = ttk.Treeview(borrow_window,
    show=['headings'],
    columns=['title','name','type','status','holder','dt_added','dt_lil'],
    displaycolumns=[0,1]
    )

list2.grid(row=2,column=2,columnspan=2)
list2.heading('title',text='Titel')
list2.heading('name',text='Autor*in')
list2.heading('type',text='Typ')
list2.heading('status',text='Status')
list2.heading('holder',text='Halter*in')
list2.heading('dt_added',text="Hinzugefügt")
list2.heading('dt_lil',text="Ausgeliehen seit")
list2.bind('<<TreeviewSelect>>',sellist_row_content_getter)

searchvar = tk.StringVar()
search_entry = ttk.Entry(borrow_window,textvariable=searchvar)
search_entry.grid(row=0,column=1,columnspan=1)

selection_display = ttk.Treeview(borrow_window,
    show=['headings'],
    columns=['title','name','type','status','holder','dt_added','dt_lil'],
    displaycolumns=[0,1],
    height=1
    )

selection_display.heading('title',text="Titel")
selection_display.heading('name',text="Autor*in")
selection_display.grid(row=6,column=0,columnspan=2)

bbstatmsg = tk.StringVar()
bbstatmsg.set("Neuheiten")

#bb append button#
ttk.Button(
    borrow_window,
    command=borrow_basket_append,
    text="In den Bücherkorb legen"
    ).grid(
        row=7,
        column=0,
        columnspan=2
        )

#bb unappend button#
ttk.Button(
    borrow_window,
    command=borrow_basket_unappend,
    text="Zurück stellen"
    ).grid(
        row=5,
        column=2
        )

#bb borrow button#
ttk.Button(
    borrow_window,
    command=lambda:[_open_co_window(),_update_base(),_update_display()],
    text="Ausleihen"
    ).grid(
        row=5,
        column=3
        )

#bb stat msg label#
ttk.Label(
    borrow_window,
    textvariable=bbstatmsg
    ).grid(
        row=1,
        column=0,
        columnspan=2
        )

#bb search button#
ttk.Button(
    borrow_window,
    text="Suchen",
    command=lookup_av
    ).grid(
        row=0,
        column=0
        )

#bb selection label#
ttk.Label(
    borrow_window,
    text="Auswahl:"
    ).grid(
        row=5,
        column=0,
        columnspan=2
        )

#bb basket label#
ttk.Label(
    borrow_window,
    text="Mein Bücherkorb"
    ).grid(
        row=1,
        column=2,
        columnspan=2
        )

#bb back button#
ttk.Button(
    borrow_window,
    text="Zurück",
    command=_bw_withdraw
    ).grid(
        row=8,
        column=0
        )

#bb done window#
ttk.Button(
    borrow_window,
    text="Fertig",
    command=_bw_withdraw
    ).grid(
        row=8,
        column=3
        )

for child in borrow_window.winfo_children():
    child.grid_configure(padx=5,pady=5)

#Checkout Window#
checkout_window = tk.Toplevel(root)
checkout_window.geometry('530x400-800+150')
checkout_window.state('withdrawn')
checkout_window.protocol("WM_DELETE_WINDOW",_co_withdraw)

var = tk.IntVar()
chstmsg = tk.StringVar()
emailvar = tk.StringVar()
usernamevar = tk.StringVar()
checkout_contentvar = tk.StringVar(value=checkout_content)

ttk.Label(checkout_window,text="Auswahl").grid(row=0,column=0)
ttk.Label(checkout_window,textvariable=chstmsg).grid(row=10,column=1,columnspan=2)
ttk.Button(checkout_window,text="Zurück",command=_co_withdraw).grid(row=11,column=1)
ttk.Button(checkout_window,text="Fertig",command=borrow_finish).grid(row=11,column=2)
ttk.Label(checkout_window,text="Name:").grid(row=7,column=1)
ttk.Label(checkout_window,text="E-Mail:").grid(row=8,column=1)

email_entry = ttk.Entry(checkout_window,textvariable=emailvar,state='normal')
fin_checkout = ttk.Button(checkout_window,text="Ausleihen",command=save_bb_selection)
 
name_entry = ttk.Entry(checkout_window,textvariable=usernamevar)

email_check = ttk.Checkbutton(checkout_window,
    text="Ich habe schon eine Email-Adresse hinterlegt",
    command=_disable_email_entry,
    variable=var,
    offvalue=0,
    onvalue=1,
)

email_check.grid(row=6,column=1,columnspan=2)
name_entry.grid(row=7,column=2)
email_entry.grid(row=8,column=2)
fin_checkout.grid(row=9,column=2)
checkout_list = ttk.Treeview(checkout_window,show=['headings'],
    columns=['title','name','type','status','holder','dt_added','dt_lil'],
    displaycolumns=[0,1]
    )

checkout_list.grid(row=1,column=0,rowspan=5,columnspan=4)
checkout_list.heading('title',text='Titel')
checkout_list.heading('name',text='Name')
checkout_list.heading('type',text='Typ')
checkout_list.heading('status',text='Status')
checkout_list.heading('holder',text='Halter*in')
checkout_list.heading('dt_added',text="Hinzugefügt")
checkout_list.heading('dt_lil',text="Ausgeliehen seit")

email_check = ttk.Checkbutton(checkout_window,
    text="Ich habe schon eine Email-Adresse hinterlegt",
    command=_disable_email_entry,
    variable=var,
    offvalue=0,
    onvalue=1,
)

#return window#

return_window = tk.Toplevel(root)
return_window.geometry('600x200-250+250')
return_window.state('withdrawn')
return_window.protocol("WM_DELETE_WINDOW",_rw_withdraw)
user_names = df_user_repository.to_records()

ttk.Label(return_window,text="Nutzer*in:").grid(row=0,column=0)
ttk.Button(return_window,text="Bücher anzeigen",command=return_window_button).grid(row=0,column=2)
ttk.Button(return_window,text="Zurück geben",command=return_sel_book).grid(column=1,row=2)
ttk.Button(return_window,text="Zurück",command=_rw_withdraw).grid(column=0,row=3)
ttk.Button(return_window,text="Fertig",command=_rw_withdraw).grid(column=2,row=3)

user_names_rawstring = []
curr_user_sel = tk.StringVar()
for item in df_user_repository.to_records():
    user_names_rawstring.append(item[1])
user_select = ttk.Combobox(return_window,values=user_names_rawstring,textvariable=curr_user_sel)
user_select.grid(row=0,column=1)
ttk.Label(return_window,text="Deine Bücher:").grid(row=1,column=2)
bbview = ttk.Treeview(return_window,
    show=['headings'],
    columns=['title','name','type','status','holder','dt_added','dt_lil'],
    displaycolumns=[0,1]
)

users_books = df_unavailable[df_unavailable['holder'].isin(df_user_repository[('user')])]
sel_user_bk_view = ttk.Treeview(return_window,show=['headings'],
    columns=['title','name','type','status','holder','dt_added','dt_lil'],
    displaycolumns=[0,1],
    height=3,
    )

sel_user_bk_view.grid(row=1,column=0,columnspan=3)


#admin access check

access_check_win = tk.Toplevel(root)
access_check_win.state('withdrawn')
access_check_win.geometry("250x150-550+250")
access_check_win.protocol("WM_DELETE_WINDOW",_close_pw_check)
pw = tk.StringVar()
ttk.Label(access_check_win,text="Passwort:").grid(row=1,column=0,columnspan=2)
pw_entry = ttk.Entry(access_check_win,textvariable=pw,show="*")
pw_entry.grid(row=2,column=0,columnspan=2)
ttk.Button(access_check_win,text="Einloggen",command=pw_check).grid(row=3,column=0)
ttk.Button(access_check_win,text="Zurück",command=_close_pw_check).grid(row=3,column=1)
pw_entry_stat_msg = tk.StringVar()
pw_check_msg = ttk.Label(access_check_win,textvariable=pw_entry_stat_msg,foreground="#FC2521").grid(row=4,column=0,columnspan=2)

for admwgt in access_check_win.winfo_children():
    admwgt.grid_configure(padx=5,pady=5)

#admin window#

admin_window = tk.Toplevel(root)
admin_window.geometry('300x300-250+250')
admin_window.title("Bibliotheksverwaltung")
admin_window.state('withdrawn')
admin_window.protocol("WM_DELETE_WINDOW",_aw_withdraw)
ttk.Button(admin_window,text="Buch hinzufügen",command=_open_bkadd).grid(column=1,row=1)
ttk.Button(admin_window,text="Inventar",command=_open_inv).grid(column=1,row=2)

#admin child window bookadd#

bookadd_window = tk.Toplevel(root)
bookadd_window.geometry('300x300-250+250')
bookadd_window.state('withdrawn')
bookadd_window.protocol("WM_DELETE_WINDOW",_bkadd_withdraw)
tk.Label(bookadd_window,text="Titel:").grid(column=0,row=0)
tk.Label(bookadd_window,text="Autor*in:").grid(column=0,row=1)
tk.Label(bookadd_window,text="Typ").grid(column=0,row=2)
statmsg = tk.StringVar()
tk.Label(bookadd_window,textvariable=statmsg).grid(column=1,row=3)
ttl = tk.StringVar()
tent = tk.Entry(bookadd_window,textvariable=ttl)
tent.grid(column=1,row=0)
athr = tk.StringVar()
authent = tk.Entry(bookadd_window,textvariable=athr)
authent.grid(column=1,row=1)
btype = tk.StringVar()
tpent = ttk.Combobox(bookadd_window,textvariable=btype,values=['hardcover','paperback'])
tpent.grid(column=1,row=2)
book_data = tent.get(),authent.get(),tpent.get(),"home","redcafe"
new_book = _make_book(book_data)
tk.Button(bookadd_window,text="Speichern",command=add_new_book).grid(column=1,row=4)

#admin child window inventory

inv_window = tk.Toplevel(root)
inv_window.geometry('1200x300-250+250')
inv_window.state('withdrawn')
inv_window.protocol("WM_DELETE_WINDOW",_inv_withdraw)
inv_list = ttk.Treeview(inv_window,
    show=['headings'],
    columns=['ID','title','name','type','status','holder','dt_added','dt_lil']
    )

inv_list.grid(row=1,column=1)
inv_list.heading('ID',text="Buch-ID")
inv_list.heading('title',text='Titel')
inv_list.heading('name',text='Name')
inv_list.heading('type',text='Typ')
inv_list.heading('status',text='Status')
inv_list.heading('holder',text='Halter*in')
inv_list.heading('dt_added',text="Hinzugefügt")
inv_list.heading('dt_lil',text="Ausgeliehen seit")
ttk.Button(inv_window,text="Buch löschen",command=_open_inv_conf).grid(column=1,row=2)

inv_conf_win = tk.Toplevel(inv_window)
inv_conf_win.geometry("200x75-450+500")
inv_conf_win.state('withdrawn')
inv_conf_win.protocol("WM_DELETE_WINDOW",_close_inv_conf)
ttk.Label(inv_conf_win,text="Buch wirklich löschen?").grid(column=1,row=1,columnspan=2,rowspan=2)
ttk.Button(inv_conf_win,text="Nein",command=_close_inv_conf).grid(column=1,row=3)
ttk.Button(inv_conf_win,text="Ja",command=lambda:[delete_inv_book(),_close_inv_conf()]).grid(column=2,row=3)

#root mainloop#

for child in mainframe.winfo_children():
    child.grid_configure(padx=5,pady=5)

root.mainloop()
