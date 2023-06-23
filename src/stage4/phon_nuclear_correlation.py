import pandas as pd
from pandarallel import pandarallel

pandarallel.initialize(progress_bar=True)
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

### Pearson correlation between PHON. & Nuclear.


df = pd.read_csv("data/stage3/colexnet_phon_geo_graph_edges.csv")
df = df.dropna(subset=["phon", "nuclear"])


def get_coefficients(field, df):
    if field == "relate_level":
        df = df[df[field] != -1]
        values = {0: "Unrelated", 1: "Lower-level related", 2: "Mid-level Related", 3: "Higher-level Related"}
        df["relate_level"].replace(values, inplace=True)
    else:
        df = df[df[field] != "-1"]
    print("language pairs:", len(df))
    print("languages", len(set(df["source"].tolist() + df["target"].tolist())))
    areas = list(set(df[field].tolist()))
    print(f"there are {len(areas)} {field}-s")

    area_dict = {x: (x if x != "0" else f"Cross {field.capitalize()}s") for x in areas}

    areas_l = []
    pvalues = []
    rs = []
    intervals = []
    samples = []
    ses = []
    for area in areas:
        df_ = df[df[field] == area]
        LEN = len(df_)
        if LEN > 2:
            areas_l.append(area_dict[area])
            samples.append(LEN)
            # result of pearson correlation
            res = pearsonr(df_.phon.to_numpy(), df_.nuclear.to_numpy())
            # coefficients
            r = res.statistic
            p = res.pvalue
            confin = res.confidence_interval()
            rs.append(r)
            pvalues.append(p)
            low_conf, high_conf = confin.low, confin.high
            se = (high_conf - low_conf) / 3.92
            intervals.append((confin.low, confin.high))
            ses.append(se)
    df_pearsonr = pd.DataFrame.from_dict({
        field: areas_l,
        "sample": samples,
        "pearsonr": rs,
        "pvalue": pvalues,
        "conf_int": intervals,
        "standard_error": ses

    })
    df_pearsonr["corrected_p"] = df_pearsonr["pvalue"] / df_pearsonr["sample"]
    return df_pearsonr


def plot_pearsonr(df, field, figsize, width=0.5):
    df_pearsonr = get_coefficients(field, df)
    df_pearsonr["Significant"] = df_pearsonr["corrected_p"] < 0.001
    significances = df_pearsonr["Significant"].tolist()
    significance = ["(*)" if x == True else " " for x in significances]

    plt.figure(figsize=figsize)
    ax = sns.barplot(data=df_pearsonr, x="pearsonr", y=field, width=width)
    ax.errorbar(data=df_pearsonr, x="pearsonr", y=field, xerr="standard_error", ls="", lw=1, color="black")
    rects = ax.patches
    ses = df_pearsonr["standard_error"].tolist()
    samples = df_pearsonr["sample"].tolist()
    plt.ylabel(f"{field.capitalize()}", fontsize=16)
    plt.xlabel("Pearson correlation with 95% CI", fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlim(0, 0.225)
    # For each bar: Place a label
    for idx, rect in enumerate(rects):
        # Get X and Y placement of label from rect.
        x_value = rect.get_width()
        y_value = rect.get_y() + rect.get_height() / 2

        # Number of points between bar and label. Change to your liking.
        space = 5
        # Vertical alignment for positive values
        ha = 'left'

        # If value of bar is negative: Place label left of bar
        if x_value < 0:
            # Invert space to place label to the left
            space *= -1
            # Horizontally align label at right
            ha = 'right'

        # Use X value as label and format number with one decimal place
        label = f"{samples[idx]} {significance[idx]}"

        # Create annotation
        plt.annotate(
            label,  # Use `label` as label
            (x_value + ses[idx] if x_value > 0 else x_value - ses[idx], y_value),  # Place label at end of the bar
            xytext=(space, 0),  # Horizontally shift label by `space`
            textcoords="offset points",  # Interpret `xytext` as offset in points
            va='center',
            ha=ha, fontsize=10)  # Horizontally align label differently for
        # positive and negative values.
    plt.savefig(f"plots/{field}_pearsonr.png")

    plt.close()
    plt.clf()


def main(field, w=14, h=5, width=0.5):
    df = pd.read_csv("data/stage3/colexnet_phon_geo_graph_edges.csv")
    df = df.dropna(subset=["phon", "nuclear"])
    plot_pearsonr(df, field, figsize=(w, h), width=width)


if __name__ == '__main__':
    import plac

    plac.call(main)
