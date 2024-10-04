import os
import shutil
import random
import hashlib
import argparse


def calculate_hash(filename, start, end):
    with open(filename, "rb") as f:
        f.seek(start)
        data = f.read(end - start)
    return hashlib.sha256(data).hexdigest()


def assert_files_equal(src, dst):
    assert os.path.exists(src) and os.path.isfile(src), f"[FileExist] src={repr(src)}"
    assert os.path.exists(dst) and os.path.isfile(dst), f"[FileExist] dst={repr(dst)}"

    size_src = os.path.getsize(src)
    size_dst = os.path.getsize(dst)
    assert size_src == size_dst, "[FileDiff] size"

    size = size_src

    if size < 1024 * 1024:
        start = 0
        end = size
        assert calculate_hash(src, start, end) == calculate_hash(dst, start, end), "[FileDiff] file hash"

    elif size < 1024 * 1024 * 16:
        start = 0
        end = round(size * 0.2)
        assert calculate_hash(src, start, end) == calculate_hash(dst, start, end), "[FileDiff] head hash"
        start = round(size * 0.2)
        end = size
        assert calculate_hash(src, start, end) == calculate_hash(dst, start, end), "[FileDiff] tail hash"

    else:
        start = 0
        end = round(size * 0.1)
        assert calculate_hash(src, start, end) == calculate_hash(dst, start, end), "[FileDiff] head hash"
        start = round(size * 0.9)
        end = size
        assert calculate_hash(src, start, end) == calculate_hash(dst, start, end), "[FileDiff] tail hash"
        start = round(size * random.randrange(0.1, 0.7))
        end = start + round(size * 0.2)
        assert calculate_hash(src, start, end) == calculate_hash(dst, start, end), "[FileDiff] random body hash"


def is_files_equal(src, dst):
    try:
        assert_files_equal(src, dst)
        return True
    except:
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=str)
    parser.add_argument("dst", type=str)
    args = parser.parse_args()

    args.src = os.path.realpath(args.src)
    args.dst = os.path.realpath(args.dst)

    for root, dirs, files in os.walk(args.src):
        root = os.path.realpath(root).replace(args.src, "").lstrip(os.path.sep)
        for file in files:
            src = os.path.join(args.src, root, file)
            dst = os.path.join(args.dst, root, file)
            if os.path.exists(dst) and os.path.isfile(dst):
                if not is_files_equal(src, dst):
                    print(f"flush {os.path.join(root, file)}")
                    shutil.rmtree(dst)
                    shutil.copytree(src, dst)
            else:
                print(f"dst file not exist {dst}")


if __name__ == "__main__":
    main()
