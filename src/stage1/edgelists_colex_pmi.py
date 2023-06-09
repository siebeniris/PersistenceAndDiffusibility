import pandas as pd
from itertools import combinations
from collections import defaultdict
import os


def co_occurrence_table(df: pd.DataFrame, by_id: str):
    """
    Get co-occurrence table for languages per colexification.
    :param df: file for colexifications
    :param by_id: Glottocode/iso3
    :return: co-occur dictionary, number of colexifications ignoring lexical forms.
    """
    print('len of colexification df:', len(df))
    df = df.drop_duplicates(subset=[by_id, "COLEX"])
    print(f'len of df after droping duplicates for {by_id}:', len(df))
    codf = df[[by_id, "COLEX"]]
    co_dict = defaultdict(int)

    num_of_colexification_ignoring_forms = 0
    for k, group in codf.groupby(["COLEX"]):
        num_of_colexification_ignoring_forms += len(group)
        combs = combinations(group[by_id].tolist(), 2)
        # sort the combins of languages -> no need for undirected flattening.
        for p in combs:
            t1, t2 = p  # LANGUAGES.
            if t1 != t2:
                co_dict[tuple(sorted(p))] += 1

    co_dict_ = {k: v for k, v in co_dict.items() if v > 0}

    return co_dict_, num_of_colexification_ignoring_forms


def get_codict(df: pd.DataFrame, by_id: str, outputfolder: str, filename: str) -> None:
    """
    Get co dict.
    :param df:
    :param by_id:
    :param outputfolder:
    :param filename:
    :return:
    """
    # by_id: column name, iso3code.

    print("len: ", len(df))
    df = df.dropna(subset=[by_id])
    co_dict, num_of_colexification_ignoring_forms = co_occurrence_table(df=df, by_id=by_id)

    print(f"output codict size: {len(co_dict)}")
    print("num_of_colexification_ignoring_forms:", num_of_colexification_ignoring_forms)

    print("generating edgelist...")
    lt1, lt2, lv = [], [], []
    for p, v in co_dict.items():
        lt1.append(p[0])
        lt2.append(p[1])
        lv.append(v)

    edge_df = pd.DataFrame(data={"source": lt1, "target": lt2, "weight": lv})

    # normalize the weight
    df_iso_colex = df.groupby([by_id])["COLEX"].count()
    d = df_iso_colex.to_dict()

    edge_df["source_num_colex"] = edge_df["source"].apply(lambda x: d[x])
    edge_df["target_num_colex"] = edge_df["target"].apply(lambda x: d[x])
    edge_df["normalized_weight"] = edge_df["weight"] / (
            edge_df["source_num_colex"] + edge_df["target_num_colex"])

    edge_df.to_csv(os.path.join(outputfolder, f"{filename}"), index=False)


def main(inputfolder, outputfolder):
    for file in os.listdir(inputfolder):
        filepath = os.path.join(inputfolder, file)
        print(file)
        df = pd.read_csv(filepath)
        get_codict(df, "Glottocode", outputfolder, file)


if __name__ == '__main__':
    import plac

    plac.call(main)
