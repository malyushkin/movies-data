import pandas as pd
from datetime import datetime

if __name__ == "__main__":

    columns = {
        "imdb": "imdbID",
        "vote": "Rating10",
        "vote_date": "WatchedDate",
    }
    path_file = "../kinopoisk/csv/movies_rating.csv"

    data = pd.read_csv(path_file, parse_dates=["vote_date"])
    data.rename(columns=columns, inplace=True)

    letterboxd_data = data.loc[:, list(columns.values())].dropna()

    letterboxd_data.to_csv(f"{datetime.now().date()}_letterboxd.csv", index=None)
