import yt_dlp as youtube_dl

from bot.errors.yt_search import URLNotValid

DEFAULT_RESOLUTION = ''
DEFAULT_ASR = 0
DEFAULT_FRAGMENTS = []

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
        self.url = data.get('url')  # url to download music from
        self.base_url = data.get('base_url')  # raw unformatted url
        self.start_time = data.get('start_time', 0)

    @classmethod
    def from_url(cls, url: str):
        if not url.startswith('http') or not url.startswith('https'):
            raise URLNotValid
        data = ytdl.extract_info(url, download=False)
        # if 'entries' in data:
        #     # take first item from a playlist
        #     data = data['entries'][0]
        for format in data.get('formats'):
            resolution = format.get('resolution', DEFAULT_RESOLUTION)
            asr = format.get('asr', DEFAULT_ASR)
            if resolution == 'audio only' and asr == 48000:
                data['formats'] = format
                break

        data.update({'base_url': url})  # push base url for database usage
        return cls(data)
