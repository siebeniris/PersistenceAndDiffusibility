import pandas as pd
import numpy as np

matrices_dir = "data/stage2/colex2cosine/matrices"


# generate abstract/concrete affective matrices.


def intersecting_matrices(wordlist):
    m1 = pd.read_csv(f"{matrices_dir}/affective_loaded.csv", index_col=0)
    m2 = pd.read_csv(f"{matrices_dir}/{wordlist}.csv", index_col=0, low_memory=False)

    m1_cols = m1.columns.tolist()
    m2_cols = m2.columns.tolist()

    overlap = list(set(m1_cols).intersection(set(m2_cols)))

    print(f"affective {len(m1_cols)}, {wordlist} {len(m2_cols)}, overlap {len(overlap)}")
    df = m1[overlap].replace(0, np.nan).dropna(how="all", axis=0).replace(np.nan, 0)

    print(f"langs: {len(df)}")
    print("saving...")
    df.to_csv(f"{matrices_dir}/aff_{wordlist}.csv")


if __name__ == '__main__':
    import plac

    plac.call(intersecting_matrices)
