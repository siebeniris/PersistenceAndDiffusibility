import json
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics.pairwise import cosine_distances  # distances instead of similarity!!!!!
from seaborn import clustermap
import seaborn as sns



def load_matrix(wordlist, langs):
    # langs are iso3 codes.
    data_dir = "data/stage2/colex2cosine/matrices"
    filepath = os.path.join(data_dir, f"{wordlist}.csv")
    df = pd.read_csv(filepath, index_col=0, low_memory=False)
    df_langs = df.loc[langs]
    df_langs = df_langs.replace(0, np.nan).dropna(how="all", axis=1).replace(np.nan, 0)
    return df_langs


def main(wordlist):
    plt.figure(figsize=(20, 12))

    european_langs = ["Turkish", "Norwegian Bokmål", "Norwegian Nynorsk", "Icelandic", "Belarusian", "Ukranian",
                      "Slovak", "Slovenian",
                      "Croatian Standard", "Kildin Saami", "Skolt Saami", "Inari Saami", "Lule Saami",
                      "South Saami",  "Liv", "Veps", "Karelian", "Basque", "Vlax Romani",
                      "Northern Tosk Albanian",
                      "Russian", "Polish", "Czech", "Bulgarian", "Latvian", "Lithuanian", "Eastern Yiddish",
                      "German", "Dutch",
                      # "English",
                      "Swedish", "Danish", "Breton", "Welsh", "Irish", "Romanian", "Portuguese", "Catalan", "Spanish",
                      "French", "Italian", "Modern Greek", "North Saami",
                      "Hungarian", "Finnish", "Estonian"]

    df_lang = pd.read_csv("data/languages/languages_colexnet.csv")

    df_european = df_lang[df_lang["name"].isin(european_langs)]
    # df_european.to_csv("data/languages/languages_europe.csv", index=False)


    print(f"langs: {len(european_langs)}, overlapping {len(df_european)}")

    iso2name = dict(zip(df_european["iso639_3"], df_european["name"]))

    with open("data/stage4/european_languages.json", "w") as f:
        json.dump(iso2name, f)
    selected_langs = list(iso2name.keys())

    df_selected = load_matrix(wordlist, selected_langs)

    # change iso2code to language names.
    df_selected = df_selected.rename(index=iso2name)

    # change the order of the names to be compared to with the paper
    names = df_selected.index.tolist()
    sort_eu_langs = []
    for lang in european_langs:
        if lang in names:
            sort_eu_langs.append(lang)

    # order are reserved for comparison
    df_selected = df_selected.loc[sort_eu_langs]

    # convert to matrix
    X = df_selected.to_numpy()
    print(f"X -> {X.shape}")

    # compute cosine similarity in X.
    vectors = cosine_distances(X)
    df_vector = pd.DataFrame(vectors)
    df_vector.index = sort_eu_langs
    df_vector.columns = sort_eu_langs
    print(df_vector)


    cluster_map = clustermap(df_selected, method="complete", metric="cosine", z_score=0, cmap="vlag", center=0)
    plt.savefig(f"data/stage4/plots/european_languages_clustermap_{wordlist}.png")
    plt.clf()


    ax = sns.heatmap(df_vector, xticklabels=True, yticklabels=True)
    ax.invert_xaxis()
    plt.tight_layout()
    plt.savefig(f"data/stage4/plots/european_languages_heatmap_{wordlist}.png")
    plt.clf()


if __name__ == '__main__':
    import plac
    plac.call(main)

