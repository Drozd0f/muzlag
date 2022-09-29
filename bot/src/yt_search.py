import youtube_dl

from bot.errors.yt_search import URLNotValid


youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YoutubeSearch:
    def __init__(self, data: dict):
        self.data = data
        self.video_id = data.get('id')
        self.title = data.get('title')
        self.url = data.get('url')
        self.start_time = data.get('start_time', 0)

    @classmethod
    def from_url(cls, url: str):
        if not url.startswith('http') or not url.startswith('https'):
            raise URLNotValid
        data = ytdl.extract_info(url, download=False)
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        return cls(data)
