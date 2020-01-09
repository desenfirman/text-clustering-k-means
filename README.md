# K-Means News Clustering

A Part of Final Project Text Mining Course

## What inside repository?

Below are the structure of the following repository:

```text
text-clustering-k-means/
    app/
        core/               # submodule for tf_idf and k_means
            k_means.py
            tf_idf.py
        index_data/         # builded index data stored here
            data.pkl
        static/
            article/        # News data from user input stored here
            cluster_result/ # Result of clustering task directory
                ...-.json
            css/
            js/
        templates/          # .html's Flask templates
            ...-.html
        __init__.py         # Flask routes
    test/
        sample_corpus/      # sample corpus for algorithm validation
            1.txt
            ...-.txt
        k_means_test.py     # algorithm test validation for k_means
        tf_idf_test.py      # algorithm test validation for tf_idf
    config.py               # Flask app config
    README.md
    requirements.yml        # Conda requirements
    run.py                  # Flask main app to run
    scratch.py              # Just a scratch for testing core algorithm
```

## Prerequisites

- Git
- Python in Conda Environment

## Set-up

1. Clone this repository into your machine

    ```bash
    git clone https://github.com/desenfirman/text-clustering-k-means.git
    cd text-clustering-k-means
    ```

2. Set up conda environment for this project.

    ```bash
    conda env create -f requirements.yml
    ```

3. Wait for download and installation package completed.
4. After installation completed, run this command to start a Flask webserver.

    ```bash
    python run.py
    ```

5. Access localhost:8080 to your browser and you're ready to use this app.

## A quick demo

1. You need to input a news data into the system.

   ![Input a news data](https://i.imgur.com/NiayPCh.gif)

2. But, before clustering task is performed. You need to build a TF-IDF index first in 'Build index data' menu

   ![Indexing task may performed a little bit slowly. It depends on your machine too](https://i.imgur.com/C18p8lu.gif)

3. You can check what inside the index data before clustering task is performed.

   ![Index data example](https://i.imgur.com/2p5DQRx.gif)

4. On 'Lakukan Clustering' menu, input following parameter before performing a K-means clustering task.

   ```text
   K        =   [number of cluster do you want]
   Iterasi  =   [number maximun iteration in k-means clustering task]
   ```

   ![Input a K-means clustering parameters](https://i.imgur.com/8Rpy8yb.gif)

5. You can check the result of clustering in 'Lihat hasil clustering' menu. The clustering result will show Group of news with a Silhouette Score and Silhoutte Graph

   ![Clustering report](https://i.imgur.com/Pt0BfAJ.gif)

## Credit(s)

You can check it on `requirements.yml` file to see what package that I used. Briefly, I used this following packages:

```text
1. flask        :   A basic Python webserver
2. pandas       :   Python packages for data manipulation and analysis.
                    (I used only Dataframe submodule to storing an index data)
3. matplotlib   :   Python packages for data visualization
4. numpy        :   Python packages for calculation and mathematics operation.
5. sastrawi     :   A Bahasa Indonesia word stemmer in Python libs.
```
