#!/usr/bin/python

from codecs import getwriter
from datetime import datetime, timedelta
from os import listdir, makedirs, system, walk
from os.path import exists, isfile, join, dirname, basename
from re import compile
from sys import argv

debug = True

title_regex = '\nT (.*)\n'
episodename_regex = '\nS (.*)\n'
comment_regex = '\nD (.*)\n'
genre_regex = '\nG (.*)\n'
channelname_regex = 'C \S* (.*)\n'
starttime_duration_regex = 'E \d* (\d*) (\d*).*\n'


def stringify(date_time):
    if hasattr(date_time, 'strftime'):
        return date_time.strftime('%Y-%m-%d %H:%M')
    return str(date_time)


def start_time(unix_time):
    return datetime.fromtimestamp(unix_time)


def end_time(date_time, duration):
    return date_time + timedelta(seconds=duration)


def read_file(path):
    if isfile(path):
        return open(path, 'r').read()


def write_file(path, content):
    directory = dirname(path)
    if not exists(directory):
        makedirs(directory)

    getwriter('utf-8')(file(path, 'w')).write(content.decode('utf-8', 'ignore'))


def apply_regex(regex, text):
    result = compile(regex).search(text)
    if result is None:
        return ''
    return result.group(1)


def parse_info_file(text):
    start_time_duration = compile(starttime_duration_regex).search(text)
    starttime = start_time(int(start_time_duration.group(1)))
    endtime = end_time(starttime, int(start_time_duration.group(2)))

    return {
        'title': apply_regex(title_regex, text),
        'episodename': apply_regex(episodename_regex, text),
        'comment': apply_regex(comment_regex, text),
        'genre': apply_regex(genre_regex, text),
        'channelname': apply_regex(channelname_regex, text),
        'starttime': starttime,
        'endtime': endtime
    }


def get_info_and_ts_files(path):
    possible_infofile_names = ['info', 'Info', 'Info.txt', 'info.txt']

    infofile = None
    for infofile_name in possible_infofile_names:
        if isfile(join(path, infofile_name)):
            infofile = join(path, infofile_name)

    if infofile is None:
        return None, None

    tsfiles = []
    for tsfile in listdir(path):
        if tsfile.endswith('.ts'):
            tsfiles.append(join(path, tsfile))

    tsfiles.sort()

    if debug:
        print 'directory: %s, infofile: %s, tsfiles: %s' % (
            dirname(infofile), basename(infofile), [basename(tsfile) for tsfile in tsfiles])

    return infofile, tsfiles


def mp_simple_tag(name, value):
    return '<SimpleTag><name>%s</name><value>%s</value></SimpleTag>\n' % (name, stringify(value))


def generate_mp_file(values):
    return """<?xml version="1.0" encoding="UTF-8"?>\n<tags>\n<tag>\n%s</tag>\n</tags>""" % (
        mp_simple_tag('TITLE', values['title']) +
        mp_simple_tag('EPISODENAME', values['episodename']) +
        mp_simple_tag('COMMENT', values['comment']) +
        mp_simple_tag('GENRE', values['genre']) +
        mp_simple_tag('CHANNEL_NAME', values['channelname']) +
        mp_simple_tag('STARTTIME', values['starttime']) +
        mp_simple_tag('ENDTIME', values['endtime'])
    )


def output_file_name(values, extension):
    return '%s - %s - %s.%s' % (values['title'], values['channelname'], values['starttime'].strftime('%Y-%m-%d %H_%M'), extension)


def output_file_path(outputdir, values, extension):
    return join(outputdir, output_file_name(values, extension))


def ts_cmd(tsfiles, output_path):
    cat = 'cat "%s" > "%s"' % ('" "'.join(tsfiles), output_path)

    system(cat)


def convert(path):
    infofile, tsfiles = get_info_and_ts_files(path)

    if infofile is None:
        return

    values = parse_info_file(read_file(infofile))
    write_file(output_file_path(OUTPUTDIR, values, 'xml'), generate_mp_file(values))
    ts_cmd(tsfiles, output_file_path(OUTPUTDIR, values, 'ts'))


if __name__ == '__main__':
    INPUTDIR = argv[1]
    OUTPUTDIR = argv[2]

    if debug:
        print 'Inputdir: %s, Outputdir: %s' % (INPUTDIR, OUTPUTDIR)

    for root, dirs, files in walk(INPUTDIR):
        if len(dirs) == 0:
            convert(root)
