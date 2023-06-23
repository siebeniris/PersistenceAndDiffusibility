import os.path
import json
from collections import defaultdict

import pandas as pd
from tqdm import tqdm
from joblib import Parallel, delayed


def get_language_distance(inputfile="data/languages/languages_colexnet.csv",
                          outputfolder="data/stage1/language_contact_colexnet"):
    df_geodesic = pd.read_csv("data/stage1/lang2lang_geodesic.csv")
    print(len(df_geodesic))
    df_geodesic.dropna(subset=["ISO1", "ISO2"], inplace=True)
    print(len(df_geodesic))
    lang2lang_dict_ = dict(zip(zip(df_geodesic["ISO1"], df_geodesic["ISO2"]), df_geodesic["GeodesicDist"]))
    lang2lang_dict_sorted = {tuple(sorted(x)): y for x, y in lang2lang_dict_.items()}
    langs_all = set(df_geodesic["ISO1"].tolist() + df_geodesic["ISO2"].tolist())

    df_input = pd.read_csv(inputfile)
    if not os.path.exists(outputfolder):
        os.makedirs(outputfolder)

    interlangs = set(df_input["iso639_3"].tolist()).intersection(langs_all)

    def get_lang2lang_contacts(tgt_lang, worklangs=interlangs, lang2lang_dict=lang2lang_dict_sorted,
                               outputfolder=outputfolder):
        outputfile = f"{outputfolder}/{tgt_lang}.json"
        if not os.path.exists(outputfile):
            in_dryer2018 = defaultdict(dict)
            in_dryer2018[tgt_lang] = dict()
            possible_langs = [x for x in worklangs if x != tgt_lang]
            for z in possible_langs:
                between_count = 0
                y = tgt_lang
                for x in worklangs:
                    try:
                        x_y = tuple(sorted([x, y]))
                        x_z = tuple(sorted([x, z]))
                        y_z = tuple(sorted([y, z]))
                        dist_x_y = lang2lang_dict[x_y]
                        dist_x_z = lang2lang_dict[x_z]
                        dist_y_z = lang2lang_dict[y_z]

                        if dist_x_y < dist_y_z and dist_x_z < dist_y_z:
                            between_count += 1
                    except Exception:
                        print(x, y, z)
                        continue
                in_dryer2018[tgt_lang][z] = between_count
            with open(outputfile, "w+") as f:
                json.dump(in_dryer2018, f)

    Parallel(n_jobs=-1)(delayed(get_lang2lang_contacts)(i) for i in tqdm(interlangs))


if __name__ == '__main__':
    import plac

    plac.call(get_language_distance)
