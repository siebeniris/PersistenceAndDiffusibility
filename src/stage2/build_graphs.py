import pandas as pd
from tqdm import tqdm
import networkx as nx
import pickle

stage1 = "data/stage1"
stage2 = "data/stage2"


def load_geo_graph():
    """
    Loading graph for geo contact and geodesic info.
    :return: graph.
    """
    with open(f"{stage1}/language_geo_graph.pickle", "rb") as f:
        graph = pickle.load(f)
    print(f"geo: {len(graph.nodes)} languages")
    return graph


def load_phon_dict():
    """
    Load phon PMI information
    :return: the dictionary of pairs of languages with their phon pmi, list of languages
    """
    df_phon = pd.read_csv(f"{stage1}/pmiLanguageDistances.csv", sep="\t")
    df_phon = df_phon.dropna(subset=["Glottocode1", "Glottocode2", "PMI"])
    phon_dict = dict()

    langs = []
    for lang1, lang2, pmi in zip(df_phon["Glottocode1"], df_phon["Glottocode2"], df_phon["PMI"]):
        l1, l2 = sorted([lang1, lang2])
        if l1 != l2:  # small languages use the same glottocodes
            phon_dict[(l1, l2)] = pmi
            langs.append(l1)
            langs.append(l2)

    return phon_dict, set(langs)


def load_colex_dict(ds, wordlist):
    """
    Load colex information
    :param ds: clics3, colexnet, wn, colex_all_dedup
    :param wordlist: nuclear, peripheral, emotion_semantics
    :return: dictionary of word pairs with pmi
    """

    df = pd.read_csv(f"{stage1}/colex_pmi/{ds}_{wordlist}.csv")
    print(f"reading {ds} -> {wordlist}")
    df_pmi = df[["source", "target", "weight", "target_nr", "source_nr", "pmi"]]

    colex_nr_dict = dict()
    for source, target, source_nr, target_nr in zip(df_pmi["source"], df_pmi["target"], df_pmi["source_nr"],
                                                    df_pmi["target_nr"]):
        if source not in colex_nr_dict:
            colex_nr_dict[source] = source_nr
        if target not in colex_nr_dict:
            colex_nr_dict[target] = target_nr

    colex_dict = dict()

    for source, target, weight, pmi in zip(df_pmi["source"], df_pmi["target"], df_pmi["weight"], df_pmi["pmi"]):
        t1, t2 = sorted([source, target])
        colex_dict[(t1, t2)] = (weight, pmi)

    print("colex pairs: ", len(colex_dict), "len languages: ", len(colex_nr_dict))
    return colex_nr_dict, colex_dict, set(colex_nr_dict.keys())


def build_colex_geo_graph(ds, wordlist):
    """
    Build graph for colex and geo.
    :param ds: colexnet, wn, clics3, colex_all_dedup
    :param wordlist: nuclear, peripheral, emotion_semantics
    :return: None
    """
    print(f"Building colex {ds}-{wordlist} geo graph....")
    geo_graph = load_geo_graph()
    colex_nr_dict, colex_dict, colex_langs = load_colex_dict(ds, wordlist)
    inter_langs = set(geo_graph.nodes).intersection(colex_langs)

    g = nx.Graph()
    g.graph["dataset"] = f"{ds}_{wordlist}"
    g.graph["langs"] = len(inter_langs)

    for lang in tqdm(inter_langs):

        geo_dict_node = geo_graph.nodes[lang]
        # add colex number for the language.
        g.add_node(lang, colex_nr=colex_nr_dict[lang])
        # add geo information for the node.
        for k, v in geo_dict_node.items():
            g.nodes[lang][k] = v

    for langp, colex_pmi_ in colex_dict.items():
        l1, l2 = langp
        weight, pmi = colex_pmi_
        if l1 in inter_langs and l2 in inter_langs:
            g.add_edge(l1, l2, colex_pmi=pmi, weight=weight)
            geo_dict_edge = geo_graph.edges[l1, l2]
            for k, v in geo_dict_edge.items():
                g.edges[l1, l2][k] = v

    outputfile = f"{stage2}/graphs/colex_geo/{ds}-{wordlist}.pickle"
    print(f"written to .. {outputfile}")
    with open(outputfile, "wb") as f:
        pickle.dump(g, f)


def build_phon_geo_graph():
    """
    Build phon geo graph.
    :return: None
    """
    print("Building phon geo graph....")
    geo_graph = load_geo_graph()
    phon_dict, langs = load_phon_dict()
    inter_langs = set(geo_graph.nodes).intersection(langs)
    lang_len = len(inter_langs)
    print(f"working on {lang_len} languages ")

    g = nx.Graph()
    # add graph attributes
    g.graph["dataset"] = "phon"
    g.graph["langs"] = lang_len

    # add nodes from geo graph. all the geo information
    # name, family, parent, branch, iso3, area, timespan, coords,
    for lang in tqdm(inter_langs):
        geo_dict_node = geo_graph.nodes[lang]

        g.add_node(lang)
        for k, v in geo_dict_node.items():
            g.nodes[lang][k] = v

    for langp, phon_pmi in phon_dict.items():
        l1, l2 = langp
        if l1 in inter_langs and l2 in inter_langs:
            g.add_edge(l1, l2, phon_pmi=phon_pmi)
            geo_dict_edge = geo_graph.edges[l1, l2]
            for k, v in geo_dict_edge.items():
                g.edges[l1, l2][k] = v

    outputfile = f"{stage2}/graphs/phon_geo_graph.pickle"
    print(f"written to{outputfile}")
    with open(outputfile, "wb") as f:
        pickle.dump(g, f)


def build_phon_colex_geo_graph(ds, wordlist):
    print("Building phon colex geo graph....")
    geo_graph = load_geo_graph()
    phon_dict, phon_langs = load_phon_dict()
    colex_nr_dict, colex_dict, colex_langs = load_colex_dict(ds, wordlist)
    inter_langs_ = set(geo_graph.nodes).intersection(colex_langs)
    inter_langs = inter_langs_.intersection(phon_langs)

    print(f"working on {len(inter_langs)} languages")

    g = nx.Graph()
    g.graph["dataset"] = f"{ds}_{wordlist}_colex_phon_geo"
    g.graph["langs"] = len(inter_langs)
    # add nodes from geo graph. all the geo information
    # name, family, parent, branch, iso3, area, timespan, coords,

    for lang in tqdm(inter_langs):

        geo_dict_node = geo_graph.nodes[lang]
        # add colex number for the language.
        g.add_node(lang, colex_nr=colex_nr_dict[lang])
        # add geo information for the node.
        for k, v in geo_dict_node.items():
            g.nodes[lang][k] = v

    for langp, phon_pmi in phon_dict.items():
        l1, l2 = langp
        if l1 in inter_langs and l2 in inter_langs:
            if (l1,l2) in colex_dict:
                weight, pmi = colex_dict[(l1, l2)]  # already sorted.
                # if l1 in inter_langs and l2 in inter_langs:
                g.add_edge(l1, l2, phon_pmi=phon_pmi, colex_pmi=pmi, weight=weight)

                geo_dict_edge = geo_graph.edges[l1, l2]
                for k, v in geo_dict_edge.items():
                    g.edges[l1, l2][k] = v

    outputfile = f"{stage2}/graphs/phon_colex_geo/colex_{ds}_{wordlist}_phon_geo_graph.pickle"
    print(f"written to{outputfile}")
    with open(outputfile, "wb") as f:
        pickle.dump(g, f)


if __name__ == '__main__':
    # if build phon geo graph
    build_phon_geo_graph()

    # if build colex geo graph
    for ds in ["clics3", "wn", "colexnet", "colex_all_dedup"]:
        for wordlist in ["nuclear", "peripheral", "emotion_semantics"]:
            build_colex_geo_graph(ds, wordlist)
            build_phon_colex_geo_graph(ds, wordlist)
