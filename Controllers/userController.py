import sys, os

sys.path.insert(0, os.path.abspath(os.getcwd()) + '/Model')

from model import Usuario
import datetime

def agregar(newUser):
    datetime.datetime.now()