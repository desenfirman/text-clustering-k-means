from flask import Flask, request, render_template, flash, g, session, redirect, url_for, Markup

app = Flask(__name__)

app.config.from_object('config')


@app.route('/')
def index():
    return render_template('default.html')


@app.route('/dashboard')
def dashboard():
    header = Markup("<script>activeSidebar('#menu_dashboard');</script>")
    return render_template('pages/dashboard.html', **locals())


@app.route('/input_teks')
def input_teks_view():
    header = Markup("<script>activeSidebar('#menu_input_teks');</script><h1>Input Teks</h1>")
    return render_template('pages/input_teks.html', **locals())


@app.route('/lihat_data_index')
def lihat_data_index_view():
    header = Markup("<script>activeSidebar('#menu_lihat_data_index');</script><h1>Lihat Data Index</h1>")
    return render_template('pages/lihat_data_index.html', **locals())


@app.route('/lakukan_clustering')
def lakukan_clustering_view():
    header = Markup("<script>activeSidebar('#menu_lakukan_clustering');</script><h1>Lihat Clustering</h1>")
    return render_template('pages/lakukan_clustering.html', **locals())


@app.route('/lihat_hasil_clustering')
def lihat_hasil_clustering_view():
    header = Markup("<script>activeSidebar('#menu_lihat_hasil_clustering');</script><h1>Lihat Hasil Clustering</h1>")
    return render_template('pages/lihat_hasil_clustering.html', **locals())




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

