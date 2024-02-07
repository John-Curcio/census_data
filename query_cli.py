"""
CLI interface for querying the efficient frontier.
User can pass positive metrics to maximize and negative metrics to minimize.
Flag to plot points.
Optional query string passed directly to pandas query method.
Optional sort_by metric to sort the results by.
--help should suggest some example queries in addition to CLI arg explanations
--print_cols should list all args in final_metric_stats.csv
"""

import click
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
from scipy.spatial import ConvexHull, convex_hull_plot_2d

def _plot_points(hull):
    points = hull.points
    plt.plot(points[:,0], points[:,1], 'o')
    for simplex in hull.simplices:
        plt.plot(points[simplex, 0], points[simplex, 1], 'k-')

class EfficientFrontierInterface:

    df = pd.read_csv("final_metric_stats.csv")

    def get_trimmed_df(self, df, query_str=None):
        if query_str:
            df = df.query(query_str)
        return df

    def get_efficient_cities(self, df, metric_dict, plot_points=False):
        metric_cols, metric_signs = list(zip(*metric_dict.items()))
        metric_cols = np.array(metric_cols)
        metric_signs = np.array(metric_signs, dtype=int)
        assert len(metric_cols) == len(metric_signs)
        efficient_inds = []
        
        hull = ConvexHull(df[metric_cols].dropna())
        hull_inds = hull.vertices
        hull_df = df[["area_name", *metric_cols]].dropna().iloc[hull_inds]
        
        for i, rowi in tqdm(hull_df.iterrows()):
            if not rowi[metric_cols].isnull().any():
                # find Y that is at least as good on all metrics
                metric_diffs = (hull_df[metric_cols] - rowi[metric_cols]) * metric_signs
                y_not_worse = (metric_diffs >= 0).all(axis=1)
                if y_not_worse.sum() == 1: # will always match w itself
                    efficient_inds.append(i)
        if plot_points:
            fig, ax = plt.subplots()
            _plot_points(hull)
            for ind in efficient_inds:
                print(hull_df["area_name"].loc[ind])
                ax.annotate(hull_df["area_name"].loc[ind], (hull_df.loc[ind][1:3]))
            plt.xlabel(metric_cols[0])
            plt.ylabel(metric_cols[1])
            
        return df.loc[hull_df.loc[efficient_inds].index]
    
@click.command()
@click.option("--maximize", "-max", multiple=True, help="Metrics to maximize")
@click.option("--minimize", "-min", multiple=True, default=None, help="Metrics to minimize")
@click.option("--plot", "-p", is_flag=True, help="Plot the efficient cities by first two metrics (shitty)")
@click.option("--query", "-q", default=None, help="Query string to pass to pandas .query() method, verbatim. " +
              "Example: (n_people > 150000) & (p_black_given_unmarried <= 0.3)")
@click.option("--sort_by", "-s", default=None, help="Metric to sort by")
@click.option("--print_cols", is_flag=True, help="Print to stdout the full list of columns and break")
@click.help_option("--help", help="""Show this method and exit.

Here's a query you could try (remove indents):

python query_cli.py -max=p_unmarried_20_24_female -max=p_white -min=median_rent_1_bed --query="n_people>=150000" -p
""")
def main(maximize, minimize, plot, query, sort_by, print_cols):
    efi = EfficientFrontierInterface()
    if print_cols:
        for col in efi.df.columns:
            print(col)
        exit()
    metric_dict = {**{m: 1 for m in maximize}, **{m: -1 for m in minimize}}
    df = efi.get_trimmed_df(efi.df, query)
    df = efi.get_efficient_cities(df, metric_dict, plot)
    if sort_by:
        df = df.sort_values(sort_by, ascending=False)
    print(df[["area_name", *maximize, *minimize]])
    # hang around for the plot
    if plot:
        plt.show()

if __name__ == "__main__":
    main()