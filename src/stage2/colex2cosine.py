import os.path

import pandas as pd
import numpy as np

import pickle
from sklearn.metrics import pairwise

from pandarallel import pandarallel

pandarallel.initialize(progress_bar=True)
from itertools import combinations

stage2 = "data/stage2"
stage1 = "data/stage1"


def load_graph(filepath):
    with open(filepath, "rb") as f:
        g = pickle.load(f)
    return g


# get frequencies of colex in each language from bible data
freq_graph = load_graph("/Users/yiyichen/Documents/experiments/CrossCoLEX/data/graphs/freq_graph.pickle")


def convert_colex2cosine(inputfile=f"{stage1}/glottocodes/colexnet_nuclear.csv",
                         outputfolder=f"{stage2}/colex2cosine", threshold=3):
    """
    Convert colexification occurrences to cosine similarity between languages...
    :param inputfile:
    :param outputfolder:
    :param threshold:
    :return:
    """
    df = pd.read_csv(inputfile)
    filename = os.path.basename(inputfile)
    colexs = sorted(list(set(df["COLEX"].tolist())))
    # if "Glottocode" in df.columns:
    #     langs = sorted(list(set(df["Glottocode"].tolist())))
    # else:
    langs = sorted(list(set(df["iso3"].tolist())))
    print(f"{inputfile}: colexes {len(colexs)}, langs {len(langs)}")

    # get an empty dataframe with colexificaiton patterns as columns, languages as rows.
    # lang2colex.at["ngal1298", "so~we"]=520
    # given a langauge and a colex pattern, show the frequency of it in bible data
    print("Building lang2colex dataframe ...")
    lang2colex = pd.DataFrame(columns=colexs, index=langs)

    counter = 0
    for iso3, colex in zip(df["iso3"], df["COLEX"]):
        t1, t2 = colex.split("~")
        if (t1, t2) in freq_graph.edges:
            freq = freq_graph.edges[t1, t2]["frequency"]
            if iso3 in freq:
                print(iso3, colex, freq[iso3])
                lang2colex.at[iso3, colex] = freq[iso3]
                counter += 1
    print(f"non-na values: ", counter)

    # filter the lang2colex dataframe with threshold
    # keep lang/colex with at least \threshold occurrences.
    print(f"Filtering lang2colex with threshold {threshold} ... ")
    colex_counter = {}
    lang_counter = {}
    for colex in colexs:
        colex_counter[colex] = len(lang2colex[colex].dropna())
    for lang in langs:
        lang_counter[lang] = len(lang2colex.loc[lang].dropna())

    colexs_remain = [colex for colex, freq in colex_counter.items() if freq >= threshold]
    langs_remain = [lang for lang, freq in lang_counter.items() if freq >= threshold]
    print(f"remaining langs {len(langs_remain)} and colex {len(colexs_remain)}")
    lang2colex = lang2colex[colexs_remain]
    lang2colex = lang2colex.loc[langs_remain]
    # fill na with 0
    lang2colex = lang2colex.fillna(0)

    # saving matrix
    matrix2file = os.path.join(outputfolder, "matrices", filename)
    print(f"saving lang2colex matrix to {matrix2file}..")
    lang2colex.to_csv(matrix2file)

    def colex2sim(l1, l2):
        """
        Caculate cosine similarity between language l1 and l2
        """
        vec1 = lang2colex.loc[l1].to_numpy().reshape(1, -1)
        vec2 = lang2colex.loc[l2].to_numpy().reshape(1, -1)
        cos = pairwise.cosine_similarity(vec1, vec2)[0][0]
        return cos

    langpairs = list(combinations(sorted(langs_remain), 2))
    print(f"language pairs {len(langpairs)}")
    print("Building a cosine edgelists ....")
    lang1s, lang2s = list(zip(*langpairs))
    df_cos = pd.DataFrame.from_dict({"source": lang1s, "target": lang2s})
    print(f"Calculating cosine similarity between {len(df_cos)} pair languages ...")
    df_cos["Cosine"] = df_cos.parallel_apply(lambda x: colex2sim(x.source, x.target), axis=1)

    # saving edgelist
    cos2file = os.path.join(outputfolder, "edgelists", filename)
    print(f"saving edgelist file to {cos2file}")
    df_cos.to_csv(cos2file, index=False)


if __name__ == '__main__':
    import plac

    plac.call(convert_colex2cosine)
