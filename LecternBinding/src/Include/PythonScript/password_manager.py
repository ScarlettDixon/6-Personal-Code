#!/usr/bin/env python3
# Author: Scarlett Dixon
# Date: 2023-11-25
# Version: 0.0.1
# Usage: import passwordManager
from cryptography.fernet import Fernet
from os import makedirs
from os.path import exists, join

class PasswordManager:

    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}
    
    def create_key(self, path):
        selk.key = Fernet.generate_key()
        with open(path, 'wb') as input_file:
            input_file.write(self.key)
    
    def load_key (self, path):
        with open(path, 'rb') as input_file:
            input_file.read()
    
    def create_password_file(self, path, filename, initial_values=None):
        self.password_file = path
        if not exists(path):
            makedirs(path)
        try:
            with open(join(path, filename), 'x') as fp:
                pass
        except:
            print('File already exists')
        for key, value in initial_values.items():
            self.add_password(key,value)

    def load_password_file(self, path):
        self.password_file = path
        with open(path, 'r') as input_file:
            for line in input_file:
                site, encrypted = line.split(":")
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()

    def add_password(self, site, password):
        self.password_dict[site] = password
        if self.password_file is not None:
            with open(self.password_file, 'a') as input_file:
                encrypted = Fernet(self.key).encrypt(password.encode())
                input_file.write(site + ":" + encrypted.decode() + "\n")

    def get_password(self, site):
        return self.password_dict[site]