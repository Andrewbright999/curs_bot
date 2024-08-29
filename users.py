import pickle, os
from config import ADMIN_LIST

pikle_path = "user_data.pickle"

if not os.path.exists(pikle_path):
    data = ADMIN_LIST
    with open(pikle_path, "wb") as file:
        pickle.dump(data, file)
        
def write_data(data):
    with open(pikle_path, "wb") as file:
        pickle.dump(data, file) # записать сериализованные данные в jar
    
def read_data():
    with open(pikle_path, "rb") as file:
        data = pickle.load(file)
        print(data)
    return data


class UserList:
    '''Класс для работы с списком пользователем'''

    def __init__(self, user_id_list=None):
        if user_id_list is None:
            user_ids = read_data()
            self.user_id_list = user_ids
        else:
            self.user_id_list = user_id_list
    
    def check_user(self, user_id):
        if user_id in self.user_id_list:
            print("такой был")
        else:
            print(f"Новый {user_id}")
            self.append(user_id)

    def get_all_list(self):
        return self.user_id_list

    def __getitem__(self, key):
        # если значение или тип ключа некорректны, list выбросит исключение
        return self.user_id_list[key]

    def __setitem__(self, key, value):
        self.user_id_list[key] = value

    def __delitem__(self, key):
        del self.user_id_list[key]

    def __iter__(self):
        return iter(self.user_id_list)
    
    def __len__(self):
        return len(self.user_id_list)


    def append(self, value):
        self.user_id_list.append(value)
        write_data(self.user_id_list)


user_list = UserList()