import asyncio
import unittest
import yt_dlp as youtube_dl
from arcbot.audio_fetcher import core as audio_fetcher


class TestFetchAudioFile(unittest.TestCase):

    def test_fetch_audio_file_valid_url(self):
        # test a valid YouTube URL
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        title, audio_url, original_url = asyncio.get_event_loop().run_until_complete(
            audio_fetcher.fetch_audio_file(url))
        self.assertEqual(title,
                         "Rick Astley - Never Gonna Give You Up (Official Music Video)")  # check if the title is correct
        self.assertTrue(audio_url.startswith("https://"))  # check if the audio URL is valid

    def test_fetch_audio_file_invalid_url(self):
        # test an invalid URL
        url = "https://www.example.com"
        with self.assertRaises(youtube_dl.utils.DownloadError):  # expect an exception to be raised
            asyncio.get_event_loop().run_until_complete(audio_fetcher.fetch_audio_file(url))

    def test_fetch_audio_file_search_query(self):
        # test a search query
        url = "ytsearch:despacito"
        title, audio_url, original_url = asyncio.get_event_loop().run_until_complete(audio_fetcher.fetch_audio_file(url))
        self.assertEqual(title, "Luis Fonsi - Despacito ft. Daddy Yankee")  # check if the title is correct
        self.assertTrue(audio_url.startswith("https://"))  # check if the audio URL is valid

    def test_fetch_audio_file_non_youtube_url(self):
        # test a non-YouTube URL that is supported by youtube-dl
        url = "https://soundcloud.com/alanwalker/alan-walker-fade"
        title, audio_url, original_url = asyncio.get_event_loop().run_until_complete(audio_fetcher.fetch_audio_file(url))
        self.assertEqual(title, "Fade")  # check if the title is correct
        self.assertTrue(audio_url.startswith("https://"))  # check if the audio URL is valid

    def test_fetch_audio_file_unsupported_url(self):
        # test a URL that is not supported by youtube-dl
        url = "https://www.wikipedia.org/"
        with self.assertRaises(youtube_dl.utils.DownloadError):  # expect an exception to be raised
            asyncio.get_event_loop().run_until_complete(audio_fetcher.fetch_audio_file(url))

    def test_fetch_audio_file_empty_url(self):
        # test an empty URL
        url = ""
        with self.assertRaises(youtube_dl.utils.DownloadError):  # expect an exception to be raised
            asyncio.get_event_loop().run_until_complete(audio_fetcher.fetch_audio_file(url))


if __name__ == '__main__':
    unittest.main()
