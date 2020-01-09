import random as rd
import copy
import pandas as pd
import functools as ft
import numpy as np


def cosineSimilarity(doc_1, doc_2):
    sums = 0
    d_resultant_doc_1 = 0
    d_resultant_doc_2 = 0
    # print(doc_1)
    for row in doc_1.keys():
        sums += doc_1[row] * doc_2[row]
        d_resultant_doc_1 += (doc_1[row] * doc_1[row])
        d_resultant_doc_2 += (doc_2[row] * doc_2[row])
    return sums / (np.sqrt(d_resultant_doc_1) * np.sqrt(d_resultant_doc_2))


def centroidInitImproved(k, index_weighted):
    doc_list = [x for x in index_weighted]
    doc_couple = list(itertools.combinations(doc_list, 2))

    distance_sum = 0
    for doc_1, doc_2 in doc_couple:
        distance_sum += cosineSimilarity(
            index_weighted[doc_1], index_weighted[doc_2])

    mean_dist = distance_sum / len(doc_couple)
    return mean_dist


def distance(d1, d2):
    return 1 - cosineSimilarity(d1, d2)


def centroidInit(k, index_weighted):
    sampl = rd.sample(range(0, len(index_weighted.columns)),
                      k)

    selected_doc = [index_weighted.iloc[:, i] for i in sampl]
    return selected_doc


def updateCentroid(index_weighted, centroid, cluster_member):
    centroid = copy.deepcopy(centroid)
    new_cluster_member = copy.deepcopy(cluster_member)
    for c_id in range(len(centroid)):
        centroid[c_id] = (
            index_weighted[new_cluster_member[c_id]].mean(axis=1))
    # print(new_centroid)
    return centroid


def k_means(k, index_weighted, iterasi):
    centroid = centroidInit(k, index_weighted)

    t = 0
    while(t < iterasi):
        cluster_member = [[] for c in range(len(centroid))]
        doc_min_data = list()
        for doc_index in index_weighted:
            dst = list()
            for c in range(len(centroid)):
                d = distance(centroid[c], index_weighted[doc_index])
                dst.append(d)
            c_selected = dst.index(min(dst))
            cluster_member[c_selected].append(doc_index)
            doc_min_data.append(min(dst))
        # print(np.mean(doc_min_data))

        c_temp = updateCentroid(index_weighted, centroid, cluster_member)
        centroid = []
        centroid = c_temp

        t += 1
    return cluster_member


def silhouette(index_weighted, cluster_result):
    avg_silhouette = 0

    silhouette = dict()
    for cix, ci in enumerate(cluster_result):
        silhouette_cluster = dict()
        for i in ci:
            a = sum([distance(index_weighted[i], index_weighted[j])
                    if i != j else 0
                    for j in ci])
            a = 0 if len(ci) <= 1 else (a / (len(ci) - 1))

            cj_other_res = list()
            for cj in cluster_result:
                if ci != cj:
                    b_temp = sum(
                        [distance(index_weighted[i], index_weighted[j])
                         for j in cj]) / len(cj)
                    cj_other_res.append(b_temp)
            b = min(cj_other_res)
            sil = 0 if (len(ci) <= 1) else (b - a) / max(a, b)
            avg_silhouette += sil
            silhouette_cluster[i] = sil
        silhouette[cix] = sorted(
            silhouette_cluster.items(), key=lambda x: x[1]
        )
    silhouette['avg'] = avg_silhouette / index_weighted.shape[1]
    return silhouette


def avg_silhouette(index_weighted, cluster_result):
    return silhouette(index_weighted, cluster_result)['avg']


def silhouette_visualizer(index_weighted, cluster_result):
    silhouette_res = silhouette(index_weighted, cluster_result)
    import matplotlib.pyplot as plt
    import random as rd
    import base64
    from io import BytesIO

    img = BytesIO()

    fig, ax = plt.subplots(figsize=(8, 6))

    x = list()
    y = list()

    cmap = list()
    bcmap = list()
    count = 1
    for idj, cluster in silhouette_res.items():
        if idj != 'avg':
            r, g, b = (rd.random(), rd.random(), rd.random())
            random_color = (r, g, b, 1)
            random_bcolor = (r, g, b, 0.4)
            for i in cluster:
                x.append(i[1])
                y.append(count)
                cmap.append(random_color)
                bcmap.append(random_bcolor)
                count += 1

    ax.barh(y, x, color=cmap)
    ax.barh(y, [1] * len(x), color=bcmap)
    ax.get_yaxis().set_ticks([])
    ax.axvline(silhouette_res['avg'], ls='--', color='r')
    plt.text(silhouette_res['avg'], len(index_weighted) + 5,
             'avg silhouette: ' + str(round(silhouette_res['avg'], 2)))
    title = 'Silhouette Result of ' + str(len(silhouette_res) - 1) + \
            ' Cluster(s)\n\n'
    plt.title(title)
    plt.xlabel('Silhouette Score')
    plt.ylabel('Input dataset')

    plt.savefig(img, format='png')
    plt.close()

    img.seek(0)

    base64_bytes = base64.b64encode(img.getvalue())

    # Opt.: os.system("rm "+strFile)
    return base64_bytes.decode('utf-8')
