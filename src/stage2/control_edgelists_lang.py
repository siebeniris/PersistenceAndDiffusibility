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

outputfolder = f"{stage2}/colex2cosine"

"""
To test gradual persistence and diffusibility, we need to control the number of colexification patterns 
and align the languages with the nuclear wordlist.
there is a tendency that with more colexification patterns, the beta is smaller comparing the language
 dissimilarity based on colex.

"""


def load_matrice(name):
    """
    Load colex~lang matrices, where the cells are the frequencies of colexifications in the lang.
    :param name: abstract_words/affective_abstract/affective_concrete/affective_extreme...
    :return:
    """
    m = pd.read_csv(f"{stage2}/colex2cosine/controlled_matrices/colexnet_{name}.csv", index_col=0)
    return m


def matrice2cosine_edgelists(name, outputfolder=outputfolder):

    lang2colex = load_matrice(name)
    def colex2sim(l1, l2):
        """
        Caculate cosine similarity between language l1 and l2
        """
        vec1 = lang2colex.loc[l1].to_numpy().reshape(1, -1)
        vec2 = lang2colex.loc[l2].to_numpy().reshape(1, -1)
        cos = pairwise.cosine_similarity(vec1, vec2)[0][0]
        return cos

    langs = list(lang2colex.index)
    langpairs = list(combinations(sorted(langs), 2))
    print(f"language pairs {len(langpairs)}")
    print("Building a cosine edgelists ....")
    lang1s, lang2s = list(zip(*langpairs))
    df_cos = pd.DataFrame.from_dict({"source": lang1s, "target": lang2s})
    print(f"Calculating cosine similarity between {len(df_cos)} pair languages ...")
    df_cos["Cosine"] = df_cos.parallel_apply(lambda x: colex2sim(x.source, x.target), axis=1)

    # saving edgelist
    outputfolder = os.path.join(outputfolder, "controlled_edgelists" )
    if not os.path.exists(outputfolder):
        os.makedirs(outputfolder)

    cos2file = os.path.join(outputfolder, f"colexnet_{name}.csv")
    print(f"saving edgelist file to {cos2file}")
    df_cos.to_csv(cos2file, index=False)


if __name__ == '__main__':
    import plac
    plac.call(matrice2cosine_edgelists)

