import hashlib
import os


GIT_DIR = '.ugit'
def set_HEAD(oid):
    with open(f'{GIT_DIR}/HEAD', 'w') as f:
        f.write(oid)


def init ():
    os.makedirs (GIT_DIR)
    os.makedirs (f'{GIT_DIR}/objects')


def hash_object (data, type_='blob'):
    obj = type_.encode () + b'\x00' + data
    oid = hashlib.sha1 (obj).hexdigest ()
    with open (f'{GIT_DIR}/objects/{oid}', 'wb') as out:
        out.write (obj)
    return oid


def get_object (oid, expected='blob'):
    with open (f'{GIT_DIR}/objects/{oid}', 'rb') as f:
        obj = f.read ()

    type_, _, content = obj.partition (b'\x00')
    type_ = type_.decode ()

    if expected is not None:
        assert type_ == expected, f'Expected {expected}, got {type_}'
    return content

def get_HEAD():
    head_path = f'{GIT_DIR}/HEAD'
    if os.path.isfile(head_path):
        with open(head_path) as f:
            return f.read().strip()
    return None

def get_ref(ref):
    path = os.path.join(GIT_DIR, 'refs', ref) if ref != 'HEAD' else os.path.join(GIT_DIR, 'HEAD')
    if os.path.isfile(path):
        with open(path) as f:
            return f.read().strip()
    return None

def update_ref(ref, oid):
    if ref != 'HEAD':
        os.makedirs(os.path.join(GIT_DIR, 'refs'), exist_ok=True)
        path = os.path.join(GIT_DIR, 'refs', ref)
    else:
        path = os.path.join(GIT_DIR, 'HEAD')

    with open(path, 'w') as f:
        f.write(oid)

