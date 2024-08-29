import os
import openpyxl

class TableField:
    def __init__(self, column_title: str, letter: str) -> None:
        self.column_title = column_title
        self.letter = letter

class FunctionalList:
    def __init__(self, **fields):
        for field_name, properties in fields:
            self.field_name = TableField(title = "id",
                letter = "A")   
        
        # self.id["title"] = "title"
        # self.fields = [{
        #     "name":
        #         {"title":
        #         },
        #     "email",
        #     "phone",
        #     "telegram",
        #     "check_in",
        #     "link",
        #     "block_bot",
        #     }]
        self.letters = []
        self.titles = []


    def __len__(self):
        return len(self.values)

    def __getitem__(self, key):
        # если значение или тип ключа некорректны, list выбросит исключение
        return self.values[key]

    def __setitem__(self, key, value):
        self.values[key] = value

    def __delitem__(self, key):
        del self.values[key]

class Workbook:
    def __init__(self) -> None:
        self.id = TableField(column_title = "id", letter = "A")

workbook = Workbook()
print(workbook.id.column_title)

class Workbook_Manager:
    def __init__(self, file_path: str):
        self.file_path = file_path     
        if not os.path.exists(leadbook_path):
            self.workbook = openpyxl.Workbook()
            self.workbook.create_sheet("Контакты лидов")
            sheet = self.workbook.active
            sheet["A1"] = "ФИО"
            sheet["B1"] = "Email"
            sheet["C1"] = "Телефон"
            sheet["D1"] = "Telegram"
            self.workbook.save(filename=leadbook_path)
        else:
            self.workbook = openpyxl.load_workbook(self.file_path)
            
    def write_user(self, name:str = "", email:str = "", contact:str = "", telegram:str = "", ):
        self.lead_sheet = self.workbook["Контакты лидов"]
        for cell in self.lead_sheet["D"]:
            if cell.value is None:
                first_unfilled_cell = cell
        first_unfilled_cell.value = telegram
        empty_row = first_unfilled_cell.row
        print()
        

leadbook_path = "leads.xlsx"

# leadbook = Workbook_Manager(leadbook_path)

# print(leadbook)

# leadbook.write_user(telegram="G")

fields_config = {
    "id": {
        "letter": "A",
        "title": "id"
        },
    "name": {
        "letter": "B",
        "title": "Имя"
        },
    "email": {
        "letter": "C",
        "title": "Email"
        },
    "phone": {
        "letter": "D",
        "title": "Телефон"
        },
    "telegram": {
        "letter": "E",
        "title": "Телеграм"
        },
    "check_in": {
        "letter": "F",
        "title": "Запись на вебинар"
        },
    "link": {
        "letter": "G", 
        "title": "Ссылка"
        },
    "block_bot": {
        "letter": "H",
        "title": "Бот заблокирован"
        }
}

leads_json_example = [{
    "id": 121232132,
    "name": "Андрей",
    "email": None,
    "telegram": "Bright099",
    "check_in": True,
    "link": "https://t.me/Bright099",
    "block_bot": False
    },
    {
    "id": 121232132,
    "name": "Андрей",
    "email": None,
    "telegram": "Bright099",
    "check_in": True,
    "link": "https://t.me/Bright099",
    "block_bot": False
    },
]

# for user in fields_config_json:
# for row in leads_json_example:
#     print(fields_config_json[row]["letter"])

# for i in fields_config_json:
#     print(fields_config_json[i]["title"])

# cell_val = sheet["A1"].value
# print(cell_val)
# cell_val = sheet.cell(row=2, column=1).value
# print(cell_val)


