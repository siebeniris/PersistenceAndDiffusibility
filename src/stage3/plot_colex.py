import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

sns.set_style("darkgrid")
palettes=["black","#194569", "#5F84A2", "#91AEC4","#008ECC", "#B7D0E1", "cadetblue"]
stage3 = "data/stage3/plots"

def plot_control_phylo(group, df, ylim=(-0.1, 0.2), figsize=(8, 6)):
    df = df[df["group"] == group]
    df = df[df["control"] == "genetic"]

    plt.figure(figsize=figsize)
    ax = sns.pointplot(x='predictor', y='Beta', hue='Response', palette=palettes,
                       linestyles='', dodge=.6, data=df)

    for (x0, y0), (x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5), (x6, y6) in zip(
            ax.collections[0].get_offsets(), ax.collections[1].get_offsets(), ax.collections[2].get_offsets(),
            ax.collections[3].get_offsets(), ax.collections[4].get_offsets(), ax.collections[5].get_offsets(),
            ax.collections[6].get_offsets()):
        ax.plot([x0, x1], [y0, y1], color='grey', ls=':', zorder=0)
        ax.plot([x1, x2], [y1, y2], color='grey', ls=':', zorder=0)
        ax.plot([x0, x2], [y0, y2], color='grey', ls=':', zorder=0)
        ax.plot([x4, x5], [y4, y5], color='grey', ls=':', zorder=0)


    ax.set_xlabel('ylabel', fontsize='medium')  # relative to plt.rcParams['font.size']
    ax.set_xlabel('Operationalizations of Contact Intensity')

    ax.set_ylim(ylim[0], ylim[1])
    plt.title("(COLEX/PHON~CONTACT)|GENETIC", loc="left")

    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    plt.savefig(f"{stage3}/colex/control_phylo_{group}.png", bbox_inches='tight')


def plot_control_geo(group, df, ylim=(-0.1, 0.2), figsize=(8, 6)):
    df = df[df["group"] == group]
    df = df[df["predictor"] == "genetic"]

    plt.figure(figsize=figsize)

    ax = sns.pointplot(x='control', y='Beta', hue='Response', palette=palettes,
                       linestyles='', dodge=.6, data=df)

    for (x0, y0), (x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5), (x6, y6) in zip(
            ax.collections[0].get_offsets(), ax.collections[1].get_offsets(), ax.collections[2].get_offsets(),
            ax.collections[3].get_offsets(), ax.collections[4].get_offsets(), ax.collections[5].get_offsets(),
            ax.collections[6].get_offsets()):
        ax.plot([x0, x1], [y0, y1], color='grey', ls=':', zorder=0)
        ax.plot([x1, x2], [y1, y2], color='grey', ls=':', zorder=0)
        ax.plot([x0, x2], [y0, y2], color='grey', ls=':', zorder=0)
        ax.plot([x4, x5], [y4, y5], color='grey', ls=':', zorder=0)

    ax.set_ylim(ylim[0], ylim[1])
    ax.set_xlabel('Operationalizations of Contact Intensity')
    plt.title("(COLEX/PHON~PHYLO)|CONTACT", loc="left")

    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    plt.savefig(f"{stage3}/colex/control_geo_{group}.png", bbox_inches='tight')

    # close.
    plt.close()
    plt.clf()


def main():
    inputfile = "data/stage3/results/colexnet_mixed_effects.csv"
    df = pd.read_csv(inputfile)
    values = {"geodist_norm": "GEO.Dist", "contact_norm": "Lang.Contact", "neighbour": "Neighbour"}
    # responses = {"nuclear": "colex", ""}
    columns = {"beta": "Beta", "response": "Response"}
    df.rename(columns=columns, inplace=True)
    df["predictor"].replace(values, inplace=True)
    df["control"].replace(values, inplace=True)
    # df["Response"].replace(responses, inplace=True)
    groups = list(set(df["group"].tolist()))
    for group in groups:
        print(f"{group} plots....")
        plot_control_geo(group, df)
        plot_control_phylo(group, df)


if __name__ == '__main__':
    main()




