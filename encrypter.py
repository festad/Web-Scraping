from aes_cipher import FileEncrypter

from pathlib import Path 

def recursive_encryption(key, path):
    p = Path(path)
    for el in p.iterdir(): 
        if el.is_dir():
            print(f'==> {el.name}')
            recursive_encryption(key, p.resolve().joinpath(el.name))
            print('<==')
        else:
            if el.name != 'encrypter.py' and el.name != 'decrypter.py':
                print(f'encrypting {el.name} ...')
                encrypt(key, el)
                print(f'done!')


def encrypt(key, path):
    try:
        file_encrypter = FileEncrypter()
        file_encrypter.Encrypt(path.resolve(), key)
        file_encrypter.SaveTo(path.resolve())
    except Exception as e:
        print(e)


if __name__ == '__main__':
    key = input('Insert the key\n-> ')
    path = Path('.')
    recursive_encryption(key, path)

