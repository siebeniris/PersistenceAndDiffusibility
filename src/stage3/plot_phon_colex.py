import os

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

sns.set_style("darkgrid")

stage3 = "data/stage3/plots"


# color palettes: https://matplotlib.org/stable/gallery/color/named_colors.html

def plot_control_phylo(group, df, outputdir, ylim=(-0.1, 0.35), figsize=(5, 6)):
    df = df[df["group"] == group]
    df = df[df["control"] == "genetic"]

    plt.figure(figsize=figsize)
    palettes = ["royalblue", "goldenrod", "tomato"]
    ax = sns.pointplot(x='predictor', y='Beta', hue='Response', palette=palettes,
                       linestyles='', dodge=.3, data=df)
    for (x0, y0), (x1, y1), (x2, y2) in zip(ax.collections[0].get_offsets(), ax.collections[1].get_offsets(),
                                            ax.collections[2].get_offsets()):
        ax.plot([x0, x1], [y0, y1], color='grey', ls=':', zorder=0)
        ax.plot([x1, x2], [y1, y2], color='grey', ls=':', zorder=0)
        ax.plot([x0, x2], [y0, y2], color='grey', ls=':', zorder=0)

    ax.set_ylim(ylim[0], ylim[1])
    ax.set_xlabel('Operationalizations of Contact Intensity')
    ax.axhline(0, color='black', ls='--')

    plt.title("(COLEX/PHON~CONTACT)|PHYLO", loc="left")
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))

    plt.savefig(os.path.join(outputdir, f"control_phylo_{group}.png"), bbox_inches='tight')

    # close.
    plt.close()
    plt.clf()


def plot_control_geo(group, df, outputdir, ylim=(-0.1, 0.35), figsize=(5, 6)):
    df = df[df["group"] == group]
    df = df[df["predictor"] == "genetic"]
    print(df.head())

    plt.figure(figsize=figsize)

    palettes = ["royalblue", "goldenrod", "tomato"]
    ax = sns.pointplot(x='control', y='Beta', hue='Response', palette=palettes,
                       linestyles='', dodge=.3, data=df)
    for (x0, y0), (x1, y1), (x2, y2) in zip(ax.collections[0].get_offsets(), ax.collections[1].get_offsets(),
                                            ax.collections[2].get_offsets()):
        ax.plot([x0, x1], [y0, y1], color='grey', ls=':', zorder=0)
        ax.plot([x1, x2], [y1, y2], color='grey', ls=':', zorder=0)
        ax.plot([x0, x2], [y0, y2], color='grey', ls=':', zorder=0)

    ax.set_ylim(ylim[0], ylim[1])
    ax.set_xlabel('Operationalizations of Contact Intensity')
    ax.axhline(0, color='black', ls='--')

    plt.title("(COLEX/PHON~PHYLO)|CONTACT", loc="left")

    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    # plt.savefig(f"{stage3}/colex_phon/control_geo_{group}.png", bbox_inches='tight')
    plt.savefig(os.path.join(outputdir, f"control_geo_{group}.png"), bbox_inches='tight')

    # close.
    plt.close()
    plt.clf()


def main(inputfile):
    folder_name = os.path.dirname(inputfile).replace("data/stage3/results/", "")
    basename = os.path.basename(inputfile).replace(".csv", "")
    outputdir = os.path.join("data/stage3/plots", f"{folder_name}_{basename}", "colex_phon")
    print(outputdir)
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    df = pd.read_csv(inputfile)
    values = {"geodist_norm": "GEO.Dist", "contact_norm": "Contact.Dist", "neighbour": "Neighbour"}

    responses = {"nuclear": "colex"}
    columns = {"beta": "Beta", "response": "Response"}
    df.rename(columns=columns, inplace=True)
    df["predictor"].replace(values, inplace=True)
    df["control"].replace(values, inplace=True)
    df["Response"].replace(responses, inplace=True)

    groups = list(set(df["group"].tolist()))
    for group in groups:
        print(f"{group} plots....")
        plot_control_geo(group, df, outputdir)
        plot_control_phylo(group, df, outputdir)


if __name__ == '__main__':
    import plac
    plac.call(main)
