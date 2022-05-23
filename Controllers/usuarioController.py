import sys, os
sys.path.insert(0, os.path.abspath(os.getcwd()) + '/Model')
from model import Usuario, session
import datetime

def agregar(newUser):
    datetime.datetime.now()