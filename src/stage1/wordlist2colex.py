import os
import pandas as pd
from tqdm import tqdm


def load_wordlist(name):
    """
    Load a wordlist to be found in the colexification graphs.
    :param name: emotion_semantics, nuclear, peripheral
    :return: the list of the words in the regarding category.
    """
    with open(f"data/wordlists/{name}.txt") as f:
        wordlist = [x.split()[0].lower() for x in f.readlines()]
    return wordlist

# iterate through all the files
def load_lang_colex(inputfolder, lang):
    df = pd.read_csv(os.path.join(inputfolder, f"{lang}.csv"))
    df[["syn1", "syn2"]] = df.colex.str.split("~", expand=True)
    return df



def preprocessing_dataset(wordlist, ratings=False, outputfolder="data/stage1/word2colex",
                          inputfolder="data/colex_freq_processed",
                          threshold=3):
    """
    Get colexification graphs for each dataset including the re. wordlist.
    :param wordlist: the chosen wordlist
    :param outputfolder: folder for output
    :param inputfolder:  folder for input
    :param threshold: threshold of the language occurrences for the regarding colexifcations
    :return: None
    """
    print(outputfolder, wordlist)
    vocab = load_wordlist(wordlist)
    # output to each sub-directory
    outputdir = os.path.join(outputfolder, wordlist)
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    for language_file in tqdm(os.listdir(inputfolder)):
        if language_file.endswith(".csv"):
            try:
                language = language_file.replace(".csv", "")
                df_lang = load_lang_colex(inputfolder, language)

                # filter out the symbols as synset.
                synsets2filter = ["'s", "--"]
                df_lang = df_lang[~df_lang["syn1"].isin(synsets2filter)]
                df_lang = df_lang[~df_lang["syn2"].isin(synsets2filter)]


                # affective loaded/ abstract/concrete wordlist: ratings=True
                if ratings:
                    df_ds = df_lang[df_lang["syn1"].isin(vocab) & df_lang["syn2"].isin(vocab)]
                else:
                    df_ds = df_lang[df_lang["syn1"].isin(vocab) | df_lang["syn2"].isin(vocab)]

                df_ds.to_csv(os.path.join(outputdir, f"{language}.csv"), index=False)
            except Exception as msg:
                print(msg)


if __name__ == '__main__':
    import plac

    plac.call(preprocessing_dataset)
    # plac.call(preprocessing_all)
