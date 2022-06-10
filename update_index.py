# -*- coding: utf-8 -*-
import os
import shutil

docs_path = "docs"

def get_file_tree(path):
    file_tree = {}
    for root, dirs, files in os.walk(path):

        # 过滤文件
        try:
            files.remove("README.md")
            files.remove("_sidebar.md")
        except ValueError:
            pass
        files = [v for v in files if os.path.splitext(v)[-1] == '.md']

        temp = {}
        temp['name'] = root.split('\\')[-1]
        temp['path'] = root
        temp['dirs'] = {}
        temp['files'] = files

        p = file_tree
        try:
            for aaa in root.split('\\'):
                p = p[aaa]['dirs']
        except KeyError:
            p[temp['name']] = temp
    return file_tree


def write_README_md(root):
    content = []

    def write(root, depth):
        for name in root['dirs']:
            ppp =  os.path.join(root['dirs'][name]['path'], 'README.md')
            s = '  '*depth + '- ['+name+'](' + ppp + ')\n'
            content.append(s)
            content.append('\n')
            write(root['dirs'][name], depth+1)


        for file in root['files']:
            ppp =  os.path.join(root['path'], file)
            s = '  '*depth + '- ['+file+'](' + ppp + ')\n'
            content.append(s)
            content.append('\n')


    for k in root:
        content = []
        write(root[k], 0)
        with open(os.path.join(root[k]['path'], 'README.md'), 'w', encoding='utf-8') as f:
            f.writelines(content)
        write_README_md(root[k]['dirs'])

# 同 write_README_md, 只是改了个输出文件名字而已
def write__sidebar_md(root):
    content = []

    def write(root, depth):
        for name in root['dirs']:
            ppp =  os.path.join(root['dirs'][name]['path'], 'README.md')
            s = '  '*depth + '- ['+name+'](' + ppp + ')\n'
            content.append(s)
            content.append('\n')
            write(root['dirs'][name], depth+1)


        for file in root['files']:
            ppp =  os.path.join(root['path'], file)
            s = '  '*depth + '- ['+file+'](' + ppp + ')\n'
            content.append(s)
            content.append('\n')

    for k in root:
        content = []
        write(root[k], 0)
        with open(os.path.join(root[k]['path'], '_sidebar.md'), 'w', encoding='utf-8') as f:
            f.writelines(content)
        write__sidebar_md(root[k]['dirs'])


def rebuild_index():
    file_tree = get_file_tree(docs_path)
    write_README_md(file_tree)
    write__sidebar_md(file_tree)
    shutil.copy(os.path.join(docs_path, 'README.md'), 'README.md')
    shutil.copy(os.path.join(docs_path, '_sidebar.md'), '_sidebar.md')


if __name__ == '__main__':
    rebuild_index()