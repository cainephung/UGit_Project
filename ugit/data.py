import hashlib
import os
from collections import namedtuple

GIT_DIR = '.ugit'
def set_HEAD(oid):
    with open(f'{GIT_DIR}/HEAD', 'w') as f:
        f.write(oid)

RefValue = namedtuple ('RefValue', ['symbolic', 'value'])

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
    ref_path = f'{GIT_DIR}/{ref}'
    value = None

    if os.path.isfile(ref_path):
        with open(ref_path) as f:
            value = f.read().strip()

    if value and value.startswith('ref:'):
        return get_ref(value.split(':', 1)[1].strip())  # Recursively dereference

    return RefValue (symbolic=False, value=value)


def update_ref (ref, value):
    assert not value.symbolic
    ref_path = f'{GIT_DIR}/{ref}'
    os.makedirs (os.path.dirname (ref_path), exist_ok=True)
    with open (ref_path, 'w') as f:
        f.write (value.value)

def iter_refs():
    refs = ['HEAD']
    for root, _, filenames in os.walk(f'{GIT_DIR}/refs/'):
        root = os.path.relpath(root, f'{GIT_DIR}/refs')
        refs.extend(f'{root}/{name}' if root != '.' else name for name in filenames)

    for refname in refs:
        full_refname = f'refs/{refname}' if refname != 'HEAD' else 'HEAD'
        ref_path = f'{GIT_DIR}/{full_refname}'
        val = get_ref(full_refname)
        print(f"[DEBUG] {full_refname} from {ref_path} => {val!r}")
        yield full_refname, val

