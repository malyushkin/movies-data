import json
import requests
import pandas as pd
from datetime import datetime
from os import environ

from data.config import IMDB_API, CONTENT_TYPE_HEADER, USER_AGENT_HEADER

HEADERS = {
    "Content-Type": CONTENT_TYPE_HEADER,
    "User-Agent": USER_AGENT_HEADER,
    "Cookie": environ["IMDB_COOKIE"]
}

PAYLOAD = {
    "query": "mutation UpdateTitleRating($rating: Int!, $titleId: ID!) {\n  rateTitle(input: {rating: $rating, titleId: $titleId}) {\n    rating {\n      value\n      __typename\n    }\n    __typename\n  }\n}",
    "operationName": "UpdateTitleRating",
    "variables": {
        "rating": "",
        "titleId": ""
    }
}


def read_data(file_path: str, columns: list) -> pd.DataFrame:
    """Read CSV data"""

    data = pd.read_csv(file_path, dtype={"year": "Int64"}, parse_dates=["vote_date"]).dropna().reset_index()
    return data.loc[:, columns]


def update_imdb_rating(id: str, rating: str) -> dict:
    """Post movie rating to IMDB"""

    data = PAYLOAD
    data["variables"].update({
        "rating": rating,
        "titleId": id
    })

    update_request = requests.post(IMDB_API, headers=HEADERS, data=json.dumps(data))

    if update_request.status_code != 200:
        raise Exception(f"IMDB API response {update_request.status_code} status code!")

    return update_request.json()["data"]["rateTitle"]


if __name__ == "__main__":

    title_col = "imdb"
    rating_col = "vote"

    movies_data = read_data(file_path="../kinopoisk/csv/movies_rating.csv", columns=[title_col, rating_col])
    size = movies_data.shape[0] - 1

    for idx, row in movies_data.iterrows():
        print(f"{datetime.now()}, {idx}/{size}, {row[title_col]}")

        imdb_response = update_imdb_rating(row[title_col], row[rating_col])
        print(imdb_response)

    print("All done!")
