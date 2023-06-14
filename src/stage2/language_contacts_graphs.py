import os
import json
import pickle

import pandas as pd
import numpy as np
import geopy.distance
from itertools import product
from tqdm import tqdm

from pandarallel import pandarallel

pandarallel.initialize(progress_bar=True)

import networkx as nx
from ast import literal_eval


def langauge_info(language_file):
    """
    Load language information
    :return: a dictionary of language information with glottocode as key.
    """
    df = pd.read_csv(language_file)
    df.index = df["iso639_3"]
    langdict = df.to_dict(orient="index")
    return langdict


def get_sim_field(lang1, lang2, graph, field):
    # branch, family, area
    # get value, if the same, otherwise 0 (different) and -1 (unknown)
    v1 = graph.nodes[lang1][field]
    v2 = graph.nodes[lang2][field]

    if str(v1) != "nan" and str(v2) != "nan":
        if v1 != v2:
            v = 0
        elif v1 == v2:
            v = v1
        else:
            v = -1

    else:
        v = -1
    return v


def load_geodesic_dict():
    df = pd.read_csv("data/stage1/lang2lang_geodesic.csv")
    df = df.dropna(subset=["ISO1", "ISO2"])
    lang2lang_dict = dict(zip(zip(df["ISO1"], df["ISO2"]), df["GeodesicDist"]))
    lang2lang_dict_sorted = {tuple(sorted(x)): y for x, y in lang2lang_dict.items()}
    return lang2lang_dict_sorted


def get_uriel_feature(feature, df):
    # GENETIC, SYNTACTIC
    file = f"/Users/yiyichen/Documents/experiments/LangSim/data/lang2vec_distances/{feature}.csv"
    df_feature = pd.read_csv(file, low_memory=False)

    def get_lang2vec_(x):
        t = x.split("_")
        if len(t) == 2:
            source, target = t
            try:
                d1 = df_feature.at[source, target]
                d2 = df_feature.at[target, source]
                d = (d1 + d2) / 2
                return d
            except Exception:
                return np.nan

    df_feature = df_feature.set_index("G_CODE")
    df["temp"] = df["LANG1"].str.cat(df["LANG2"], sep="_")
    df[feature.lower()] = df["temp"].parallel_apply(get_lang2vec_)
    return df


def load_word_dict(wordlist):
    df_word = pd.read_csv(f"data/stage2/colex2cosine/edgelists/colexnet_{wordlist}.csv")
    d = dict()
    for src, tgt, cos in zip(df_word["source_iso"], df_word["target_iso"], df_word["cosine"]):
        s, t = sorted((src, tgt))
        d[(s, t)] = cos
    return d


def load_phon_dist():
    df = pd.read_csv("data/stage1/pmiLanguageDistances.csv")
    df = df.dropna(subset=["ISO1", "ISO2"])
    d = dict()
    for src, tgt, cos in zip(df["ISO1"], df["ISO2"], df["PMI"]):
        s, t = sorted((src, tgt))
        d[(s, t)] = cos
    return d


def build_lang2geo_graph(ds="colexnet",
                         inputfolder="data/stage1/language_contact_colexnet",
                         language_file="data/languages/languages_colexnet.csv",
                         outputfolder="data/stage2/graphs/colex_geo"):
    print("Loading data....")
    langs = [x.replace(".json", "") for x in os.listdir(inputfolder) if x.endswith(".json")]
    outputfile = os.path.join(outputfolder, f"{ds}_geo_graph.pickle")
    langdict = langauge_info(language_file)

    lang2lang_dict_sorted = load_geodesic_dict()

    print("Building graphs...")
    g = nx.Graph()
    g.graph["dataset"] = "geo"
    g.graph["langs"] = len(langs)

    for lang in langs:  # isocode.
        node_dict = langdict[lang]  # geo information
        glotto_code = node_dict["id"]  # glottocode
        name = node_dict["name"]
        fam = node_dict["Family.wals"]
        genus = node_dict["Genus.wals"]
        parent = node_dict["parent_name"]
        branch = node_dict["branch"]
        lat = node_dict["latitude"]
        long = node_dict["longitude"]
        macroarea = node_dict["macroarea"]
        area = node_dict["Area.autotyp"]

        times = []
        if str(node_dict["timespan"]) != "nan":
            timespan = literal_eval(node_dict["timespan"])
            start_year = timespan["start_year"]
            times.append(start_year)
            end_year = timespan["end_year"]
            times.append(end_year)

        g.add_node(lang,
                   name=name,
                   family=fam,
                   genus=genus,
                   parent=parent,
                   branch=branch,
                   glottocode=glotto_code,
                   macroarea=macroarea,
                   area=area,
                   timespan=tuple(times),
                   coord=(lat, long))

    print("Building languages dataframe ...")
    lang1s = []
    lang2s = []
    cons = []
    for lang in tqdm(langs):
        with open(f"{inputfolder}/{lang}.json") as f:
            langd = json.load(f)

            for lang2, con in langd[lang].items():
                if con is not None:
                    lang1s.append(lang)
                    lang2s.append(lang2)
                    cons.append(con)
    df_lang = pd.DataFrame.from_dict({"LANG1": lang1s, "LANG2": lang2s, "ContactDist": cons})

    if ds == "colexnet":
        print("loading colexnet cosine similarity of languages....")
        d_emotion = load_word_dict("emotion_semantics")
        d_nuclear = load_word_dict("nuclear")
        d_peripheral = load_word_dict("peripheral")
        d_random = load_word_dict("random")
    elif ds == "phon":
        d_phon = load_phon_dist()
    else:
        # mix.
        d_emotion = load_word_dict("emotion_semantics")
        d_nuclear = load_word_dict("nuclear")
        d_peripheral = load_word_dict("peripheral")
        d_random = load_word_dict("random")
        d_phon = load_phon_dist()

    print("Write genetic feature...")
    get_uriel_feature("GENETIC", df_lang)
    print("Write syntactic feature ...")
    get_uriel_feature("SYNTACTIC", df_lang)

    print("Writing edges...")
    for lang, lang2, con, genetic, syntactic in tqdm(zip(df_lang["LANG1"], df_lang["LANG2"], df_lang["ContactDist"],
                                                         df_lang["genetic"], df_lang["syntactic"])):
        g.add_edge(lang, lang2)
        branch = get_sim_field(lang, lang2, g, "branch")
        genus = get_sim_field(lang, lang2, g, "genus")
        family = get_sim_field(lang, lang2, g, "family")
        macroarea = get_sim_field(lang, lang2, g, "macroarea")
        area = get_sim_field(lang, lang2, g, "area")

        l1, l2 = sorted([lang, lang2])
        distkm = lang2lang_dict_sorted[(l1, l2)]
        if con < 10:
            g.add_edge(lang, lang2, contact=con, geodist=distkm, neighbour=1, branch=branch, area=area,
                       family=family, genus=genus, macroarea=macroarea, syntactic=syntactic, genetic=genetic)
        else:
            g.add_edge(lang, lang2, contact=con, geodist=distkm, neighbour=0, branch=branch, area=area,
                       family=family, genus=genus, macroarea=macroarea, syntactic=syntactic, genetic=genetic)

        if ds != "phon":
            if (l1, l2) in d_emotion:
                g.edges[l1, l2]["emotion"] = d_emotion[(l1, l2)]
            if (l1, l2) in d_nuclear:
                g.edges[l1, l2]["nuclear"] = d_nuclear[(l1, l2)]
            if (l1, l2) in d_peripheral:
                g.edges[l1, l2]["peripheral"] = d_peripheral[(l1, l2)]
            if (l1, l2) in d_random:
                g.edges[l1, l2]["random"] = d_random[(l1, l2)]

        elif ds != "colexnet":
            if (l1, l2) in d_phon:
                g.edges[l1, l2]["phon"] = d_phon[(l1, l2)]

    g = g.to_undirected(as_view=True)
    print(f"langs {len(g.nodes)} - lang pairs {len(g.edges)}")
    print(f"writing the graph to {outputfile}")
    with open(outputfile, "wb") as f:
        pickle.dump(g, f)


if __name__ == '__main__':
    import plac

    plac.call(build_lang2geo_graph)
