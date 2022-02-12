from GoogleNews import GoogleNews
import urllib.parse

googlenews = GoogleNews(lang='en', encode='utf-8')
googlenews.get_news(urllib.parse.quote('Sony'))
result = googlenews.results()
print(result)