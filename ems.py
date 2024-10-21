from customtkinter import*
from PIL import Image
from tkinter import ttk # for treeview rightframe de 
from tkinter import messagebox # login olurken mesaj çıkması için bunu import etmek gerek
import database
import random

#Functions


def delete_all():
    result=messagebox.askyesno('Confirm','Do you really want to delete all the records?')
    if result:
        database.deleteall_records()
        treeview_data()
        clear()
    


def show_all():
    treeview_data()
    searchEntry.delete(0,END)
    searchBox.set('Search By')
    

def search_employee():
    if searchEntry.get()=='':
        messagebox.showerror('Error for Searching','You Must Enter Some Value to Search')
    elif searchBox.get()=='Search By': #default ise 
        messagebox.showerror('Error for Searching','You Must Select an Option')
    else:
        searched_data=database.search(searchBox.get(),searchEntry.get()) #these two value will pass
        tree.delete(*tree.get_children())# bu fonksiyon ile her çağırışımızda aynı liste üst üste duplicate etmesin diye temizledik ve ardından yenisini ekleyip tazesiyle hepsini çektik yoksa her sorgu başı  tekrar tekrar aynı liste üst üste gelir ekleye ekleye öncekilerden birsürü olurdu
        for employee in searched_data: # döngüsü, bu listedeki her bir demeti (yani her bir çalışan kaydını) sırayla employee değişkenine atar ve döngü içindeki işlemleri yapar.
            tree.insert('',END,values=employee) # END: Yeni kaydın, mevcut kayıtların sonuna eklenmesini sağlar.



def delete_employee():
    selected_item=tree.selection()
    if not selected_item:
        messagebox.showerror('Error while Deleting','You must select data row to delete')
    else:
        database.delete(idEntry.get())
        treeview_data() # arayüze yansıtmak, görmek icin yoksa sadece databaesde göözükür.
        clear() # silme işleminden sonra seçildiği için soldaki fieldler doluyor onu boşaltıyor.
        messagebox.showinfo('Deleted!','It is deleted successfully')


def update_employee():
    selected_item = tree.selection()
    
    if not selected_item:
        messagebox.showerror('Updating Error', 'You must select a data row to update')
        return
    
    # Seçilen verinin mevcut ID'sini al
    existing_id = tree.item(selected_item)['values'][0]  # İlk sütun ID olmalı
    
    # Kullanıcının girdiği yeni ID ile mevcut ID'yi karşılaştır
    new_id = idEntry.get()
    if new_id != existing_id:
        messagebox.showerror('ID Change Error', 'ID cannot be changed only other field can be modified')
        return
    
    # ID değiştirilmemişse güncelleme işlemini yap
    database.update(new_id, nameEntry.get(), phoneEntry.get(), roleBox.get(), genderBox.get(), salaryEntry.get())
    
    treeview_data() 
    clear()
    messagebox.showinfo('Success', 'Data is updated')



def selection(event): # tıklamalarda treede seçince solda ki entrylere eklenmesi için.
    selected_item=tree.selection()
    if selected_item:
        clear() # bunu seçmezsek tıkladıgımız peş peşe birsürü yazıyor entrylerde EMP1EMP5EMP3 diye ekleyerek..
        row=tree.item(selected_item)['values'] #tree içinde bir şeye tıklanınca print ediyoruz satırın değerlerini
        idEntry.insert(0,row[0])
        nameEntry.insert(0,row[1])
        phoneEntry.insert(0,row[2])
        roleBox.set(row[3])
        genderBox.set(row[4])
        salaryEntry.insert(0,row[5])


def clear(value=False): #to clean after entering data to make fields empty again
    if value:
        tree.selection_remove(tree.focus()) # odaklanmış öğeyi seçili öğelerden çıkarır.
    idEntry.delete(0,END)
    nameEntry.delete(0,END)
    phoneEntry.delete(0,END)
    roleBox.set('Web Developer')
    genderBox.set('Male')
    salaryEntry.delete(0,END)



def treeview_data():
    employees=database.fetch_employees() # Bu satır, fetch_employees fonksiyonunu çağırır ve onun döndürdüğü listeyi employees adlı bir değişkene atar.
    tree.delete(*tree.get_children())# bu fonksiyon ile her çağırışımızda aynı liste üst üste duplicate etmesin diye temizledik ve ardından yenisini ekleyip tazesiyle hepsini çektik yoksa her sorgu başı  tekrar tekrar aynı liste üst üste gelir ekleye ekleye öncekilerden birsürü olurdu
    for employee in employees: # döngüsü, bu listedeki her bir demeti (yani her bir çalışan kaydını) sırayla employee değişkenine atar ve döngü içindeki işlemleri yapar.
        tree.insert('',END,values=employee) # END: Yeni kaydın, mevcut kayıtların sonuna eklenmesini sağlar.
        # Treeview'a eklenen satırlara hangi verilerin yazılacağını belirtmek için values parametresi kullanılır.



def add_employee():
    if idEntry.get()=='' or phoneEntry.get()=='' or salaryEntry.get()=='' or nameEntry.get()=='':
        messagebox.showerror('Empty Field Error','Complete all the required fields to add')
    elif database.id_exists(idEntry.get()):
        messagebox.showerror('Error','Id Already Exists')
    else:
        database.insert(idEntry.get(),nameEntry.get(),phoneEntry.get(),roleBox.get(),genderBox.get(),salaryEntry.get())
        treeview_data() #too add it to display
        clear() #when you add new data, make the fields empty for next data entering
        messagebox.showinfo('Success','Data is added successfully')



#GUI Part

window=CTk()
window.geometry('930x630+300+150') # +300 ve 150 komutu açılırken ekranın soldan 300 üstten 150 ile açılması için )
window.title('Employee Management System by Berkay')
window.configure(fg_color='#161C30')
window.resizable(False,False)


logo=CTkImage(Image.open('cover1.jpg'),size=(930,200))
logoLabel=CTkLabel(window,image=logo,bg_color='orange',text='')
logoLabel.grid(row=0,column=0,columnspan=2)

leftFrame=CTkFrame(window,fg_color='#161C30')
leftFrame.grid(row=1,column=0)

idLabel=CTkLabel(leftFrame,text='Id',font=('arial',18,'bold'),text_color='white')
idLabel.grid(row=0,column=0,padx=20,pady=15,sticky='w')
idEntry=CTkEntry(leftFrame,font=('arial',15,'bold'),width=180)
idEntry.grid(row=0,column=1)


nameLabel=CTkLabel(leftFrame,text='Name',font=('arial',18,'bold'),text_color='white')
nameLabel.grid(row=1,column=0,padx=20,pady=15,sticky='w')
nameEntry=CTkEntry(leftFrame,font=('arial',15,'bold'),width=180)
nameEntry.grid(row=1,column=1)


phoneLabel=CTkLabel(leftFrame,text='Phone',font=('arial',18,'bold'),text_color='white')
phoneLabel.grid(row=2,column=0,padx=20,pady=15,sticky='w')
phoneEntry=CTkEntry(leftFrame,font=('arial',15,'bold'),width=180)
phoneEntry.grid(row=2,column=1)

roleLabel=CTkLabel(leftFrame,text='Role',font=('arial',18,'bold'),text_color='white')
roleLabel.grid(row=3,column=0,padx=20,pady=15,sticky='w')
role_options=['Web Developer','Cloud Architech','Network Engineer','UX/UI Designer', 'IT Consultant', 'Data Scientist']
roleBox=CTkComboBox(leftFrame,values=role_options,font=('arial',15,'bold'),width=180,state='readonly')
roleBox.grid(row=3,column=1)
roleBox.set(role_options[0])


genderLabel=CTkLabel(leftFrame,text='Gender',font=('arial',18,'bold'),text_color='white')
genderLabel.grid(row=4,column=0,padx=20,pady=15,sticky='w')
gender_options=['Male','Female']
genderBox=CTkComboBox(leftFrame,values=gender_options,font=('arial',15,'bold'),width=180,state='readonly')
genderBox.grid(row=4,column=1)
genderBox.set(gender_options[0])

salaryLabel=CTkLabel(leftFrame,text='Salary',font=('arial',18,'bold'),text_color='white')
salaryLabel.grid(row=5,column=0,padx=20,pady=15,sticky='w')
salaryEntry=CTkEntry(leftFrame,font=('arial',15,'bold'),width=180)
salaryEntry.grid(row=5,column=1)



#right part

rightFrame=CTkFrame(window)
rightFrame.grid(row=1,column=1)

search_options=['Id','Name','Phone','Role','Gender','Salary']
searchBox=CTkComboBox(rightFrame,values=search_options,state='readonly')
searchBox.grid(row=0,column=0)
searchBox.set('Search By')

searchEntry=CTkEntry(rightFrame)
searchEntry.grid(row=0,column=1)

searchButton=CTkButton(rightFrame,text='Search',width=100,command=search_employee)
searchButton.grid(row=0,column=2)

showAllButton=CTkButton(rightFrame,text='Show All',width=100,command=show_all)
showAllButton.grid(row=0,column=3)

tree=ttk.Treeview(rightFrame,height=13)
tree.grid(row=1,column=0,columnspan=4)

tree['columns']=('Id','Name','Phone','Role','Gender','Salary')
# Sütun başlıklarını ayarlama
tree.heading('Id', text='Id')
tree.heading('Name', text='Name')
tree.heading('Phone', text='Phone')
tree.heading('Role', text='Role')
tree.heading('Gender', text='Gender')
tree.heading('Salary', text='Salary')

tree.config(show='headings')

tree.column('Id', anchor=CENTER, width=100)
tree.column('Name', anchor=CENTER, width=140)
tree.column('Phone', anchor=CENTER, width=150)
tree.column('Role', anchor=CENTER, width=170)
tree.column('Gender', anchor=CENTER, width=110)
tree.column('Salary', anchor=CENTER, width=110)

style=ttk.Style()
style.configure('Treeview.Heading',font=('arial',18,'bold')) 
style.configure('Treeview',font=('arial',13,'bold'),rowheight=30,background='#161C30',foreground='white')


scrollbar=ttk.Scrollbar(rightFrame,orient=VERTICAL,command=tree.yview)
scrollbar.grid(row=1,column=4,sticky='ns')

tree.config(yscrollcommand=scrollbar.set)


buttonFrame=CTkFrame(window,fg_color='#161C30')
buttonFrame.grid(row=2,column=0,columnspan=2,sticky='e') # columnspan kaç sütün kullanacağına karar verir Zaten 2 vardı tamamına yaydık
# üstte sticky e ile east yani doğuya en sağa yasladık.
newButton=CTkButton(buttonFrame,text='New Employee(Clean Fields)',font=('arial',15,'bold'),width=160,corner_radius=15,command=lambda:clear(True))
newButton.grid(row=0,column=0,pady=5)

addButton=CTkButton(buttonFrame,text='Add Employee',font=('arial',15,'bold'),width=160,corner_radius=15,command=add_employee)
addButton.grid(row=0,column=1,pady=5,padx=5)

updateButton=CTkButton(buttonFrame,text='Update Employee',font=('arial',15,'bold'),width=160,corner_radius=15,command=update_employee)
updateButton.grid(row=0,column=2,pady=5,padx=5)

deleteButton=CTkButton(buttonFrame,text='Delete Employee',font=('arial',15,'bold'),width=160,corner_radius=15,command=delete_employee)
deleteButton.grid(row=0,column=3,pady=5,padx=5)

deleteallButton=CTkButton(buttonFrame,text='Delete All',font=('arial',15,'bold'),width=160,corner_radius=15,command=delete_all)
deleteallButton.grid(row=0,column=4,pady=5,padx=5)

treeview_data() # thanks to that we can directly see the data if not we need to add 1 data then see all for function working
window.bind('<ButtonRelease>',selection) # <ButtonRelease>: Bir fare düğmesinin bırakılmasını ifade eden bir olay türüdür.



def update_id_entry(event):
    current_text = idEntry.get()
    if not current_text.startswith("EMP"):
        idEntry.delete(0, 'end')
        idEntry.insert(0, "EMP" + current_text)

# Kullanıcının her tuş girişinde bu işlevi çağırmak için bind metodu
idEntry.bind("<KeyRelease>", update_id_entry)

window.mainloop()    