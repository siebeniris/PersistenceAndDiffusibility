import os.path

import pandas as pd

from sklearn.metrics.pairwise import cosine_distances


def computing_matrix2cosine(wordlist: str,
                            outputfolder="data/stage2/colex2cosine/cosine_distances",
                            inputfolder="data/stage2/colex2cosine/matrices"):
    print(f"Loading the matrix {wordlist}")
    df = pd.read_csv(f"{inputfolder}/{wordlist}.csv", index_col=0, low_memory=False)
    print(df.head(2))
    langs = df.index.tolist()
    print(f"converting to a numpy array")
    X = df.to_numpy()
    # calculating cosine distances.
    vectors = cosine_distances(X)

    df_vectors = pd.DataFrame(vectors)
    df_vectors.index = langs
    df_vectors.columns = langs

    print(df_vectors.shape)
    print("Saving...")
    df_vectors.to_csv(os.path.join(outputfolder, f"{wordlist}.csv"))


if __name__ == '__main__':
    import plac

    plac.call(computing_matrix2cosine)
