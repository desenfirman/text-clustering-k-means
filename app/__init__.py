from flask import Flask, request, render_template, flash
from flask import g, session, redirect, url_for, Markup
import base64
import os
import re
from app.core.tf_idf import getFileListing, tokenize, buildIndex
from app.core.tf_idf import tfidfWeighting, getTitle
from app.core.k_means import k_means, avg_silhouette, silhouette_visualizer
import pandas as pd
from datetime import datetime
import json

app = Flask(__name__)

app.config.from_object('config')


@app.route('/')
def index():
    return render_template('pages/dashboard.html')


@app.route('/dashboard')
def dashboard():
    script = Markup("<script>activeSidebar('#menu_dashboard');</script>")
    return render_template('pages/dashboard.html', **locals())


@app.route('/input_berita', methods=['GET', 'POST'])
def input_berita():
    html_content = """
            <script>
                activeSidebar('#menu_input_berita');
            </script>
    """
    script = Markup(html_content)
    if request.method == 'POST':
        if request.form.get('title') is not None \
                and request.form.get('content') is not None:
            file_name = re.sub('[^A-Za-z]+', '-', request.form.get('title')
                               ).casefold()[:20] + '-' + \
                        str(base64.b64encode(bytes(
                            request.form.get('title'), 'utf-8')))[:10]
            file_content = request.form.get('title') + "\n\n" + \
                request.form.get('content')
            try:
                with open(os.path.abspath('app/static/article/' + str(
                        file_name) + '.txt'), 'w+') as file_handler:

                    file_handler.write(file_content)
                    submitted_message = Markup("""
                        <div class="alert alert-primary" role="alert">
                            Document submitted!
                        </div>
                    """)
            except (OSError, IOError) as exp:
                submitted_message = Markup(f"""
                        <div class="alert alert-danger" role="alert">
                            Error submitting document: {exp}
                        </div>
                    """)

    return render_template('pages/input_berita.html', **locals())


@app.route('/build_index_data', methods=['POST', 'GET'])
def build_index_data():
    html_content = """
        <script>
            activeSidebar('#menu_build_index_data');
        </script>
    """
    script = Markup(html_content)

    file_list = getFileListing(
                        os.path.abspath("app/static/article/"))
    file_list_name = list(map(getTitle, file_list))
    file_list_count = len(file_list)
    if request.method == 'POST' and request.form.get('submit') \
            and file_list_count > 0:

        term_dict = dict()
        term_dict = tokenize(file_list)
        index = buildIndex(term_dict)
        index_weighted = tfidfWeighting(index)
        index_weighted.to_pickle(os.path.abspath('app/index_data/data.pkl'))

    return render_template('pages/build_index_data.html', **locals())


@app.route('/lihat_data_index')
def lihat_data_index():
    html_content = """
        <script>
            activeSidebar('#menu_lihat_data_index');
        </script>
    """
    script = Markup(html_content)
    if os.path.exists("app/index_data/data.pkl"):
        index = pd.read_pickle("app/index_data/data.pkl")
        tables = [index.to_html(header="true", classes="table table-responsive\
            table-striped table-sm")]
    else:
        message = "Index doesn't exist. Please build an index first in 'Build \
            index data' before performing this task"
    return render_template('pages/lihat_data_index.html', **locals())


@app.route('/lakukan_clustering', methods=['POST', 'GET'])
def lakukan_clustering():
    html_content = """
        <script>
            activeSidebar('#menu_lakukan_clustering');
        </script>
    """
    script = Markup(html_content)
    message = None
    if request.method == 'POST':
        if request.form.get("k") and request.form.get("iterasi"):
            k = int(request.form.get("k"))
            iterasi = int(request.form.get("iterasi"))
            if os.path.exists("app/index_data/data.pkl"):
                index = pd.read_pickle("app/index_data/data.pkl")
                clusters = k_means(k, index, iterasi)
                clustering_date = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
                json_dict = {
                    "k": k,
                    "iterasi": iterasi,
                    "performed_at": clustering_date,
                    "cluster_result": clusters,
                    "avg_sil": avg_silhouette(index, clusters),
                    "graph": silhouette_visualizer(index, clusters)
                }
                with open(os.path.abspath('app/static/cluster_result/' + str(
                        clustering_date) + '.json'), 'w') as fp:
                    json.dump(json_dict, fp)
                    message = f"Clustering successful. You can check the\
                                result in 'Lihat Hasil Clustering' menu"

            else:
                message = "Index doesn't exist. Please build an index first in\
                     'Build index data' before performing this task"

            # print(k, iterasi)
        pass
    return render_template('pages/lakukan_clustering.html', **locals())


@app.route('/lihat_hasil_clustering/')
def lihat_hasil_clustering():
    result = None
    html_content = """
        <script>
            activeSidebar('#menu_lihat_hasil_clustering');
        </script>
    """
    script = Markup(html_content)
    file_list = getFileListing(
                        os.path.abspath("app/static/cluster_result/"))

    file_list = list(map(os.path.basename, file_list))
    return render_template('pages/lihat_hasil_clustering.html', **locals())


@app.route('/lihat_hasil_clustering/cluster/<file_name>')
def lihat_hasil_clustering_view(file_name):
    file_list = None
    html_content = """
        <script>
            activeSidebar('#menu_lihat_hasil_clustering');
        </script>
    """
    script = Markup(html_content)
    abs_path = os.path.abspath("app/static/cluster_result/" + file_name)
    if os.path.exists(abs_path):
        with open(abs_path, 'r') as fp:
            result = json.load(fp)
            result['cluster_result_title'] = list(
                map(lambda x: list(map(getTitle, list(
                    map(lambda file_name: os.path.abspath(
                        "app/static/article/" + file_name + '.txt'), x)
                ))),
                    result['cluster_result'])
            )
            # print(result)

    return render_template('pages/lihat_hasil_clustering.html', **locals())
