import os
import warnings

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')


sns.set_style("darkgrid")
palettes = ["goldenrod", "saddlebrown", "indigo", "dimgray"]


def plot_control_phylo(group, df, outputdir, ylim=(-0.1, 0.4), figsize=(8, 6)):
    df = df[df["group"] == group]
    df = df[df["control"] == "genetic"]

    plt.figure(figsize=figsize)
    ax = sns.pointplot(x='predictor', y='Beta', hue='Response', palette=palettes,
                       linestyles='', dodge=.6, data=df)

    for (x0, y0), (x1, y1), (x2, y2) in zip(
            ax.collections[0].get_offsets(), ax.collections[1].get_offsets(), ax.collections[2].get_offsets()):
        ax.plot([x0, x1], [y0, y1], color='grey', ls=':', zorder=0)
        ax.plot([x1, x2], [y1, y2], color='grey', ls=':', zorder=0)
        ax.plot([x0, x2], [y0, y2], color='grey', ls=':', zorder=0)

    ax.set_xlabel('ylabel', fontsize='medium')  # relative to plt.rcParams['font.size']
    ax.set_xlabel('Operationalizations of Contact Intensity')

    ax.set_ylim(ylim[0], ylim[1])
    ax.axhline(0, color='black', ls='--')

    plt.title("(COLEX~CONTACT)|GENETIC", loc="left")

    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    plt.savefig(os.path.join(outputdir, f"control_phylo_{group}_level1.png"), bbox_inches='tight')


def plot_control_geo(group, df, outputdir, ylim=(-0.1, 0.4), figsize=(8, 6)):
    df = df[df["group"] == group]
    df = df[df["predictor"] == "genetic"]

    plt.figure(figsize=figsize)

    ax = sns.pointplot(x='control', y='Beta', hue='Response', palette=palettes,
                       linestyles='', dodge=.6, data=df)

    for (x0, y0), (x1, y1), (x2, y2) in zip(
            ax.collections[0].get_offsets(), ax.collections[1].get_offsets(), ax.collections[2].get_offsets()):
        ax.plot([x0, x1], [y0, y1], color='grey', ls=':', zorder=0)
        ax.plot([x1, x2], [y1, y2], color='grey', ls=':', zorder=0)
        ax.plot([x0, x2], [y0, y2], color='grey', ls=':', zorder=0)

    ax.set_ylim(ylim[0], ylim[1])
    ax.axhline(0, color='black', ls='--')

    ax.set_xlabel('Operationalizations of Contact Intensity')
    plt.title("(COLEX~PHYLO)|CONTACT", loc="left")

    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    # plt.savefig(f"{stage3}/control_geo_{group}_level1.png", bbox_inches='tight')
    plt.savefig(os.path.join(outputdir, f"control_geo_{group}_level1.png"), bbox_inches='tight')


    # close.
    plt.close()
    plt.clf()


def main(inputfile):
    # inputfile = "data/stage3/results/colex_jaeger_inner/controlled_lang_graph_colexnet_reports.csv"
    folder_name = os.path.dirname(inputfile).replace("data/stage3/results/", "")
    basename = os.path.basename(inputfile).replace(".csv", "")
    outputdir = os.path.join("data/stage3/plots", f"{folder_name}_{basename}", "level1")
    print(outputdir)
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    df = pd.read_csv(inputfile)
    df = df[df["response"].isin(["nuclear", "non_nuclear", "emotion", "random"])]

    beta_min, beta_max = df["beta"].min(), df["beta"].max()
    # beta_min_round = round(beta_min, 3) - 0.025
    print(beta_max, beta_min)
    beta_min_round = beta_min - 0.02
    # beta_max_round = round(beta_max, 3) + 0.025
    beta_max_round = beta_max + 0.02
    ylim = (beta_min_round, beta_max_round)

    values = {"geodist_norm": "GEO.Dist", "contact_norm": "Contact.Dist", "neighbour": "Neighbour"}
    responses = {"non_nuclear": "non-nuclear"}
    columns = {"beta": "Beta", "response": "Response"}

    df.rename(columns=columns, inplace=True)
    df["predictor"].replace(values, inplace=True)
    df["control"].replace(values, inplace=True)
    df["Response"].replace(responses, inplace=True)

    groups = list(set(df["group"].tolist()))
    for group in groups:
        print(f"{group} plots....")
        # plot_control_geo(group, df, ylim=ylim)
        # plot_control_phylo(group, df, ylim=ylim)
        plot_control_geo(group, df, outputdir, ylim=ylim)
        plot_control_phylo(group, df, outputdir, ylim=ylim)


if __name__ == '__main__':
    import plac

    plac.call(main)
