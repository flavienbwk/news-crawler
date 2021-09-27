import os
import hashlib


def sha256_bytes(blob: bytes):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(blob)
    return sha256_hash.hexdigest()


def sha256_file(file_path: str):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as file_rs:
        for byte_block in iter(lambda: file_rs.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def sha256_string(hash_string: str) -> str:
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


def md5_string(hash_string: str) -> str:
    md5_signature = hashlib.md5(hash_string.encode()).hexdigest()
    return md5_signature


def minihash_file(file_path: str) -> str:
    size = os.path.getsize(file_path)
    mtime = os.path.getmtime(file_path)
    hash_string = f"{size}-{mtime}"
    with open(file_path, "rb") as f:
        hash_string += f.read(4096).decode("utf-8")
    return sha256_string(hash_string)
