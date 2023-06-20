import pandas as pd
import warnings
import statsmodels.formula.api as smf
from statsmodels.tools.sm_exceptions import ConvergenceWarning

warnings.simplefilter('ignore', ConvergenceWarning)


def analysis_mixed_effects_per_group(response, predictor, control, group, df):
    # response -> COLEX(nuclear/peripheral/emotion/abstract/concrete/affective), PHON
    # group -> area, macroarea, genus, branch, family, relate_level
    # predictor (contact) -> neighbour, contact, geodist
    # predictor (PHYLO) -> genetic

    df = df.dropna(subset=[response, predictor, control, group])
    df = df[df[group] != -1]  # unknown
    languages = set(df["source"].tolist() + df["target"].tolist())
    print(f"language pairs {len(df)}, languages {len(languages)} ")
    print(f"({response} ~ {predictor})|{control} <-> {group}")
    model = smf.mixedlm(f"{response} ~ {predictor}  ", df, groups=df[group], re_formula=f"~{control}")
    mdf = model.fit()
    beta = mdf.params.loc[predictor]
    pvalue = mdf.pvalues.loc[predictor]
    conf_interval = tuple(mdf.conf_int(alpha=0.5).loc[predictor].tolist())
    print(beta, pvalue, conf_interval)
    print('*' * 40)
    return beta, pvalue, conf_interval[0], conf_interval[1]


def main(inputfile, ds="colexnet"):
    df = pd.read_csv(inputfile)

    # df = df[df["relate_level"] != -1] # doesn't make a difference.

    phylo = ["genetic"]
    # contact = ["geodist_norm", "contact_norm"]
    contact = ["geodist_norm", "contact_norm", "neighbour"]
    groups = ["area_id", "macroarea_id", "relate_level", "family_id", "genus_id", "branch_id"]
    reporter = open(f"data/stage3/results/all/{ds}_reports_mixed_effects2.csv", "a+")
    reporter.write(f"response,predictor,control,group,beta,pvalue,conf_int1,conf_int2\n")

    if ds == "phon":
        for response in ["phon", "nuclear", "syntactic"]:
            df = df.dropna(subset=["phon", "nuclear"])
            for v1, v2 in [(x, y) for x in phylo for y in contact]:
                for group in groups:
                    b1, p1, ci11, ci12 = analysis_mixed_effects_per_group(response, v1, v2, group, df)
                    reporter.write(f"{response},{v1},{v2},{group},{b1},{p1},{ci11},{ci12}\n")
                    b2, p2, ci21, ci22 = analysis_mixed_effects_per_group(response, v2, v1, group, df)
                    reporter.write(f"{response},{v2},{v1},{group},{b2},{p2},{ci21},{ci22}\n")

    else:
        for response in ["nuclear", "peripheral", "emotion", "random"]:
            df = df.dropna(subset=["nuclear"])
            for v1, v2 in [(x, y) for x in phylo for y in contact]:
                for group in groups:
                    b1, p1, ci11, ci12 = analysis_mixed_effects_per_group(response, v1, v2, group, df)
                    reporter.write(f"{response},{v1},{v2},{group},{b1},{p1},{ci11},{ci12}\n")
                    b2, p2, ci21, ci22 = analysis_mixed_effects_per_group(response, v2, v1, group, df)
                    reporter.write(f"{response},{v2},{v1},{group},{b2},{p2},{ci21},{ci22}\n")

        for response in ["concrete", "abstract"]:
            df = df.dropna(subset=["concrete", "abstract"])
            for v1, v2 in [(x, y) for x in phylo for y in contact]:
                for group in groups:
                    b1, p1, ci11, ci12 = analysis_mixed_effects_per_group(response, v1, v2, group, df)
                    reporter.write(f"{response},{v1},{v2},{group},{b1},{p1},{ci11},{ci12}\n")
                    b2, p2, ci21, ci22 = analysis_mixed_effects_per_group(response, v2, v1, group, df)
                    reporter.write(f"{response},{v2},{v1},{group},{b2},{p2},{ci21},{ci22}\n")

        for response in ["aff_conc", "aff_abs"]:
            df = df.dropna(subset=["aff_conc", "aff_abs"])
            for v1, v2 in [(x, y) for x in phylo for y in contact]:
                for group in groups:
                    b1, p1, ci11, ci12 = analysis_mixed_effects_per_group(response, v1, v2, group, df)
                    reporter.write(f"{response},{v1},{v2},{group},{b1},{p1},{ci11},{ci12}\n")
                    b2, p2, ci21, ci22 = analysis_mixed_effects_per_group(response, v2, v1, group, df)
                    reporter.write(f"{response},{v2},{v1},{group},{b2},{p2},{ci21},{ci22}\n")

    reporter.close()


if __name__ == '__main__':
    import plac

    plac.call(main)
