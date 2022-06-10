# -*- coding: utf-8 -*-
import os
import shutil

docs_path = "docs"

def clean_index(path):
    for root, dirs, files in os.walk(path):
        if os.path.exists(os.path.join(root, "README.md")):
            os.remove(os.path.join(root, "README.md"))
        if os.path.exists(os.path.join(root, "_sidebar.md")):
            os.remove(os.path.join(root, "_sidebar.md"))


if __name__ == '__main__':
    clean_index('.')