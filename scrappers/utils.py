import os
import json


def read_json_files(directory):
    file_list = []
    for filename in json_files(directory):
        with open(os.path.join(directory, filename), "r", encoding='utf-8') as file:
            file_list.append(json.load(file))
    return file_list


def json_files(directory):  # List JSON files in directory
    return [f for f in os.listdir(directory) if f.endswith('.json')]


def save_json(directory, data):
    # Get the highest numbered JSON file (to start where we stopped)
    highest_number = max(
        [int(f.split('.')[0]) for f in json_files(directory)],
        default=0
    )

    new_filename = f"{highest_number + 1}.json"
    with open(os.path.join(directory, new_filename), 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


keywords = [
    "çamur akıntısı", "çamur akması", "çamur hareketi", "heyelan", "kaya çökmesi", "kaya devrilmesi",
    "kaya düşmesi", "kaya hareketi", "kaya kayması", "kaya yuvarlanması", "moloz akıntısı", "moloz akması",
    "moloz hareketi", "toprak çökmesi", "toprak hareketi", "toprak kayması", "toprak sürüklenmesi", "yamaç kayması",
    "yer çökmesi", "yer hareketleri", "yer kayması", "zemin çökmesi", "zemin hareketi", "zemin kayması"
]

turkey_cities = [
    'adana', 'adıyaman', 'afyonkarahisar', 'ağrı', 'aksaray', 'amasya', 'ankara',
    'antalya', 'ardahan', 'artvin', 'aydın', 'balıkesir', 'bartın', 'batman',
    'bayburt', 'bilecik', 'bingöl', 'bitlis', 'bolu', 'burdur', 'bursa', 'çanakkale',
    'çankırı', 'çorum', 'denizli', 'diyarbakır', 'düzce', 'edirne', 'elazığ', 'erzincan',
    'erzurum', 'eskişehir', 'gaziantep', 'giresun', 'gümüşhane', 'hakkari', 'hatay',
    'ığdır', 'ısparta', 'istanbul', 'izmir', 'kahramanmaraş', 'karabük', 'karaman',
    'kars', 'kastamonu', 'kayseri', 'kırıkkale', 'kırklareli', 'kırşehir', 'kilis',
    'kocaeli', 'konya', 'kütahya', 'malatya', 'manisa', 'mardin', 'mersin', 'muğla',
    'muş', 'nevşehir', 'niğde', 'ordu', 'osmaniye', 'rize', 'sakarya', 'samsun',
    'şanlıurfa', 'siirt', 'sinop', 'sivas', 'şırnak', 'tekirdağ', 'tokat', 'trabzon',
    'tunceli', 'uşak', 'van', 'yalova', 'yozgat', 'zonguldak'
]
