import os
import random

import pandas as pd
import numpy as np


def get_colex_sample_nr(filename):
    if filename in ["nuclear", "non-nuclear", "random", "emotion_semantics"]:
        sample_colexes = 5000
        return sample_colexes
    elif filename in ["concrete_words", "abstract_words"]:
        sample_colexes = 10000
        return sample_colexes
    elif filename in ["aff_concrete_words", "aff_abstract_words"]:
        sample_colexes = 68
        return sample_colexes
    else:
        print("not correct filename")
        return None


def sampling_matrices(matrices_dir="data/stage2/colex2cosine/matrices",
                      output_dir="data/stage2/controlled_colex2cosine"):
    random.seed(42)

    # randomly sample the colexifications for testing hypotheses.
    outputfolder = os.path.join(output_dir, "matrices")
    if not os.path.exists(outputfolder):
        os.makedirs(outputfolder)

    for file in os.listdir(matrices_dir):
        filepath = os.path.join(matrices_dir, file)
        filename = file.replace(".csv", "")

        df = pd.read_csv(filepath, index_col=0, low_memory=False)
        cols = df.columns.tolist()
        print(filename, f"len {len(df)} colex. {len(cols)}")
        samples_nr = get_colex_sample_nr(filename)
        if samples_nr is not None:
            if len(cols) > samples_nr:
                sampled_cols = random.sample(cols, k=samples_nr)
                df_sampled = df[sampled_cols].replace(0, np.nan).dropna(how="all", axis=0).replace(np.nan, 0)
                print(f"lang {len(df_sampled)}, {len(df_sampled.columns)}")
                df_sampled.to_csv(os.path.join(outputfolder, file))
            else:
                df.to_csv(os.path.join(outputfolder, file))


if __name__ == '__main__':
    sampling_matrices()
