import os
import pandas as pd

from tqdm import tqdm
from pandarallel import pandarallel

pandarallel.initialize(progress_bar=True)

stage2 = "data/stage2"
stage1 = "data/stage1"


# get frequencies of colex in each language from bible data
def load_lang_colex2freq(wordlist:str, lang:str):
    filepath = f"data/stage1/word2colex/{wordlist}/{lang}.csv"
    df_lang = pd.read_csv(filepath)
    colex2freq = dict(zip(df_lang["colex"], df_lang["lemma_colex_freq"]))
    return colex2freq


def load_all_colex_patterns(wordlist):
    folder = f"data/stage1/word2colex/{wordlist}"
    colex = set()
    langs = []
    for lang_file in tqdm(os.listdir(folder)):
        filepath = os.path.join(folder, lang_file)
        lang = lang_file.replace(".csv", "")
        df_lang = pd.read_csv(filepath)
        colexes = set(df_lang["colex"].tolist())
        colex = colex.union(colexes)
        langs.append(lang)
    return list(colex), langs



def convert_colex2matrix(wordlist="abstract_words",
                         outputfolder=f"{stage2}/colex2cosine", threshold=3):
    """
    Convert colexification occurrences to cosine similarity between languages...
    :param wordlist:
    :param outputfolder:
    :param threshold: #colex.patterns and #langs should be equal or higher than the threshold.
    :return:
    """
    print(f"Loading all colexification patterns from {wordlist}")
    all_colex_patterns, langs = load_all_colex_patterns(wordlist)
    print(f"there are {len(all_colex_patterns)} colex  {len(langs)} languages.")

    # get an empty dataframe with colexificaiton patterns as columns, languages as rows.
    # lang2colex.at["ngal1298", "so~we"]= ?
    # given a langauge and a colex pattern, show the frequency of it in bible data
    print("Building lang2colex dataframe ...")
    lang2colex = pd.DataFrame(columns=all_colex_patterns, index=langs)

    for lang in tqdm(langs):
        lang_colex2freq = load_lang_colex2freq(wordlist, lang)
        for colex in all_colex_patterns:
            if colex in lang_colex2freq:
                lang2colex.at[lang, colex] = lang_colex2freq[colex]

    # filter the lang2colex dataframe with threshold
    # keep lang/colex with at least \threshold occurrences.
    print(f"Filtering lang2colex with threshold {threshold} ... ")
    colex_counter = {}
    lang_counter = {}
    for colex in all_colex_patterns:
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
    matrix_folder = os.path.join(outputfolder, "matrices")
    if not os.path.exists(matrix_folder):
        os.makedirs(matrix_folder)
    matrix2file = os.path.join(matrix_folder, f"{wordlist}.csv")
    print(f"saving lang2colex matrix to {matrix2file}..")
    lang2colex.to_csv(matrix2file)

    # def colex2sim(l1, l2):
    #     """
    #     Caculate cosine similarity between language l1 and l2
    #     """
    #     vec1 = lang2colex.loc[l1].to_numpy().reshape(1, -1)
    #     vec2 = lang2colex.loc[l2].to_numpy().reshape(1, -1)
    #     cos = pairwise.cosine_similarity(vec1, vec2)[0][0]
    #     return cos
    #
    # langpairs = list(combinations(sorted(langs_remain), 2))
    # print(f"language pairs {len(langpairs)}")
    # print("Building a cosine edgelists ....")
    # lang1s, lang2s = list(zip(*langpairs))
    # df_cos = pd.DataFrame.from_dict({"source": lang1s, "target": lang2s})
    # print(f"Calculating cosine similarity between {len(df_cos)} pair languages ...")
    # df_cos["cosine"] = df_cos.parallel_apply(lambda x: colex2sim(x.source, x.target), axis=1)
    #
    # # saving edgelist
    # edgelist_outputdir = os.path.join(outputfolder, "edgelists")
    # if not os.path.exists(edgelist_outputdir):
    #     os.makedirs(edgelist_outputdir)
    # cos2file = os.path.join(edgelist_outputdir, f"{wordlist}.csv")
    # print(f"saving edgelist file to {cos2file}")
    # df_cos.to_csv(cos2file, index=False)


if __name__ == '__main__':
    import plac

    plac.call(convert_colex2matrix)
