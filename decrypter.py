from aes_cipher import FileDecrypter

from pathlib import Path 

def recursive_decryption(key, path):
    p = Path(path)
    for el in p.iterdir(): 
        if el.is_dir():
            print(f'==> {el.name}')
            recursive_decryption(key, p.resolve().joinpath(el.name))
            print('<==')
        else:
            if el.name != 'decrypter.py' and el.name != 'encrypter.py':
                print(f'decrypting {el.name} ...')
                decrypt(key, el)
                print(f'done!')


def decrypt(key, path):
    try:
        file_decrypter = FileDecrypter()
        file_decrypter.Decrypt(path.resolve(), key)
        file_decrypter.SaveTo(path.resolve())
    except Exception as e:
        print(e)


if __name__ == '__main__':
    key = input('Insert the key to decrypt:\n-> ')
    path = Path('.')
    recursive_decryption(key, path)
