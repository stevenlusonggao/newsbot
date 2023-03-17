import json

def write_json(new_data, filename):
    with open(filename, 'r+') as file: #create copy of old json
        file_data = json.load(file)
        file.close()

    with open(filename, 'w') as file: #wipe old json
        json.dump({"log":[]}, file, indent = 4)
        file.close

    with open(filename, 'r+') as file: #maintain json data then paste to cleared json file
        for i in file_data['log']:
            if new_data['title'] == i['title']:
                json.dump(file_data, file, indent = 4)
                file.close()
                return False
        
        if len(file_data['log']) > 0:
            new_data['index'] = file_data['log'][0]['index'] + 1

        file_data['log'].insert(0, new_data)
        file.seek(0)

        if len(file_data['log']) > 250:
            del file_data['log'][-1]
            file.seek(0)
    
        json.dump(file_data, file, indent = 4)
        file.close()
    return True

