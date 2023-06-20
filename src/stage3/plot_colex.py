import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

sns.set_style("darkgrid")
palettes = ["black", "#194569", "#5F84A2", "#91AEC4", "#008ECC", "#B7D0E1", "cadetblue"]
stage3 = "data/stage3/plots"


def plot_control_phylo(group, df, ylim=(-0.1, 0.4), figsize=(8, 6)):
    df = df[df["group"] == group]
    df = df[df["control"] == "genetic"]

    plt.figure(figsize=figsize)
    ax = sns.pointplot(x='predictor', y='Beta', hue='Response', palette=palettes,
                       linestyles='', dodge=.6, data=df)

    for (x0, y0), (x1, y1), (x2, y2), (x3, y3) in zip(
            ax.collections[0].get_offsets(), ax.collections[1].get_offsets(), ax.collections[2].get_offsets(),
            ax.collections[3].get_offsets()):
        ax.plot([x0, x1], [y0, y1], color='grey', ls=':', zorder=0)
        ax.plot([x1, x2], [y1, y2], color='grey', ls=':', zorder=0)
        ax.plot([x0, x2], [y0, y2], color='grey', ls=':', zorder=0)

    ax.set_xlabel('ylabel', fontsize='medium')  # relative to plt.rcParams['font.size']
    ax.set_xlabel('Operationalizations of Contact Intensity')

    ax.set_ylim(ylim[0], ylim[1])
    ax.axhline(0, color='black', ls='--')

    plt.title("(COLEX~CONTACT)|GENETIC", loc="left")

    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    plt.savefig(f"{stage3}/colex/control_phylo_{group}_level1.png", bbox_inches='tight')


def plot_control_geo(group, df, ylim=(-0.1, 0.4), figsize=(8, 6)):
    df = df[df["group"] == group]
    df = df[df["predictor"] == "genetic"]

    plt.figure(figsize=figsize)

    ax = sns.pointplot(x='control', y='Beta', hue='Response', palette=palettes,
                       linestyles='', dodge=.6, data=df)

    for (x0, y0), (x1, y1), (x2, y2), (x3, y3) in zip(
            ax.collections[0].get_offsets(), ax.collections[1].get_offsets(), ax.collections[2].get_offsets(),
            ax.collections[3].get_offsets()):
        ax.plot([x0, x1], [y0, y1], color='grey', ls=':', zorder=0)
        ax.plot([x1, x2], [y1, y2], color='grey', ls=':', zorder=0)
        ax.plot([x0, x2], [y0, y2], color='grey', ls=':', zorder=0)

    ax.set_ylim(ylim[0], ylim[1])
    ax.axhline(0, color='black', ls='--')

    ax.set_xlabel('Operationalizations of Contact Intensity')
    plt.title("(COLEX~PHYLO)|CONTACT", loc="left")

    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    plt.savefig(f"{stage3}/colex/control_geo_{group}_level1.png", bbox_inches='tight')

    # close.
    plt.close()
    plt.clf()


def main(inputfile):
    # inputfile = "data/stage3/results/colexnet_mixed_effects.csv"
    df = pd.read_csv(inputfile)
    df = df[df["response"].isin(["nuclear", "peripheral", "emotion", "random"])]

    beta_min, beta_max = df["beta"].min(), df["beta"].max()
    beta_min_round = round(beta_min, 3) - 0.025
    beta_max_round = round(beta_max, 3) + 0.025
    ylim = (beta_min_round, beta_max_round)

    values = {"geodist_norm": "GEO.Dist", "contact_norm": "Contact.Dist", "neighbour": "Neighbour"}
    responses = {"peripheral": "non-nuclear"}
    columns = {"beta": "Beta", "response": "Response"}

    df.rename(columns=columns, inplace=True)
    df["predictor"].replace(values, inplace=True)
    df["control"].replace(values, inplace=True)
    df["Response"].replace(responses, inplace=True)

    groups = list(set(df["group"].tolist()))
    for group in groups:
        print(f"{group} plots....")
        plot_control_geo(group, df, ylim=ylim)
        plot_control_phylo(group, df, ylim=ylim)


if __name__ == '__main__':
    import plac

    plac.call(main)