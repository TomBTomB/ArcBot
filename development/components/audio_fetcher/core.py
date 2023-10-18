import yt_dlp as youtube_dl

from development.components.log.core import get_logger

logger = get_logger('arcBot-logger')

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
    'skip_download': True
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


async def fetch_audio_file(url: str) -> (str, str):
    """
    Fetches an audio file from a URL or name
    :param url: URL to fetch the audio file from.
    :returns: (title, url)
    """
    logger.info(f'Fetching audio file: {url}')
    data = ytdl.extract_info(url, download=False)
    if 'entries' in data:
        # take first item from a playlist
        data = data['entries'][0]
    logger.info(f'Fetched audio file: {data["title"]}, {data["url"]}, {data["original_url"]}')
    return data['title'], data['url'], data['original_url']
