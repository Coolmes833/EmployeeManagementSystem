from customtkinter import *
from PIL import Image # pip install pillow yüklendi ve sonra image class eklendi burada.
from tkinter import messagebox # login olurken mesaj çıkması için bunu import etmek gerek

#function

def login(): # function then command ile logine ekledim. 
    if usernameEntry.get()=='' or passwordEntry.get()=='':
        messagebox.showerror('Empty Field Error','Complete all the required fields to login')
    elif usernameEntry.get()=='berkay' and passwordEntry.get()=='1234':
        messagebox.showinfo('Info','Login is successful')
        root.destroy() # login başarılı olduğu için sayfayı yok edip yeni sayfa olan alttaki kodla import ems'e gidecek
        import ems 
    else:
        messagebox.showerror('Login Error', 'wrong credentials')
    
#GUI part

root = CTk()          # Ana pencere oluşturuluyor
root.title("Employee Management System Login Page by Berkay [username: berkay, password: 1234]")  # Pencere başlığını ayarlıyoruz
root.geometry('930x478') # pencere büyüklüğü
root.resizable(0,0) # for blocking changing the size of window ( full screen is blocked )
root.configure(fg_color='orange')


# for placing the photo and more in below
image=CTkImage(Image.open('cover.jpg'),size=(930,478))
imageLabel=CTkLabel(root,image=image,text='')
imageLabel.place(x=120,y=0)

# Arka plan rengi ve çerçeve rengi
frame = CTkFrame(root, fg_color='#436D96')
frame.place(x=25, y=100)

# Çerçevenin içine yerleştirilen metin
headinglabel = CTkLabel(frame, text='Employee Management System', 
                        font=('Goudy Old Style', 20, 'bold'), 
                        text_color='#FAFAFA')
headinglabel.pack(padx=10, pady=5)  # Sağ ve sol kenarlardan 10 piksel boşluk, yukarı ve aşağıdan 5 piksel


usernameEntry=CTkEntry(root,placeholder_text=' Enter Your Username',width=180)
usernameEntry.place(x=25,y=150)

passwordEntry=CTkEntry(root,placeholder_text=' Enter Your Password',width=180,show='*')
passwordEntry.place(x=25,y=200)

loginButton=CTkButton(root,text='Login',fg_color='#436D96',cursor='hand2',text_color='#FAFAFA',command=login)
loginButton.place(x=25,y=250)


root.mainloop() # Pencereyi gösterme ve uygulamanın çalışmasını sağlama


