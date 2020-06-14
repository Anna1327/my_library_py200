from pathlib import Path

from tkinter import *
from tkinter import messagebox as mb
import os
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter.ttk as ttk
import json
import csv
import pandas as pd
from PIL import ImageTk, Image
from ttkthemes import ThemedTk
from dicttoxml import dicttoxml

from Baza_dannyh import *


class Mistakes:
    def __init__(self):
        ...

    @staticmethod
    def mistake_db_file():
        win_mistake_load_file = Toplevel(root)
        win_mistake_load_file.title("Ошибка")
        win_mistake_load_file.geometry('270x40')
        message = Label(win_mistake_load_file, text="Файл должен быть с расширением .db!", width=45, height=2)
        message.place(x=-30, y=0)

    @staticmethod
    def mistake_load_table():
        win_mistake_load_file = Toplevel(root)
        win_mistake_load_file.title("Ошибка")
        win_mistake_load_file.geometry('320x80')
        message = Label(win_mistake_load_file, text="Таблица не выбрана! \n "
                                                    "Сначала загрузите или создайте базу данных, \n "
                                                    "а затем выберите таблицу!", width=45, height=4)
        message.place(x=0, y=0)

    @staticmethod
    def mistake_del_table():
        win_mistake_del_table = Toplevel(root)
        win_mistake_del_table.title("Ошибка")
        win_mistake_del_table.geometry('350x40')
        message = Label(win_mistake_del_table, text="Эта таблица является системной и не может быть удалена!", width=45,
                        height=2)
        message.place(x=10, y=0)

    @staticmethod
    def mistake_enter_fields():
        win_mistake_enter_fields = Toplevel(root)
        win_mistake_enter_fields.title("Ошибка")
        win_mistake_enter_fields.geometry('200x40')
        message = Label(win_mistake_enter_fields, text="Сначала заполните все поля!", width=30, height=2)
        message.place(x=-5, y=0)

    @staticmethod
    def mistake_select_value():
        win5 = Toplevel(root)
        win5.title("Ошибка")
        win5.geometry('270x40')
        lbl12 = Label(win5, text="Сначала выберите значение из списка!", width=45, height=2)
        lbl12.place(x=-30, y=0)

    @staticmethod
    def mistake_not_found():
        win6 = Toplevel(root)
        win6.title("Ошибка")
        win6.geometry('270x40')
        lbl13 = Label(win6, text="Значение не найдено в базе данных!", width=45, height=2)
        lbl13.place(x=-30, y=0)

    @staticmethod
    def mistake_enter():
        win7 = Toplevel(root)
        win7.title("Ошибка")
        win7.geometry('320x60')
        lbl13 = Label(win7, text="Пожалуйста, нажмите ввод \n перед повторной выгрузкой данных!", width=45, height=4)
        lbl13.place(x=0, y=0)

    @staticmethod
    def mistake_load_csv():
        win8 = Toplevel(root)
        win8.title("Ошибка")
        win8.geometry('320x60')
        lbl13 = Label(win8, text="Убедитесь, что ваш .csv файл \n сохранен в кодировке UTF-8!", width=45, height=4)
        lbl13.place(x=0, y=0)


class Output(Mistakes, MyDataBase):
    def __init__(self):
        super().__init__()
        self.win_create_add_str = Text(root)
        self.win_create_delete_str = Text(root)
        self.win_create_update_str = Text(root)
        self.import_lst = []
        self.list_of_table = Listbox()
        self.data_base = ''
        self.table = ''
        self.new_data = []
        self.choice = ttk.Combobox()
        self.confirmation = Label()
        self.res = []
        self.search_delete_enter = ttk.Combobox()

    def clear_data_from_table(self):
        self.sqlite3_simple_clear_table(self.data_base, self.table)
        output_on_display.delete(1.0, END)
        output_on_display.insert(END, '')
        return

    def create_delete_entry(self, columns, win, x, y):
        window_for_search = Frame(win)
        window_for_search.place(x=x, y=y)
        self.search_delete_enter = ttk.Combobox(window_for_search, values=columns, height=3)
        self.search_delete_enter.set(u'Выбор параметра')
        self.search_delete_enter.grid(column=0, row=0)
        self.choice = self.search_delete_enter
        print(self.choice)
        return self.choice


class CreateNewDB(Output):
    def __init__(self):
        super().__init__()
        self.menu1 = Menu(root, tearoff=False)
        self.menu1.add_cascade(label="Создать новую базу данных", command=self.create_new_file_db)
        self.menu1.add_cascade(label="Создать новую таблицу", command=self.create_win_create_table)
        self.menu1.add_cascade(label="Удалить базу данных", command=self.delete_file_db)

        self.image1 = ImageTk.PhotoImage(file="pictures/ph.jpg")
        self.but1 = ttk.Menubutton(root, menu=self.menu1, image=self.image1)
        self.but1.place(x=0, y=0)

        self.win_create_table = Text()
        self.enter_table_name = Entry()
        self.enter_column_values = Entry()
        self.column_data = ''
        self.my_table = ''
        self.new_data = []
        self.column_names = []
        self.data = []

    def create_new_file_db(self):
        self.data_base = asksaveasfilename(title="Select file", filetypes=(("DATA BASE", "*.db"), ("all files", "*.*")),
                                           defaultextension='.db')

        if Path(self.data_base).suffix == '.db':
            self.create_win_create_table()
        else:
            self.mistake_db_file()

    def create_win_create_table(self):
        if self.data_base == '':
            self.mistake_load_table()
        else:
            self.win_create_table = Toplevel(root)
            self.win_create_table.title("Ввод")
            self.win_create_table.geometry('320x150')
            self.win_create_table.resizable(height=False, width=False)
            self.enter_table_name = Entry(self.win_create_table)
            self.enter_table_name.place(x=15, y=40, width=210)
            lbl2 = Label(self.win_create_table, text="Введите название таблицы: ")
            lbl2.place(x=10, y=10)
            enter_data_button = ttk.Button(self.win_create_table, text="  Ввод  ", command=self.get_create_data)
            enter_data_button.place(x=250, y=70)
            lbl3 = Label(self.win_create_table, text="Введите через запятую: Название книги, "
                                                     "\nИмя автора и Год публикации")
            lbl3.place(x=10, y=70)
            self.enter_column_values = Entry(self.win_create_table)
            self.enter_column_values.place(x=15, y=110, width=200)

    def get_create_data(self):
        self.table = self.enter_table_name.get()
        column_values = self.enter_column_values.get()
        self.win_create_table.destroy()
        self.column_data = column_values
        self.column_data = self.column_data.split(',')

        self.create_table(self.data_base, self.table, self.column_data)
        self.update_list_tables(self.data_base)

    @staticmethod
    def create_table(data_base, table, column_data):
        try:
            con = sqlite3.connect(data_base)
            cur = con.cursor()
            q = """
                CREATE TABLE {table} ( 
                  Name {txt}, 
                  Author {txt}, 
                  Published year {txt})
                """
            cur.execute(q.format(table=table, txt='TEXT'))
            cur.execute('INSERT INTO ' + table + ' VALUES(?, ?, ?)', column_data)
            con.commit()
            cur.close()
            con.close()
        except sqlite3.OperationalError:
            pass

    def update_list_tables(self, data_base):
        data_for_list_of_table = self.get_inform_from_db(data_base)
        self.list_of_table = Listbox(root, selectmode=SINGLE, height=7)
        but_load = ttk.Button(text="  Загрузить  ", command=self.output)
        for i in data_for_list_of_table:
            for j in i:
                self.list_of_table.insert(END, i)
                self.new_data.append(j)
        self.list_of_table.place(x=25, y=270)
        but_load.place(x=50, y=420)
        return self.new_data

    @staticmethod
    def get_inform_from_db(data_base):
        con = sqlite3.connect(data_base)
        cur = con.cursor()
        master = 'sqlite_master'
        query = "SELECT name FROM " + master + " WHERE type = 'table'"
        cur.execute(query)
        data = cur.fetchall()
        return data

    def del_table(self):
        try:
            self.sqlite3_simple_delete_table(self.data_base, self.table)
            list_tables = self.update_list_tables(self.data_base)
            list_tables.clear()
            output_on_display.delete(1.0, END)
            output_on_display.insert(END, '')
            return
        except sqlite3.OperationalError:
            self.mistake_del_table()

    def output(self):
        clear_table = ttk.Button(root, text="  Очистить таблицу  ", command=self.clear_data_from_table)
        delete_table = ttk.Button(root, text="  Удалить таблицу ", command=self.del_table)
        clear_table.place(x=30, y=460)
        delete_table.place(x=35, y=500)
        self.import_lst.clear()
        try:
            self.table = self.list_of_table.get(*self.list_of_table.curselection())
        except TypeError:
            pass

        if type(self.table) is tuple:
            self.table = str(self.table[0])
        self.data = self.sqlite3_simple_read_db(self.data_base, self.table)
        self.new_data = self.data[0]

        counter_row = 0
        for i in self.data:
            output_on_display.delete(1.0, END)

            for j in i:
                output_lst = list(j)
                self.import_lst.append(output_lst)
                output_on_display.insert(END, str(output_lst) + '\t')
                output_on_display.insert(END, '\n')
                counter_row += 1

            if not self.data[1]:
                output_on_display.delete(1.0, END)
                output_on_display.insert(END, "В таблице нет данных")
        self.create_delete_entry(self.data[0], root, 10, 210)

        try:
            self.win_create_add_str.destroy()
            self.win_create_delete_str.destroy()
            self.win_create_update_str.destroy()
        except AttributeError:
            pass
        counter_row -= len(self.data[0])
        text_message = f'Найдено колонок: {counter_row}'
        sum_rows = Label(root, text=text_message, width=20, height=1)
        sum_rows.place(x=15, y=570)
        print(f' data OUTPUT {self.data}')
        self.column_names = self.data[0]
        return self.data

    def delete_file_db(self):
        filename = askopenfilename(filetypes=(("DATA BASE", "*.db"), ("all files", "*.*")), defaultextension='.db')
        if Path(filename).suffix == '.db':
            answer = mb.askyesno(title="Вопрос", message="Вы действительно хотите удалить этот файл?")
            if answer is True:
                path = os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)
                os.remove(path)
                if filename == self.data_base:
                    self.data_base = ''
                    self.table = ''
                    output_on_display.delete(1.0, END)
                    self.search_delete_enter.delete(0, END)
                    self.list_of_table.delete(0, END)


class LoadTable(CreateNewDB):
    def __init__(self):
        super().__init__()
        self.image4 = ImageTk.PhotoImage(file="pictures/file_upload.jpg")
        self.but4 = ttk.Button(image=self.image4, command=self.load_file)
        self.but4.place(x=304, y=0)
        self.new_data_base = ''
        self.new_data = []

    def load_file(self):
        open_name = askopenfilename()
        if Path(open_name).suffix == '.db':
            self.data_base = open_name
            self.data_base = str(self.data_base)
            self.new_data_base = self.parse(self.data_base)
            self.new_data = self.update_list_tables(self.new_data_base)
            print(f'new data {self.new_data}')
            self.new_data.clear()

        else:
            self.mistake_db_file()

    def load_txt_file(self):
        if self.data_base == '':
            self.mistake_load_table()
        try:
            con = sqlite3.connect(self.data_base)
            cur = con.cursor()
            tet = []
            open_name = askopenfilename()
            if Path(open_name).suffix == '.txt':
                file_input = open(open_name, "r")
                for line in file_input:
                    if line == '\n':
                        pass
                    else:
                        lst = line.split()
                        tet.append(lst)
                table = 'load_txt'
                q = """
                                CREATE TABLE {table} ( 
                                  Name {txt}, 
                                  Author {txt}, 
                                  Published year {txt})
                                """
                cur.execute(q.format(table=table, txt='TEXT'))
                for i in tet:
                    cur.execute('INSERT INTO ' + table + ' VALUES(?, ?, ?)', i)
                con.commit()
                cur.close()
                con.close()
            self.update_list_tables(self.data_base)
        except sqlite3.OperationalError:
            pass

    def load_csv_file(self):
        if self.data_base == '':
            self.mistake_load_table()
        cnx = sqlite3.connect(self.data_base)
        file = askopenfilename()
        if Path(file).suffix == '.csv':
            try:
                df = pd.read_csv(file)
                df.to_sql('load_csv', cnx)
                self.update_list_tables(self.data_base)
            except UnicodeDecodeError:
                self.mistake_load_csv()

    def load_json_file(self):
        if self.data_base == '':
            self.mistake_load_table()
        file_name = askopenfilename()
        if Path(file_name).suffix == '.json':
            with open(file_name, 'r', encoding='utf-8') as file:
                data = json.load(file)
        con = sqlite3.connect(self.data_base)
        cur = con.cursor()
        table = 'load_json'
        q = """
                            CREATE TABLE {table} ( 
                              Name {txt}, 
                              Author {txt}, 
                              Published year {txt})
                            """
        cur.execute(q.format(table=table, txt='TEXT'))
        lst = []
        for i in data:
            d = dict(i)
            print(d)
            lst.append(d.values())

            cur.execute('INSERT INTO ' + table + ' VALUES(?, ?, ?)', [j for i in lst for j in i])
            lst.clear()
        con.commit()
        cur.close()
        con.close()
        self.update_list_tables(self.data_base)

    @staticmethod
    def parse(database_path):
        new_path = database_path.split("/")
        database_file_name = './' + new_path[-1]
        return database_file_name


class Download(LoadTable):
    def __init__(self):
        super().__init__()
        self.menu2 = Menu(root, tearoff=False)
        self.menu2.add_cascade(label="Выгрузить в .txt", command=self.save_txt_file)
        self.menu2.add_cascade(label="Выгрузить в .csv", command=self.save_csv_file)
        self.menu2.add_cascade(label="Выгрузить в .xml", command=self.save_xml_file)
        self.menu2.add_cascade(label="Выгрузить в .json", command=self.save_json_file)

        self.image6 = ImageTk.PhotoImage(file="pictures/file_download.jpg")
        self.but6 = ttk.Menubutton(root, menu=self.menu2, image=self.image6)
        self.but6.place(x=552, y=0)
        self.count = 0

    def save_txt_file(self):
        if self.data_base == '':
            self.mistake_load_table()
        else:
            print(f'Download data {self.data}')
            save_name = asksaveasfilename(title="Select file", filetypes=(("TXT", "*.txt"), ("all files", "*.*")),
                                          defaultextension='.txt')
            if Path(save_name).suffix == '.txt':
                data_txt = output_on_display.get('1.0', 'end')
                f = open(save_name, 'w')
                f.write(data_txt)
                f.close()

    def save_csv_file(self):
        if self.data_base == '':
            self.mistake_load_table()
        else:
            self.data = self.output()
            column_names = self.data[0]
            save_name = asksaveasfilename(title="Select file", filetypes=(("CSV", "*.csv"), ("all files", "*.*")),
                                          confirmoverwrite=True, defaultextension='.csv')
            step = len(column_names)
            print(self.import_lst)
            data_csv = self.import_lst
            if len(data_csv[0]) == step:
                pass
            else:
                data_csv = self.import_lst[step::]

            with open(save_name, 'w+') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(column_names)
                csv_writer.writerows(data_csv)

    def save_xml_file(self):
        if self.data_base == '':
            self.mistake_load_table()
        else:
            column_names = self.data[0]
            print(column_names)
            print(f' self.data {self.data}')
            step = len(column_names)

            save_name = asksaveasfilename(title="Select file", filetypes=(("XML", "*.xml"), ("all files", "*.*")),
                                          confirmoverwrite=True, defaultextension='.xml')
            data = self.import_lst
            try:

                if len(data[0]) == step:
                    pass
                else:
                    data = self.import_lst[step::]
            except IndexError:
                self.mistake_enter()

            data2 = list(map(list, zip(*data)))

            data3 = {key: value for key, value in zip(column_names, data2)}

            column = list(data3.keys())

            df = pd.DataFrame(data3, columns=column)

            data_dict = df.to_dict(orient="records")
            with open('output.json', "w+") as f:
                json.dump(data_dict, f, indent=4)

            xml_data = dicttoxml(data_dict).decode()
            with open(save_name, "w+") as f:
                f.write(xml_data)

            data.clear()
            data2.clear()
            data3.clear()

    def save_json_file(self):
        if self.data_base == '':
            self.mistake_load_table()
        else:
            column_names = self.new_data
            step = len(column_names)
            save_name = asksaveasfilename(title="Select file", filetypes=(("JSON", "*.json"), ("all files", "*.*")),
                                          confirmoverwrite=True, defaultextension='.json')
            data = self.import_lst
            print(f' data {data}')
            if len(data[0]) == step:
                pass
            else:
                data = self.import_lst[step::]

            data2 = list(map(list, zip(*data)))

            data3 = {key: value for key, value in zip(column_names, data2)}

            column = list(data3.keys())

            df = pd.DataFrame(data3, columns=column)

            data_dict = df.to_dict(orient="records")
            with open(save_name, "w+") as f:
                json.dump(data_dict, f, indent=4)

            data.clear()
            data2.clear()
            data3.clear()


class AddString(Download):
    def __init__(self):
        super().__init__()
        self.menu3 = Menu(root, tearoff=False)
        self.menu3.add_cascade(label="Добавить книгу в базу данных", command=self.create_enter_window)
        self.menu3.add_cascade(label="Загрузить книги из .txt в бд", command=self.load_txt_file)
        self.menu3.add_cascade(label="Загрузить книги из .csv в бд", command=self.load_csv_file)
        self.menu3.add_cascade(label="Загрузить книги из .json в бд", command=self.load_json_file)
        self.image3 = ImageTk.PhotoImage(file="pictures/add.jpg")
        self.but3 = ttk.Menubutton(root, menu=self.menu3, image=self.image3)
        self.but3.place(x=150, y=0)
        self.record = []
        self.enters_data = []

    def create_enter_window(self):
        try:
            self.column_names = self.data[0]
            self.win_create_add_str = Toplevel(root, relief=SUNKEN, bd=10, bg="light sky blue")
            self.win_create_add_str.title("Окно ввода")
            self.win_create_add_str.minsize(width=500, height=200)
            self.win_create_add_str.resizable(height=False, width=False)
            self.record = self.create_enter_entry(self.win_create_add_str)
            enter_data_button = ttk.Button(self.win_create_add_str, text="  Ввод  ", command=self.get_item)
            enter_data_button.place(x=400, y=33)
            update_button = ttk.Button(self.win_create_add_str, text="  Обновить  ", command=self.output)
            update_button.place(x=385, y=80)

        except IndexError:
            self.mistake_load_table()

    def create_enter_entry(self, window):
        count = len(self.column_names)
        x = 0
        y = 0
        width = 100
        height = 15
        while count != 0:
            for i in self.column_names:
                sign = Label(window, text=str(i), width=10, height=2, bg="light sky blue", fg="black", bd=10)
                sign.place(x=x, y=y)
                entry = Entry(window)
                entry.place(x=width, y=height, width=250)
                self.record.append(entry)
                count -= 1
                y += 33
                height += 33
        return self.record

    def get_item(self):
        remember_table = self.table
        self.enters_data.clear()
        for i in range(len(self.record)):
            try:
                a = self.record[i]
                b = a.get()
                self.enters_data.append(b)
                a.delete(0, END)
            except TclError:
                pass

        if '' in self.enters_data:
            self.mistake_enter_fields()

        if len(self.enters_data) > 1:
            self.add_record_table(self.enters_data)

        if remember_table != self.table:
            self.record.clear()

    def add_record_table(self, lst):
        con = sqlite3.connect(self.data_base)
        cur = con.cursor()
        cur.execute('INSERT INTO ' + self.table + ' VALUES (%s)' % ','.join('?' * len(lst)), lst)
        con.commit()
        cur.close()
        con.close()


class DeleteString(AddString):
    def __init__(self):
        super().__init__()
        self.image5 = ImageTk.PhotoImage(file="pictures/del.jpg")
        self.but5 = ttk.Button(image=self.image5, command=self.create_delete_window)
        self.but5.place(x=398, y=0)
        self.output1 = Text()
        self.place_for_enter = Entry()
        self.choice_row = []
        self.result = []

    def create_delete_window(self):
        try:
            self.column_names = self.data[0]
            self.win_create_delete_str = Toplevel(root, relief=SUNKEN, bd=10, bg="light sky blue")
            self.win_create_delete_str.title("Окно выбора данных")
            self.win_create_delete_str.minsize(width=500, height=300)
            self.win_create_delete_str.resizable(height=False, width=False)
            self.create_delete_entry(self.column_names, self.win_create_delete_str, 5, 10)
            enter_data_button = ttk.Button(self.win_create_delete_str, text="  Ввод  ", command=self.choice_of_param)
            enter_data_button.place(x=420, y=10)
            self.place_for_enter = Entry(self.win_create_delete_str)
            self.place_for_enter.place(x=150, y=10, width=250)
            self.output1 = Text(self.win_create_delete_str, width=40, height=10, font="12", wrap=WORD)
            self.output1.place(x=10, y=80)

            but_delete = ttk.Button(self.win_create_delete_str, text="  Удалить ", command=self.delete_record)
            but_delete.place(x=394, y=85)

            but_cancel = ttk.Button(self.win_create_delete_str, text="  Отмена  ", command=self.cancel)
            but_cancel.place(x=394, y=135)

            but_cancel = ttk.Button(self.win_create_delete_str, text="  Обновить  ", command=self.output)
            but_cancel.place(x=390, y=185)

        except IndexError:
            self.mistake_load_table()

    def delete_record(self):
        self.choice_row = self.choice.get()
        self.sqlite3_simple_delete_record(self.data_base, self.table, self.choice_row, self.res)
        self.output1.delete(1.0, END)
        self.confirmation.after(1, self.confirmation.destroy)
        self.place_for_enter.delete(0, END)

    def cancel(self):
        self.output1.delete(1.0, END)
        self.confirmation.after(1, self.confirmation.destroy)
        self.place_for_enter.delete(0, END)

    def choice_of_param(self):
        self.result = self.get_result_from_db()
        if self.result == 'Значение не найдено в базе данных!':
            self.output1.delete(1.0, END)
            self.mistake_not_found()

        self.output1.delete(1.0, END)
        if len(self.result) == 1:
            self.confirmation = Label(self.win_create_delete_str, text="Вы действительно хотите удалить эту строку?")
        elif len(self.result) > 1:
            self.confirmation = Label(self.win_create_delete_str, text="Вы действительно хотите удалить эти строки?")
        self.confirmation.place(x=15, y=40)
        for i in range(len(self.result)):
            self.output1.insert(END, self.result[i])
            self.output1.insert(END, '\n')
        return self.result

    def get_result_from_db(self):
        column_names = self.data[0]
        try:
            self.confirmation.after(1, self.confirmation.destroy)
        except AttributeError:
            pass
        self.choice_row = self.choice.get()
        self.res = self.place_for_enter.get()
        if self.choice_row in column_names:
            self.result = self.simple_search_from_db(self.data_base, self.table, self.choice_row, self.res)
            return self.result
        else:
            self.mistake_select_value()


class Update(DeleteString, AddString):
    def __init__(self):
        super().__init__()
        self.image7 = ImageTk.PhotoImage(file="pictures/images1.png")
        self.but7 = ttk.Button(image=self.image7, command=self.create_update_window)
        self.but7.place(x=645, y=0)
        self.count = 0
        self.my_lst = []
        self.choose = Entry()
        self.win_update_concurrence = Text()
        self.number_str = 0
        self.data = self.data
        self.zero = 0

    def test(self):
        print(f'test: {self.count}')
        self.count += 1

    def create_update_window(self):
        try:
            print(f' column_names: {self.column_names}')
            print(f' data: {self.data}')
            self.column_names = self.data[0]
            self.win_create_update_str = Toplevel(root, relief=SUNKEN, bd=10, bg="light sky blue")
            self.win_create_update_str.title("Окно выбора данных")
            self.win_create_update_str.minsize(width=500, height=300)
            self.win_create_update_str.resizable(height=False, width=False)
            self.create_delete_entry(self.column_names, self.win_create_update_str, 5, 10)
            enter_data_button = ttk.Button(self.win_create_update_str, text="  Ввод  ",
                                           command=self.choice_of_update_param)
            enter_data_button.place(x=420, y=10)
            self.place_for_enter = Entry(self.win_create_update_str)
            self.place_for_enter.place(x=150, y=10, width=250)

            self.output1 = Text(self.win_create_update_str, width=40, height=10, font="12", wrap=WORD)
            self.output1.place(x=10, y=80)

            but_update = ttk.Button(self.win_create_update_str, text="  Редактировать ", command=self.update_record)
            but_update.place(x=383, y=85)

            but_cancel = ttk.Button(self.win_create_update_str, text="  Отмена  ", command=self.cancel)
            but_cancel.place(x=398, y=135)

            but_cancel = ttk.Button(self.win_create_update_str, text="  Обновить  ", command=self.output)
            but_cancel.place(x=394, y=185)

        except IndexError:
            self.mistake_load_table()

    def choice_of_update_param(self):
        column_names = self.data[0]
        try:
            self.confirmation.after(1, self.confirmation.destroy)
        except AttributeError:
            pass
        self.choice_row = self.choice.get()
        self.res = self.place_for_enter.get()
        if self.choice_row in column_names:
            self.result = self.simple_search_from_db(self.data_base, self.table, self.choice_row, self.res)

            if self.result == 'Значение не найдено в базе данных!':
                output_on_display.delete(1.0, END)
                self.mistake_not_found()
            self.output1.delete(1.0, END)

            if len(self.result) == 1:
                confirmation = Label(self.win_create_update_str, text="Вы действительно хотите обновить эту строку?")
                confirmation.place(x=15, y=40)

            elif len(self.result) > 1:
                cnt = 1
                j = 0
                count = 0
                for w in range(len(self.result) - 1):
                    for i in range(len(self.result[0])):
                        if self.result[j][count] == self.result[cnt][count]:
                            count += 1
                        else:
                            self.my_lst.append(self.result[j][count])
                    j += 1
                    cnt += 1
                    self.zero = count

                self.confirmation = Label(self.win_create_update_str, text="Найдено более чем одно совпадение")
                self.find_more_one_str()

            for i in self.result:
                for j in i:
                    self.output1.insert(END, str(j) + '\n')
                self.output1.insert(END, '\n')
            return self.result
        else:
            self.mistake_select_value()

    def find_more_one_str(self):
        self.win_update_concurrence = Toplevel(self.win_create_update_str)
        self.win_update_concurrence.title("Выберите значение")
        self.win_update_concurrence.geometry('240x60')
        self.win_update_concurrence.resizable(height=False, width=False)
        lbl12 = Label(self.win_update_concurrence, text="Какую строку вы хотите обновить?", width=45, height=2)
        lbl12.place(x=-50, y=0)
        self.choose = Entry(self.win_update_concurrence)
        self.choose.place(x=15, y=30, width=50)
        enter_button1 = ttk.Button(self.win_update_concurrence, text="  Ввод  ", command=self.get_choose)
        enter_button1.place(x=100, y=30)
        self.confirmation.place(x=15, y=40)

    def get_choose(self):
        self.number_str = self.choose.get()
        self.result = self.result[int(self.number_str) - 1]
        self.output1.delete(1.0, END)
        for i in self.result:
            self.output1.insert(END, str(i) + '\n')
        self.confirmation.destroy()
        confirmation = Label(self.win_create_update_str, text='Измените строку и нажмите "Редактировать"')
        confirmation.place(x=15, y=40)
        self.win_update_concurrence.destroy()

    def update_record(self):
        a = self.output1.get('1.0', END)
        a = a[0:-1]
        changed_string = a.split('\n')
        changed_string = changed_string[0:-2]

        self.number_str = int(self.number_str) - 1
        source_string = []
        for i in self.result:
            for j in i:
                source_string.append(j)

        for i in range(0, 4):
            try:
                if changed_string[i] == source_string[i]:
                    pass
            except IndexError:
                pass
            else:
                param_value = changed_string[i]
                step = i
                param_column = self.column_names[step]
                self.sqlite3_update_record(self.data_base, self.table, param_column, param_value, self.choice_row,
                                           self.res)
        self.output1.delete(1.0, END)


class AddString(Update):
    def __init__(self):
        super().__init__()


class Search(Update):
    def __init__(self):
        super().__init__()
        enter_button = ttk.Button(text="  Ввод  ", command=self.choice_param_of_search)
        enter_button.place(x=800, y=155)

        enter_button = ttk.Button(text="  Отмена ", command=self.cancel_main)
        enter_button.place(x=795, y=200)

    def cancel_main(self):
        entry1.delete(0, END)
        output_on_display.delete(1.0, END)
        self.output()

    def choice_param_of_search(self):
        self.import_lst.clear()
        self.choice = self.search_delete_enter
        self.place_for_enter = entry1
        self.result = self.get_result_from_db()
        if self.result == 'Значение не найдено в базе данных!':
            output_on_display.delete(1.0, END)
            self.mistake_not_found()

        output_on_display.delete(1.0, END)
        counter_row = 0
        try:
            for j in self.result:
                lst = list(j)
                self.import_lst.append(lst)
        except TypeError:
            pass
        try:
            for i in range(len(self.result)):
                output_on_display.insert(END, str(self.import_lst[i]) + '\t')
                counter_row += 1
                output_on_display.insert(END, '\n')
        except TypeError:
            pass
        text_message = f'Найдено колонок: {counter_row}'
        sum_rows = Label(root, text=text_message, width=20, height=1)
        sum_rows.place(x=15, y=570)
        return self.result


class Help:
    def __init__(self):
        self.image8 = ImageTk.PhotoImage(file="pictures/help.png")
        self.but8 = ttk.Button(image=self.image8, command=self.create_help_window)
        self.but8.place(x=798, y=0)

        self.image_base = "test/base.png"
        self.help_window = Text()
        self.picture_lst = []
        self.my_iterator = []
        self.forward_button = ttk.Button()
        self.canvas = Canvas()

    def create_help_window(self):
        self.help_window = Toplevel(root, relief=SUNKEN, bd=10, bg="light sky blue")
        self.help_window.title("Справка")
        self.help_window.minsize(width=1000, height=550)
        self.help_window.resizable(height=False, width=False)
        main_win_button = ttk.Button(self.help_window, text="   Главное окно    ", command=self.help_main_but)
        main_win_button.place(x=20, y=50)
        add_db_table = ttk.Button(self.help_window, text="Добавить базу данных", command=self.help_add_db)
        add_db_table.place(x=10, y=120)
        add_string_button = ttk.Button(self.help_window, text=" Добавить строку ", command=self.help_add_str)
        add_string_button.place(x=15, y=190)
        load_file_button = ttk.Button(self.help_window, text="  Загрузить файл  ", command=self.help_load_file)
        load_file_button.place(x=20, y=260)
        del_string_button = ttk.Button(self.help_window, text="  Удалить строку   ", command=self.help_del_str)
        del_string_button.place(x=20, y=330)
        download_file_button = ttk.Button(self.help_window, text=" Выгрузить файл  ", command=self.help_download_file)
        download_file_button.place(x=20, y=400)
        update_string_button = ttk.Button(self.help_window, text=" Обновить строку ", command=self.help_update_str)
        update_string_button.place(x=20, y=470)

    def help_main(self):
        self.my_iterator = iter(self.picture_lst)
        pill_image = Image.open(self.image_base)
        image = ImageTk.PhotoImage(pill_image)

        self.canvas = Canvas(self.help_window, width=700 + 15, height=490 + 15)
        self.canvas.create_image(10, 10, anchor=NW, image=image)

        self.canvas.place(x=170, y=10)

        self.forward_button = ttk.Button(self.help_window, text=" Вперед ", command=self.forward)
        self.forward_button.place(x=910, y=250)
        self.help_window.mainloop()

    def help_main_but(self):
        self.picture_lst = ["test/main.png", "test/main2.jpg", "test/main3.jpg", "test/main4.jpg", "test/main5.jpg",
                            "test/main6.jpg"]
        self.help_main()

    def help_add_db(self):
        self.picture_lst = ["test/db1.jpg", "test/db2.jpg", "test/db3.jpg", "test/db4.jpg", "test/db5.jpg",
                            "test/db6.jpg", "test/db7.jpg", "test/db8.jpg", "test/db9.jpg", "test/db10.jpg"]
        self.help_main()

    def help_add_str(self):
        self.picture_lst = ["test/add1.jpg", "test/add2.jpg", "test/add3.jpg", "test/add4.jpg"]
        self.help_main()

    def help_load_file(self):
        self.picture_lst = ["test/load1.png", "test/load2.png", "test/load3.png", "test/load4.png"]
        self.help_main()

    def help_del_str(self):
        self.picture_lst = ["test/del1.jpg", "test/del2.jpg", "test/del3.jpg", "test/del4.jpg", "test/del5.jpg"]
        self.help_main()

    def help_download_file(self):
        self.picture_lst = ["test/download1.png", "test/download2.png", "test/download3.png", "test/download4.png",
                            "test/download5.png", "test/download6.png", "test/download7.png", "test/download8.png",
                            "test/download9.png", "test/download10.png", "test/download11.png", "test/download12.png",
                            "test/download13.png"]
        self.help_main()

    def help_update_str(self):
        self.picture_lst = ["test/update1.jpg", "test/update2.jpg", "test/update3.jpg", "test/update4.jpg",
                            "test/update5.jpg", "test/update6.jpg"]
        self.help_main()

    def forward(self):
        try:
            iterable = next(self.my_iterator)
            pill_image = Image.open(iterable)
            image = ImageTk.PhotoImage(pill_image)
            self.canvas.create_image(10, 10, anchor=NW, image=image)
            self.help_window.mainloop()
        except StopIteration:
            self.forward_button.destroy()


if __name__ == "__main__":

    root = ThemedTk()
    root.title("Добро пожаловать в приложение My library")
    root.geometry('895x600')
    root.resizable(height=False, width=False)
    root.set_theme('aquativo')
    background_root = PhotoImage(file="pictures/kls.png")
    Label(root, image=background_root).place(x=0, y=0)

    output_on_display = Text(root, width=60, height=20, font="12", wrap=WORD)
    output_on_display.place(x=230, y=200)

    entry1 = Entry(root)
    entry1.place(x=230, y=160, width=540)

    ram_for_list_of_table = Frame(width=155, height=300, bg="light sky blue", relief=SUNKEN, bd=10)
    ram_for_list_of_table.place(x=10, y=250)

    lbl1 = Label(root, text="Загрузите таблицу и \nвыберите параметры поиска", width=30, height=2)
    lbl1.place(x=-20, y=160)

    my_frame = Frame(root)
    my_frame.grid()
    CreateNewDB()
    LoadTable()
    Download()
    Update()
    AddString()
    Search()
    Help()
    root.mainloop()