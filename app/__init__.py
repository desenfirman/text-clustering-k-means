from flask import Flask, request, render_template, flash, g, session, redirect, url_for

app = Flask(__name__)

app.config.from_object('config')


centroid = []
f_old = 0
f_new = 0


def init_dataset(some_dataset):
    return 0


def randomly_label_dataset():
    return 0


def init_centroid():
    return 0


def distance_from_centroid():
    return 0


def update_new_centroid():
    return 0


def delta_f():
    return 0

