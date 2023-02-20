#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import logging
import os
import sys

import click
import requests

from pyyoutube import Api
from youtube_transcript_api import YouTubeTranscriptApi

log = logging.getLogger(__file__)


def _configure_logging(verbosity: int):
    loglevel = max(3 - verbosity, 0) * 10
    logging.basicConfig(level=loglevel, format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    if loglevel >= logging.DEBUG:
        # Disable debugging logging for external libraries
        for loggername in 'urllib3':
            logging.getLogger(loggername).setLevel(logging.CRITICAL)


def get_preview_image(img_url: str, video_id: str, img_path: str = 'img'):
    img_file_name = os.path.join(img_path, video_id) + '.jpg'
    with open(img_file_name, 'wb') as handle:
        response = requests.get(img_url, stream=True)

        if not response.ok:
            log.warning("Couldn't fetch preview: %s", response)
            return None

        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)

        return img_file_name

    return None


def gen_markdown_page(video_id: str, title: str, image_path: str, description: str, date: datetime, captions: list):
    markdown = ""

    markdown += "# {title} ({date})\n\n".format(title=title, date=date.strftime("%Y-%m-%d"))
    markdown += "![alt {title}]({img_path} \"{title}\")\n\n".format(title=title, img_path=image_path)
    markdown += "## Description\n\n"
    markdown += description.strip()
    markdown += "\n\n"
    markdown += "## Transcript\n\n"
    for c in captions:
        markdown += "[{time}](https://youtu.be/{id}?t={seconds}) {text}  \n".format(time=str(
            datetime.timedelta(seconds=int(c['start']))),
                                                                                    seconds=int(c['start']),
                                                                                    id=video_id,
                                                                                    text=c["text"])

    return markdown


def gen_srt(captions: list) -> list:
    srt = []

    captions = [{
        'text': c['text'],
        'start': datetime.timedelta(seconds=c['start']),
        'end': datetime.timedelta(seconds=c['start']) + datetime.timedelta(seconds=c['duration'])
    } for c in captions]

    for i in range(len(captions)):
        if i < len(captions) - 1:
            if captions[i]['end'] > captions[i + 1]['start']:
                captions[i]['end'] = captions[i + 1]['start'] - datetime.timedelta(seconds=0.001)
        srt.append(gen_srt_frame(caption=captions[i]))

    return srt


def gen_srt_frame(caption: dict) -> dict:
    return {
        'timing': "{start} --> {end}".format(start=str(caption['start'])[:-3], end=str(caption['end'])[:-3]),
        'text': caption['text']
    }


@click.group()
@click.option('-v', '--verbosity', help='Verbosity', default=0, count=True)
def cli(verbosity: int):
    _configure_logging(verbosity)
    return 0


@cli.command(name='scribe')
@click.option('-i', '--video-id', help='id of the youtube video', required=True)
@click.option('-k', '--youtube-api-key', help='youtube api key', default=os.getenv('YOUTUBE_API_KEY'))
def scribe(video_id: str, youtube_api_key: str):

    if not youtube_api_key:
        log.error('You need to provide an API key either by --youtube-api0key or by setting YOUTUBE_API_KEY')
        sys.exit(1)

    api = Api(api_key=youtube_api_key)
    video_metadata = api.get_video_by_id(video_id=video_id).items[0]

    #log.debug(json.dumps(video_metadata.to_dict(), sort_keys=True, indent=2))

    title = video_metadata.snippet.title
    preview_image_path = get_preview_image(img_url=video_metadata.snippet.thumbnails.default.url, video_id=video_id)
    description = video_metadata.snippet.description
    date = datetime.datetime.strptime(video_metadata.snippet.publishedAt, "%Y-%m-%dT%H:%M:%S%z")
    captions = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'de'])

    print(
        gen_markdown_page(video_id=video_id,
                          title=title,
                          image_path=preview_image_path,
                          description=description,
                          date=date,
                          captions=captions))


@cli.command(name='srt')
@click.option('-i', '--video-id', help='id of the youtube video', required=True)
@click.option('-k', '--youtube-api-key', help='youtube api key', default=os.getenv('YOUTUBE_API_KEY'))
def scribe(video_id: str, youtube_api_key: str):

    if not youtube_api_key:
        log.error('You need to provide an API key either by --youtube-api0key or by setting YOUTUBE_API_KEY')
        sys.exit(1)

    api = Api(api_key=youtube_api_key)

    captions = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'de'])

    srt_frames = gen_srt(captions=captions)
    for i in range(len(srt_frames)):
        print("""{frame_index}
{timing}
{text}
        """.format(frame_index=i, timing=srt_frames[i]['timing'], text=srt_frames[i]['text']))


if __name__ == '__main__':
    # pylint: disable=E1120
    sys.exit(cli())
