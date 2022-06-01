from contextlib import redirect_stderr
from unittest import result
from flask import Flask, redirect, url_for, jsonify
from flask import render_template
from flask import Response
from collections import Counter
from email.mime import image
from functools import total_ordering
import pickle
from types import coroutine

app = Flask(__name__)

@app.route("/")
def test():
    return render_template("login.html")

if __name__ == "__main__":
     app.run(debug=True)