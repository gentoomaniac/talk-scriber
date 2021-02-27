#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import logging
import sys

import click

from youtube_transcript_api import YouTubeTranscriptApi

log = logging.getLogger(__file__)


def _configure_logging(verbosity):
    loglevel = max(3 - verbosity, 0) * 10
    logging.basicConfig(level=loglevel, format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    if loglevel >= logging.DEBUG:
        # Disable debugging logging for external libraries
        for loggername in 'urllib3':
            logging.getLogger(loggername).setLevel(logging.CRITICAL)


def get_caption_markdown(video_id):
    captions = YouTubeTranscriptApi.get_transcript(video_id)
    return [
        "[{time}](https://youtu.be/{id}?t={seconds}) {text}\n".format(time=str(
            datetime.timedelta(seconds=int(c['start']))),
                                                                      seconds=int(c['start']),
                                                                      id=video_id,
                                                                      text=c["text"]) for c in captions
    ]


def get_metadata_markdown(video_id):
    # https://i1.ytimg.com/vi/fE2KDzZaxvE/hqdefault.jpg
    # https://i1.ytimg.com/vi/fE2KDzZaxvE/maxresdefault.jpg
    pass


@click.group()
@click.option('-v', '--verbosity', help='Verbosity', default=0, count=True)
def cli(verbosity: int):
    _configure_logging(verbosity)
    return 0


@cli.command(name='scribe')
@click.option('-i', '--video-id', help='id of the youtube video', required=True)
def scribe(video_id: str):

    captions = get_caption_markdown(video_id)


if __name__ == '__main__':
    # pylint: disable=E1120
    sys.exit(cli())
