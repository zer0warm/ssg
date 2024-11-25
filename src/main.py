import os
import shutil

def copy_files(src, dst):
    print(f'Copying files from {src} to {dst}...')

    if not os.path.isdir(src):
        raise Exception(f'{src} does not exist in the current directory')

    if os.path.isdir(dst):
        print(f'{dst} exist, deleting...')
        shutil.rmtree(dst)
    if not os.path.isdir(dst):
        print(f'{dst} not exist, creating...')
        os.mkdir(dst)

    for file in os.listdir(src):
        entry = os.path.join(src, file)
        print(f'<> Processing {entry}...')
        if os.path.isdir(entry):
            print(f'--> is a directory')

            new_dst = os.path.join(dst, file)
            print(f'--> creating {new_dst}...')
            os.mkdir(new_dst)

            new_src = os.path.join(src, file)
            copy_files(new_src, new_dst)
        if os.path.isfile(entry):
            print(f'--> is a file')
            print(f'--> copying {entry} to {dst}...')
            shutil.copy(entry, dst)

def main():
    copy_files('./static', './public')

if __name__ == '__main__':
    main()
