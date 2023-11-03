import requests


divider = ('='*100).center(100)
title = 'Target List'.center(100)
    
def header():
    print("\033[1H\033[2J", divider, title, divider, sep='\n')

def get_id():
    with open('targets.txt', 'r') as f:
        targets = f.read().splitlines()
        if len(targets) == 0:
            return 1
        else:
            last_id = targets[-1].split('||')[0]
            return int(last_id) + 1
D
def get_widest_data():
    max_id = 4
    max_name = 6
    max_age = 5
    max_address = 9
    max_phone = 7
    max_email = 7
    with open('targets.txt', 'r') as f:
        targets = f.read().splitlines()
        for i in targets:
            datas = i.split('||')
            if len(datas[0]) > max_id:
                max_id = len(datas[0])+2
            if len(datas[1]) > max_name:
                max_name = len(datas[1])+2
            if len(datas[2]) > max_age:
                max_age = len(datas[2])+2
            if len(datas[3]) > max_address:
                max_address = len(datas[3])+2
            if len(datas[4]) > max_phone:
                max_phone = len(datas[4])+2
            if len(datas[5]) > max_email:
                max_email = len(datas[5])+2
    return max_id, max_name, max_age, max_address, max_phone, max_email

def createdata():
    datas = requests.get('https://randomuser.me/api/?results=100&nat=us').json()['results']
    for i in datas:
        name = i['name']['first'] + ' ' + i['name']['last']
        age = i['dob']['age']
        address = str(i['location']['street']['number']) + ' ' + i['location']['street']['name'] + ', ' + i['location']['city'] + ', ' + i['location']['state'] + ', ' + i['location']['country'] + ', ' + str(i['location']['postcode'])
        phone = i['phone']
        email = i['email']
        with open('targets.txt', 'a+') as f:
            f.write(f"{get_id()}||{name}||{age}||{address}||{phone}||{email}\n")

def add_target():
    header()
    id = get_id()
    name = input('Enter your target name: ')
    age = input('Enter your target age: ')
    address = input('Enter your target address: ')
    phone = input('Enter your target phone number: ')
    email = input('Enter your target email: ')
    with open('targets.txt', 'a+') as f:
        f.write(f"{id}||{name}||{age}||{address}||{phone}||{email}\n")
    return 'success'

def view_targets():
    header()
    print()
    length = get_widest_data()
    with open('targets.txt', 'r') as f:
        targets = f.read().splitlines()
        print(''.ljust(length[0], '-'), ''.ljust(length[1], '-'), ''.ljust(length[2], '-'), ''.ljust(length[3], '-'), ''.ljust(length[4], '-'), ''.ljust(length[5], '-'), sep='+')
        print('ID'.ljust(length[0]), 'Name'.ljust(length[1]), 'Age'.ljust(length[2]), 'Address'.ljust(length[3]), 'Phone'.ljust(length[4]), 'Email'.ljust(length[5]), sep='|')
        print(''.ljust(length[0], '-'), ''.ljust(length[1], '-'), ''.ljust(length[2], '-'), ''.ljust(length[3], '-'), ''.ljust(length[4], '-'), ''.ljust(length[5], '-'), sep='+')
        for i in targets:
            datas = i.split('||')
            print(datas[0].ljust(length[0]), datas[1].ljust(length[1]), datas[2].ljust(length[2]), datas[3].ljust(length[3]), datas[4].ljust(length[4]), datas[5].ljust(length[5]), sep='|')

    return 'success'

def edit_target():
    header()
    target_id = input('Enter target id: ')
    with open('targets.txt', 'r') as f:
        targets = f.read().splitlines()
        for i in targets:
            datas = i.split('||')
            if datas[0] == target_id:
                print(f'Name: {datas[1]}')
                print(f'Age: {datas[2]}')
                print(f'Address: {datas[3]}')
                print(f'Phone: {datas[4]}')
                print(f'Email: {datas[5]}')
                print()
                new_name = input('Enter new name: ')
                new_age = input('Enter new age: ')
                new_address = input('Enter new address: ')
                new_phone = input('Enter new phone number: ')
                new_email = input('Enter new email: ')
                with open('targets.txt', 'w') as f:
                    for i in targets:
                        datas = i.split(',')
                        if datas[0] == target_id:
                            f.write(f"{datas[0]},{new_name},{new_age},{new_address},{new_phone},{new_email}\n")
                        else:
                            f.write(i+'\n')
                return 'success'
        return 'Target not found'


def remove_target():
    header()
    target_id = input('Enter target id: ')
    with open('targets.txt', 'r') as f:
        targets = f.read().splitlines()
        for i in targets:
            datas = i.split('||')
            if datas[0] == target_id:
                with open('targets.txt', 'w') as f:
                    for i in targets:
                        datas = i.split(',')
                        if datas[0] != target_id:
                            f.write(i+'\n')
                return 'Removed successfully'
        return 'Target not found'


while True:
    header()
    createdata()
    choices = ['Add Target', 'View Targets', 'Edit Target Info', 'Remove Target', 'Exit']
    for i in choices:
        print(f'[{choices.index(i)+1}]', i)
    selected = input('\nSelect an option: ')
    match selected:
        case '1':
            result = add_target()
        case '2':
            result = view_targets()
        case '3':
            result = edit_target()
        case '4':
            result = remove_target()
        case '5':
            print('Exiting...')
            break
        case _:
            print('Invalid option.')
            input('Press enter to continue...')
            continue
    
    print(result)
    input('Press enter to continue...')
