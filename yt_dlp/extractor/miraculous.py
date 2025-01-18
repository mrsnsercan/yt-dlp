from yt_dlp.extractor.common import InfoExtractor
from yt_dlp.utils import ExtractorError

class MiraculousIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?miraculous\.to/tr/watch\?s=(?P<id>\d+)'
    _TESTS = [{
        'url': 'https://miraculous.to/tr/watch?s=1',
        'info_dict': {
            'id': '1',
            'title': 'Sample Title',
        },
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        # M3U8 URL'sini bul
        m3u8_url = self._search_regex(
            r'(https?://.*?\.m3u8)', webpage, 'm3u8 url', default=None)
        
        if not m3u8_url:
            raise ExtractorError('M3U8 URL bulunamadı!')

        # Metadata ve başlık
        title = self._html_search_regex(
            r'<title>([^<]+)</title>', webpage, 'title', default=f'Video {video_id}')

        return {
            'id': video_id,
            'title': title,
            'url': m3u8_url,
            'ext': 'mp4',
            'protocol': 'm3u8_native',
        }
