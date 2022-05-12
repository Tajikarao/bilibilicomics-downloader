import json

import requests


class BiliComics:
    def __init__(self) -> None:
        self.session = requests.session()
        self.endpoints = {
            "GetImageIndex": "https://www.bilibilicomics.com/twirp/comic.v1.Comic/GetImageIndex?device=android",
            "ImageToken": "https://www.bilibilicomics.com/twirp/comic.v1.Comic/ImageToken",
        }

    def getEpisode(self, episode_id: int) -> json:
        payload = {
            "ep_id": episode_id,
        }

        return self.session.post(self.endpoints["GetImageIndex"], json=payload).json()

    def getToken(self, url):
        payload = {"urls": json.dumps([url])}

        return self.session.post(self.endpoints["ImageToken"], json=payload).json()

    def downloadImages(self, episode_data: json) -> list:
        images = episode_data["data"]["images"]

        for i, dict in enumerate(images):
            uncomplet_path = f'{images[i]["path"]}@{dict["x"]}w.png'
            complet_path = self.getToken(uncomplet_path)["data"][0]

            url = f'{complet_path["url"]}?token={complet_path["token"]}'

            with requests.get(url, stream=True) as r:
                with open(f"{i}.png", "wb") as file:
                    for chunk in r.iter_content(chunk_size=1024):
                        file.write(chunk)


if __name__ == "__main__":
    bilicomics = BiliComics()
    episode_data = bilicomics.getEpisode(5853)

    bilicomics.downloadImages(episode_data)
