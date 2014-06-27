from datetime import datetime, timedelta
from os import listdir
from os.path import isfile, isdir, join
from re import compile
from sys import argv


title_regex = 'T (.*)\n'
genre_regex = 'S (.*)\n'
comment_regex = 'D (.*)\n'
channelname_regex = 'C \S* (.*)\n'
starttime_duration_regex = 'E \d* (\d*) (\d*).*\n'


def stringify(date_time):
    if hasattr(date_time, 'strftime'):
        return date_time.strftime('%Y-%m-%d %H:%M')
    return str(date_time)


def start_time(unix_time):
    return datetime.fromtimestamp(int(unix_time))


def end_time(date_time, duration):
    return date_time + timedelta(seconds=duration)


def read_file(path):
    if isfile(path):
        return open(path, 'r').read()


def parse_info_file(text):
    start_time_duration = compile(starttime_duration_regex).search(text)

    return {
        'title': compile(title_regex).search(text).group(1),
        'genre': compile(genre_regex).search(text).group(1),
        'comment': compile(comment_regex).search(text).group(1),
        'channelname': compile(channelname_regex).search(text).group(1),
        'starttime': start_time_duration.group(1),
        'duration': start_time_duration.group(2)
    }


def get_info_and_ts_files(wdir):
    infofile = join(wdir, 'info')
    tsfiles = []

    if not isfile(infofile):
        raise Exception('No info file found')

    for tsfile in listdir(wdir):
        if tsfile.endswith('.ts'):
            tsfiles.append(join(wdir, tsfile))

    return infofile, tsfiles


if __name__ == '__main__':
    INPUTDIR = argv[1]
    OUTPUTDIR = argv[2]

    for subdir in listdir(INPUTDIR):
        if isdir(subdir):
            get_info_and_ts_files(join(INPUTDIR, subdir))