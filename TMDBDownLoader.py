import requests
from config import TMDB_API_Key_v3_auth
import imdb


def size_str_to_int(x: str) -> int:
    """sorting function to get the biggest picture size """
    return float("inf") if x == 'original' else int(x[1:])


class TMDBDownloader:
    content_temp_path="./temp_content/"
    def __init__(self):
        self.CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key={key}'
        self.base_url = 'http://d3gtl9l2a4fn1j.cloudfront.net/t/p/'
        self.IMG_PATTERN = 'http://api.themoviedb.org/3/movie/{imdbid}/images?api_key={key}'
        self.KEY = TMDB_API_Key_v3_auth
        self.url = self.CONFIG_PATTERN.format(key=self.KEY)
        self.config = requests.get(self.url).json()
        self.base_url = self.config['images']['base_url']
        self.sizes = self.config['images']['poster_sizes']
        self.max_size = max(self.sizes, key=size_str_to_int)  # use the sort function in max to get biggest size

    def getIMDBID(self, name):
        ia = imdb.IMDb()
        search = ia.search_movie(name)
        return "tt" + str(search[0].movieID)

    def getPoster(self, imdbid, name):
        api_response = requests.get(self.IMG_PATTERN.format(key=self.KEY, imdbid=imdbid)).json()
        posters = api_response['posters']
        poster_urls = []
        for poster in posters:
            rel_path = poster['file_path']
            url = "{0}{1}{2}".format(self.base_url, self.max_size, rel_path)
            poster_urls.append(url)
        # single poster download

        r = requests.get(poster_urls[0])
        filetype = r.headers['content-type'].split('/')[-1]
        filename = 'poster_{0}.{1}'.format(name, filetype)
        with open(self.content_temp_path+filename, 'wb') as w:
            w.write(r.content)

        return filename


    def search_and_download(self,movie_name):
        """ returns tuple imdb_id,file_name"""
        imdb_id = self.getIMDBID(movie_name)
        file_name=self.getPoster(imdb_id, movie_name)
        return (imdb_id, file_name)


if __name__ == "__main__":
    TMDBconn = TMDBDownloader()
    # movie_name="spiderman"
    # TMDBconn.search_and_download(movie_name)