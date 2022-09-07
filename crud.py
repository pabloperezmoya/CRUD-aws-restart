import hashlib
import json
import secrets


class DB:
    def __init__(self):
        self.file_name = 'db.json'
        f = open(self.file_name, 'a')
        f.close()

    def _fake_data(self, pref=False):
        return { 'nombre':secrets.token_hex(8), 'direccion':secrets.token_hex(8), 'email':secrets.token_hex(16), 'preferente':pref }

    def generate_dump_data(self, limit=1000):
        self.temp_data = dict()
        for i in range(limit):
            if i%2 == 0:
                preferente = True
            else:
                preferente = False
            
            print(i, self.add_client(self._fake_data(preferente), (True, i, limit)))
    
    def write_dump_data(self):
        with open(self.file_name, 'w') as file:
            json.dump(self.temp_data, file, indent=4)
            return 'Writed all clients!'

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
            return 'Not sufficient clients'
        
        file_data[id_cliente] = data
        with open(self.file_name, 'w') as file:
            json.dump(file_data, file, indent=4)
            return '\nClient updated'


    def show(self, client_preferente=False, client_nif=False):
        try:
            file_data = json.load(open(self.file_name, 'r'))
        except json.JSONDecodeError:
            file_data = {}
        
        if client_preferente:
            for id_cliente, dict_value in file_data.items():
                if dict_value['preferente'] == True:
                    print('-'.center(30, '-'))
                    print(f'NIF preferente: {id_cliente}'.center(30, ' '))
                    for key, value in dict_value.items():
                        print('>', key, ':', value)
            return

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
        return dk.hexdigest()

    def _check_if_exists(self, nif):
        try:
            file_data = json.load(open(self.file_name, 'r'))
            try:
                if file_data[nif]:
                    return True
            except KeyError:
                return False
        except json.JSONDecodeError: # means the file is empty
            return False


    def add_client(self, dictionary, batch=(False, 0, 0)):
        nif = str(self._generate_hash(dictionary['email']))
        
        if self._check_if_exists(nif):
            return 'Exists a client with that data'
        else:
            return self._append_data(nif, dictionary, batch)

    def _append_data(self, nif, data, batch):
        new_data = {nif:data}
        try:
            file_data = json.load(open(self.file_name, 'r'))
        except json.JSONDecodeError:
            file_data = {}
        
        if batch[0]:
            if batch[1] < batch[2]:
                self.temp_data = file_data | self.temp_data  | new_data
                return 'Added to cache'

        else:
            with open(self.file_name, 'w') as file:
                json.dump(file_data|new_data, file, indent=4)
                return 'Adding client'

    
def ask_data():
    lista_data = ['nombre', 'direccion', 'email', 'preferente']
    data = {}
    
    for element in lista_data:
        if element == 'preferente':
            inp = input(f'> {element.capitalize()} (True/False): ')
            if inp == 'False' or 'false' or '0':
                data[element] = False
            else:
                data[element] = True
            return data
        inp = input(f'> {element.capitalize()}: ')
        data[element] = inp
    

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
        print('[4] List Preferent Clients')
        print('[5] Delete Client')
        print('[6] Exit')
        
        inp = input('Choose: ')
        if inp == '1':
            data = ask_data()
            print(db.add_client(data))
        
        elif inp == '2':
            nif = input('Type NIF: ')
            data = ask_data()
            db.update(nif, data)
        
        elif inp == '3':
            nif = input('Show especific client? (type the NIF or leave it blank): ')
            if nif:
                db.show(client_id=nif)
            else:
                db.show()
                
        elif inp == '4':
            db.show(True)

        elif inp == '5':
            nif = input('Type the NIF: ')
            if nif:
                db.delete(nif)
        else:
            flag = False


if __name__ == '__main__':
    main()
