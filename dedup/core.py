import os
import hashlib
from collections import defaultdict

def hash_file(filepath, blocksize=65536):
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            buf = f.read(blocksize)
            while buf:
                hasher.update(buf)
                buf = f.read(blocksize)
        return hasher.hexdigest()
    except (OSError, IOError):
        return None

def find_duplicates(root_dirs, skip_hidden=True):
    hashes = defaultdict(list)
    for root_dir in root_dirs:
        for dirpath, _, filenames in os.walk(root_dir):
            if skip_hidden and os.path.basename(dirpath).startswith('.'):
                continue
            for name in filenames:
                if skip_hidden and name.startswith('.'):
                    continue
                path = os.path.join(dirpath, name)
                if os.path.getsize(path) == 0:
                    continue
                h = hash_file(path)
                if h:
                    hashes[h].append(path)
    return {h: paths for h, paths in hashes.items() if len(paths) > 1}

def choose_to_keep(paths, strategy="newest"):
    key_func = os.path.getmtime if strategy == "newest" else os.path.getctime
    return max(paths, key=key_func) if strategy == "newest" else min(paths, key=key_func)

def delete_duplicates(duplicates, strategy="newest", dry_run=False):
    to_delete = []
    for paths in duplicates.values():
        keep = choose_to_keep(paths, strategy)
        for p in paths:
            if p != keep:
                to_delete.append(p)

    if dry_run:
        print("\n[Modo simulación] Se eliminarían:")
        for p in to_delete:
            print(f"  ❌ {p}")
        print(f"\nTotal: {len(to_delete)} archivos.")
        return to_delete

    print(f"\nSe van a eliminar {len(to_delete)} archivos.")
    print("Se conservará el más", "reciente" if strategy == "newest" else "antiguo", "de cada grupo.")
    confirm = input("¿Confirmar? (s/N): ").strip().lower()
    if confirm in ("s", "si", "yes"):
        for p in to_delete:
            try:
                os.remove(p)
                print(f"✅ Eliminado: {p}")
            except OSError as e:
                print(f"⚠️  Error: {e}")
    else:
        print("Operación cancelada.")
    return to_delete
