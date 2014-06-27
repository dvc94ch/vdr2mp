from datetime import datetime
from os.path import dirname, realpath, join
from unittest import TestCase

from main.vdr2mp import stringify, start_time, end_time, get_info_and_ts_files, parse_info_file


class InfoFileParsingTestCase(TestCase):

    unix_time = 1403618279
    duration = 4500
    start_time = datetime(2014, 6, 24, 15, 57, 59)
    end_time = datetime(2014, 6, 24, 17, 12, 59)
    stringified = '2014-06-24 15:57'

    def test_stringify(self):
        self.assertEquals(stringify(self.start_time), self.stringified)
        self.assertEquals(stringify(self.stringified), self.stringified)
        self.assertEquals(stringify(5), '5')

    def test_start_time(self):
        self.assertEquals(start_time(self.unix_time), self.start_time)

    def test_end_time(self):
        self.assertEquals(end_time(self.start_time, self.duration), self.end_time)

    def test_parse_info_file(self):
        self.assertEquals(parse_info_file("""
            C S19.2E-1-1011-11100 Das Erste HD
            E 40747 1303617600 4500 4E 1C
            T TITLE
            S GENRE
            D COMMENT
        """), {
            'title': 'TITLE',
            'genre': 'GENRE',
            'comment': 'COMMENT',
            'channelname': 'Das Erste HD',
            'starttime': '1303617600',
            'duration': '4500'
        })


class InputdirParsingTestCase(TestCase):

    tests_path = dirname(realpath(__file__))
    inputdir_path = join(tests_path, 'inputdir')
    folderdir_path = join(inputdir_path, 'Untitled.Folder')
    infofile_path = join(folderdir_path, 'info')
    tsfile1_path = join(folderdir_path, '00001.ts')
    tsfile2_path = join(folderdir_path, '00002.ts')

    def test_get_info_and_ts_files(self):
        self.assertEquals(
            get_info_and_ts_files(self.folderdir_path), (self.infofile_path, [self.tsfile1_path, self.tsfile2_path]))
