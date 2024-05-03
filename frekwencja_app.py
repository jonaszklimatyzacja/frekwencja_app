import json
import datetime
import asyncio
import os
import tkinter as tk
from vulcan import Keystore, Account, Vulcan

#Written by Jonasz Mielke

async def async_create_keystore():
    keystore = await Keystore.create()
    with open("keystore.json", "w") as f:
        f.write(keystore.as_json)


async def async_create_account(login):
    try:
        with open("keystore.json") as f:
            keystore = Keystore.load(f)

        #                                           token     symbol     PIN
        account = await Account.register(keystore, login[0], login[1], login[2])

        with open("account.json", "w") as f:
            f.write(account.as_json)
        
    except Exception as e:
        print("Logowanie nie powiodło się")
        return False
    
    return True


def create_account(login):
    if not os.path.exists("keystore.json"):
        asyncio.run(async_create_keystore())
        print()

    if asyncio.run(async_create_account(login)):
        return True
    else:
        return False
    
    
def show_login_window():
    root = tk.Tk()
    root.title("Logowanie")

    login_data = []

    def submit():
        login_data.append(entry1.get())
        login_data.append(entry2.get())
        login_data.append(entry3.get())
        root.destroy()

    label_header = tk.Label(root, text="Podaj dane logowania (dostęp mobilny)", font=("Helvetica", 14, "bold"))
    label_header.grid(row=0, column=0, columnspan=2, pady=10)

    label1 = tk.Label(root, text="Token:")
    label1.grid(row=1, column=0, padx=10, pady=10)
    entry1 = tk.Entry(root)
    entry1.grid(row=1, column=1, padx=10, pady=10)

    label2 = tk.Label(root, text="Symbol:")
    label2.grid(row=2, column=0, padx=10, pady=10)
    entry2 = tk.Entry(root)
    entry2.grid(row=2, column=1, padx=10, pady=10)

    label3 = tk.Label(root, text="PIN:")
    label3.grid(row=3, column=0, padx=10, pady=10)
    entry3 = tk.Entry(root)
    entry3.grid(row=3, column=1, padx=10, pady=10)

    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.grid(row=4, column=0, columnspan=2, pady=10)

    root.mainloop()

    return login_data


async def async_get_attendance(start, end):
    with open("keystore.json") as f:
        keystore = Keystore.load(f)
    
    with open("account.json") as f:
        account = Account.load(f)

    client = Vulcan(keystore, account)
    await client.select_student()
    attendance_raw = await client.data.get_attendance(date_from = start, date_to = end)
    attendance_data = []
    async for lesson in attendance_raw:
        attendance_data.append(lesson)

    await client.close()

    return attendance_data


class DataTable(tk.Frame):
    def __init__(self, master, data):
        super().__init__(master)
        self.data = data
        self.create_table()

    def create_table(self):
        num_rows = len(self.data)
        num_columns = len(self.data[0])

        for i in range(num_rows):
            for j in range(num_columns):
                cell_value = str(self.data[i][j])
                cell = tk.Entry(self, width=15, font=('Arial', 25))  
                cell.grid(row=j, column=i * 5)
                cell.insert(tk.END, cell_value)


def display_table(data):
    root = tk.Tk()
    root.title("Frekwencja względem jednostki")

    table = DataTable(root, data)
    table.pack(pady=10, padx=10)

    root.mainloop()



#--------------------------------------------------------------------------------------------------------------



if not os.path.exists("account.json"):
    login = show_login_window()
    if create_account(login) == False:
        print("Wystąpił błąd")
        exit()
    else:
        print("Połączenie z kontem powiodło się!")
        

datestart = datetime.datetime(2023, 9, 5)
dateend = datetime.datetime.today()

attendance = asyncio.run(async_get_attendance(datestart, dateend))

lekcje = []
for element in attendance:
    data = element.date.date.weekday()
    slot = element.time.position

    """
    TYP, ID
    obecność, 1
    spóźnienie, 4
    spóźnienie usprawiedliwione, 5
    nieobecny z przyczyn szkolnych, 6

    nieobecność, 2
    nieobecność usprawiedliwiona, 3
    """

    if element.presence_type != None:
        if element.presence_type and (element.presence_type.category_id == 1 or element.presence_type.category_id == 4 or element.presence_type.category_id == 5 or element.presence_type.category_id == 6):
            obecnosc = True
        else:
            obecnosc = False

        lekcja = {'dzien': data, 'nr_lekcji': slot, 'obecnosc': obecnosc}
        lekcje.append(lekcja)
    
    #return pattern: 
    #dzień tygodnia 0-6, zwykle 0-4 bo nie ma lekcji w weekendy
    #numer lekcji
    #czy obecność

#print(lekcje)

del attendance
del lekcja

laczne_lekcje = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
obecne = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]

for lekcja in lekcje:
    laczne_lekcje[lekcja['dzien']][lekcja['nr_lekcji']] += 1
    if lekcja['obecnosc'] == True:
        obecne[lekcja['dzien']][lekcja['nr_lekcji']] += 1

dni = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek"]

output = [["","7:10 - 7:55","8:00 - 8:45","8:50 - 9:35","9:50 - 10:35","10:40 - 11:25","11:30 - 12:15","12:30 - 13:15","13:20 - 14:05","14:10 - 14:55","15:00 - 15:45"]]

for i in range(5):

    kolumna = []
    kolumna.append(dni[i])
    for j in range(10):
        if(laczne_lekcje[i][j] != 0):
            kolumna.append(f"{round(obecne[i][j]/laczne_lekcje[i][j]*100, 2)}%")
        else:
            kolumna.append("")
            
    output.append(kolumna)

display_table(output)