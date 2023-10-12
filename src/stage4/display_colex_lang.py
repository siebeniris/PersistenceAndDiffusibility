import os

import pandas as pd


def load_lang_colex(lang:str):
    freq_dir = "/Users/yiyichen/Documents/experiments/CrossCoLEX/data/colex_freq_processed"
    filepath = os.path.join(freq_dir, f"{lang}.csv")
    df_lang = pd.read_csv(filepath)
    colex2freq = dict(zip(df_lang["colex"], df_lang["lemma_clean"]))
    return colex2freq

def main():
    df_lang = pd.read_csv("data/languages/languages_colexnet.csv")
    iso2name = dict(zip(df_lang["iso639_3"], df_lang["name"]))
    name2iso = dict(zip(df_lang["name"], df_lang["iso639_3"]))
    data_dir = "data/stage2/colex2cosine"
    colex_examples = ["language~tongue", "eye~look", "finger~hand", "tree~wood", "knee~kneel"]
    languages = ["Russian",  "Polish", "Danish", "Rundi", "Igbo", "Yoruba", "Hindi", "Literary Chinese"]

    df_nuclear = pd.read_csv(f"{data_dir}/matrices/nuclear.csv", index_col=0, low_memory=False)
    df_nuclear = df_nuclear.rename(index=iso2name)

    df_nuclear_colex = df_nuclear[colex_examples].sort_values(by=colex_examples, ascending=False)
    print(df_nuclear_colex.loc[languages])

    for language in languages:
        iso3_lang = name2iso[language]
        print(language, iso3_lang)
        lang_colex2freq = load_lang_colex(iso3_lang)
        for colex in colex_examples:
            if colex in lang_colex2freq:
                print(colex)
                print(f"{colex}-> {lang_colex2freq[colex]}")
        print("*"*10)





if __name__ == '__main__':
    main()