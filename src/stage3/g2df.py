import os.path

import numpy as np
import networkx as nx

from pandarallel import pandarallel

pandarallel.initialize(progress_bar=True)


def load_graph(filepath):
    """
    Load a graph.
    :param filepath:
    :return:
    """

    return nx.read_edgelist(filepath)


def l2c(field, df):
    """
    Convert certain categories into numerals.
    :param field: genus/ branch/ family/ area/ macroarea
    :param df:
    :return:
    """
    l = df[field].tolist()
    ls = list(set(l))
    l2c = dict()
    for idx, i in enumerate(ls):
        if i in [-1, 0]:
            l2c[i] = i
        else:
            l2c[i] = idx + 2
    df[f"{field}_id"] = df[field].replace(l2c)
    return df


def normalizer(L):
    """
    Normalizing a list to [0,1].
    :param L: List
    :return: Normalized list.
    """
    L = (L - np.min(L)) / (np.max(L) - np.min(L))
    return L


def g2df(g):
    """
    Graph to dataframe.
    :param g: Graph
    :return: dataframe
    """
    df = nx.to_pandas_edgelist(g)
    # convert categories to numerals
    df = l2c("family", df)
    df = l2c("branch", df)
    df = l2c("area", df)
    df = l2c("macroarea", df)
    df = l2c("genus", df)

    contact = df["contact"].to_numpy().reshape(-1, 1)
    contact = normalizer(contact)
    df["contact_norm"] = contact

    geodist = df["geodist"].to_numpy().reshape(-1, 1)
    df["geodist_norm"] = normalizer(geodist)
    return df


def get_related_level(fam, genus, branch):
    # higher level related - fam the same,3
    # mid level related - genus the same, 2
    # low level related - branch the same,1
    # -1: unknown
    # 0: unrelated
    # related=[-1, 0,1,2,3]
    if branch not in [0, -1]:
        r = 1
    else:
        # move up
        if genus not in [0, -1]:
            r = 2
        else:
            # move up
            if fam not in [0, -1]:
                r = 3
            elif fam == 0:
                r = 0
            else:
                r = -1

    return r


def main(graph_filepath, outputfolder="data/stage3"):
    """
    Graph to dataframe.

    :param graph_filepath:
    :param outputfolder:
    :return:
    """
    filename = os.path.basename(graph_filepath)
    folder_name = os.path.dirname(graph_filepath).replace("data/stage2/graphs/", "")
    sub_dir = os.path.join(outputfolder, folder_name)
    if not os.path.exists(sub_dir):
        os.makedirs(sub_dir)


    print(f"loading the graph {graph_filepath}")
    g = load_graph(graph_filepath)
    print(f"processing and extract dataframe...")
    df = g2df(g)
    df["relate_level"] = df.parallel_apply(lambda x: get_related_level(x.family_id, x.genus_id, x.branch_id), axis=1)

    edge_file = os.path.join(sub_dir, filename).replace(".txt", ".csv")
    print(f"dataframe saved to {edge_file}")
    df.to_csv(edge_file, index=False)


if __name__ == '__main__':
    import plac

    plac.call(main)
