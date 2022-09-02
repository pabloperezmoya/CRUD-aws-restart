import hashlib
import json


class DB:
    def __init__(self):
        self.file_name = 'db.json'

    def delete(self, id_cliente, force=None):
        if self._check_if_exists(id_cliente):
            self.show(id_cliente)
            if force == None:
                option = input('Are you sure?: Y/n: ')
                if option == 'Y':
                    try:
                        file_data = json.load(open(self.file_name, 'r'))
                        del file_data[id_cliente]
                        with open(self.file_name, 'w') as file:
                            json.dump(file_data, file, indent=4)
                            print('\nClient deleted')
                    except Exception as e:
                        print(e)
                        raise e
            else:
                try:
                    file_data = json.load(open(self.file_name, 'r'))
                    del file_data[id_cliente]
                    with open(self.file_name, 'w') as file:
                        json.dump(file_data, file, indent=4)
                        return True, 'Client deleted'
                except Exception as e:
                    print(e)
                    raise e
            
                
    def update(self, id_cliente, data):
        try:
            file_data = json.load(open(self.file_name, 'r'))
        except json.JSONDecodeError:
            file_data = {}
            print('\nNot sufficient clients')
        
        file_data[id_cliente] = data
        with open(self.file_name, 'w') as file:
            json.dump(file_data, file, indent=4)
            print('\nClient updated')


    def show(self, client_nif=False):
        try:
            file_data = json.load(open(self.file_name, 'r'))
        except json.JSONDecodeError:
            file_data = {}
        
        if client_nif:
            print('-'.center(30, '-'))
            print(f'NIF: {client_nif}'.center(30, ' '))
            for key, value in file_data[client_nif].items():
                print('>', key, ':', value)
            
        else:
            for id_cliente, dict_value in file_data.items():
                print('-'.center(30, '-'))
                print(f'NIF: {id_cliente}'.center(30, ' '))
                for key, value in dict_value.items():
                    print('>', key, ':', value)


    def _generate_hash(self, secret):
        dk = hashlib.sha256()
        s = secret + 'AWS'
        dk.update(s.encode('utf-8'))
        return dk.hexdigest()[0:5]

    def _check_if_exists(self, nif):
        try:
            file_data = json.load(open(self.file_name, 'r'))
            if file_data[nif]:
                return True
        except KeyError:
            return False


    def add_client(self, dictionary):
        nif = str(self._generate_hash(dictionary['email']))
        
        if self._check_if_exists(nif):
            return False, 'Exists an client with that data'
        self._append_data(nif, dictionary)

    def _append_data(self, nif, data):
        new_data = {nif:data}
        try:
            file_data = json.load(open(self.file_name, 'r'))
        except json.JSONDecodeError:
            file_data = {}

        with open(self.file_name, 'w') as file:
            json.dump(file_data|new_data, file, indent=4)
            return True, 'Adding client'

    


#a = DB()
#a.delete('fa55b', force=True)
#a.update('fa55b',{"nombre": "Enrique", "direccion": "Casablanca", "email": "casablanca@email.com", "preferente": True})

#print(a.add_client({"nombre": "Pablo", "direccion": "Las erdjf 123", "email": "ppm@email.com", "preferente": True}))
#a.add_client({"nombre": "oeoe", "direccion": "Ldsfsdfds", "email": "qq@email", "preferente": False})

#client1 = {"nombre": "Pablo", "direccion": "Las erdjf 123", "email": "ppm@email.com", "preferente": True}
#client2 = {"456": {"nombre": "oeoe", "direccion": "Ldsfsdfds", "email": "qq@email", "preferente": False}}

def ask_data():
    lista_data = ['nombre', 'direccion', 'email', 'preferente']
    data = {}
    
    for element in lista_data:
        if element == 'preferente':
            tem_inp = bool(input(f'> {element.capitalize()}: (True/False)'))
            if tem_inp == 'False' or 'false' or '0':
                data[element] = False
            else:
                data[element] = True
        tem_inp = input(f'> {element.capitalize()}: ')
        data[element] = tem_inp
    return data

def main():
    print('\n')
    print('Client-Managaer'.center(30, '-'))

    db = DB()

    flag = True
    while flag:
        print('\n')
        print('[1] Create Client')
        print('[2] Update Client')
        print('[3] List Clients')
        print('[4] Delete Client')
        print('[5] Exit')
        
        inp = input('Choose: ')
        if inp == '1':
            data = ask_data()
            db.add_client(data)
        elif inp == '2':
            nif = input('Type NIF: ')
            data = ask_data()
            db.update(nif, data)
        elif inp == '3':
            nif = input('Show especific client? (type the NIF or leave it blank): ')
            if nif:
                db.show(nif)
            else:
                db.show()
        elif inp == '4':
            nif = input('Type the NIF: ')
            if nif:
                db.delete(nif)
        else:
            quit()


if __name__ == '__main__':
    main()
    