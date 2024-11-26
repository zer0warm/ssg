import os
import shutil

from transformers import markdown_to_htmlnode
from helpers import extract_title

def copy_files(src, dst):
    print(f'Copying files from {src} to {dst}...')

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

def generate_page(template_path, src, dst):
    print(f'Generating page from {src} to {dst} using {template_path}...')

    with open(src) as f:
        markdown = f.read()

    with open(template_path) as f:
        template = f.read()

    html = markdown_to_htmlnode(markdown).to_html()
    title = extract_title(markdown)
    page = template.replace('{{ Title }}', title).replace('{{ Content }}', html)

    with open(dst, 'w') as f:
        if page[-1] != '\n':
            page += '\n'
        f.write(page)

    print('Done.')

def generate_pages_recursive(template_path, content_dir, dst_dir):
    for file in os.listdir(content_dir):
        entry = os.path.join(content_dir, file)
        if os.path.isdir(entry):
            new_dst = os.path.join(dst_dir, file)
            print(f'--> creating {new_dst}...')
            os.mkdir(new_dst)

            from_dir = os.path.join(content_dir, file)
            generate_pages_recursive(template_path, from_dir, new_dst)
        if os.path.isfile(entry):
            new_html_name = file.replace('.md', '.html')
            generate_page(template_path, entry, os.path.join(dst_dir, new_html_name))

def delete_files_recursive(directory):
    print(f'Deleting files in {directory}...')
    for file in os.listdir(directory):
        entry = os.path.join(directory, file)
        print(f'Processing {entry}...')
        if os.path.isdir(entry):
            delete_files_recursive(entry)
            print(f'Deleting {entry}...')
            os.rmdir(entry)
        else:
            print(f'Deleting {entry}...')
            os.remove(entry)
    print('Done.')

def main():
    src = 'static'
    dst = 'public'

    if not os.path.isdir(src):
        raise Exception(f'{src} does not exist in the current directory')

    if os.path.isdir(dst):
        print(f'{dst} exist, deleting...')
        delete_files_recursive(dst)
    if not os.path.isdir(dst):
        print(f'{dst} not exist, creating...')
        os.mkdir(dst)

    copy_files(src, dst)
    generate_pages_recursive('template.html', 'content', 'public')

if __name__ == '__main__':
    main()
