import pandas as pd


def load_wordlist(name):
    """
    Load a wordlist to be found in the colexification graphs.
    :param name: emotion_semantics, nuclear, peripheral
    :return: the list of the words in the regarding category.
    """
    with open(f"data/wordlists/{name}.txt") as f:
        wordlist = [x.split()[0].lower() for x in f.readlines()]
    return wordlist


def preprocessing_dataset(wordlist, outputfolder="data/stage1", inputfile="data/colexifications/colex_all.csv",
                          threshold=3,
                          lang_field="Glottocode", concept_field="SYN"):
    """
    Get colexification graphs for each dataset including the re. wordlist.
    :param wordlist: the chosen wordlist
    :param outputfolder: folder for output
    :param inputfile:  file for input
    :param threshold: threshold of the language occurrences for the regarding colexifcations.
    :param lang_field: Glottocode, iso3.
    :param concept_field: SYN, SYNSET
    :return: None
    """
    print(outputfolder, wordlist)
    vocab = load_wordlist(wordlist)

    df = pd.read_csv(inputfile)

    synsets2filter = ["'s", "--"]
    df = df[~df[f"{concept_field}1"].isin(synsets2filter)]
    df = df[~df[f"{concept_field}2"].isin(synsets2filter)]


    for ds in ["wn", "clics3", "colexnet"]:
        df_ds = df[df["ds"] == ds]

        print(f"{ds}, len {len(df_ds)}")

        df_ds = df_ds[df_ds[f"{concept_field}1"].isin(vocab) | df_ds[f"{concept_field}2"].isin(vocab)]
        if len(df_ds) > 0:
            print(f"len {len(df_ds)}")
            df_ds = df_ds.drop_duplicates(subset=[lang_field, "COLEX"])

            langs = []
            for lang, group in df_ds.groupby(lang_field):
                syns = set(group[f"{concept_field}1"].tolist() + group[f"{concept_field}2"].tolist())
                if len(syns) > threshold:
                    langs.append(lang)

            df_ds = df_ds[df_ds[lang_field].isin(langs)]
            print(f"len {len(df_ds)} langs {len(langs)}")
            df_ds.to_csv(f"{outputfolder}/{ds}_{wordlist}.csv", index=False)
        else:
            print(f"no concept in the data available")


def preprocessing_all(wordlist, outputfolder="data/stage1", inputfile="data/colexifications/colex_all_dedup.csv",
                      threshold=3,
                      lang_field="Glottocode", concept_field="SYN"):
    """
    Get all the data for the full colex.
    :param wordlist:
    :param outputfolder:
    :param inputfile:
    :param threshold:
    :param lang_field:
    :param concept_field:
    :return:
    """
    print(outputfolder, wordlist)
    vocab = load_wordlist(wordlist)

    df = pd.read_csv(inputfile)

    # filter out the synsets
    synsets2filter = ["'s", "--"]
    df = df[~df[f"{concept_field}1"].isin(synsets2filter)]
    df = df[~df[f"{concept_field}2"].isin(synsets2filter)]

    print(f" len {len(df)}")

    df_ds = df[df[f"{concept_field}1"].isin(vocab) | df[f"{concept_field}2"].isin(vocab)]
    if len(df_ds) > 0:
        print(f"len {len(df_ds)}")
        df_ds = df_ds.drop_duplicates(subset=[lang_field, "COLEX"])

        langs = []
        for lang, group in df_ds.groupby(lang_field):
            syns = set(group[f"{concept_field}1"].tolist() + group[f"{concept_field}2"].tolist())
            if len(syns) > threshold:  # filter out synsets appear in less than 3 languages.
                langs.append(lang)

        df_ds = df_ds[df_ds[lang_field].isin(langs)]
        print(f"len {len(df_ds)} langs {len(langs)}")
        df_ds.to_csv(f"{outputfolder}/colex_all_dedup_{wordlist}.csv", index=False)
    else:
        print(f"no concept in the data available")


if __name__ == '__main__':
    import plac

    plac.call(preprocessing_dataset)
    # plac.call(preprocessing_all)
