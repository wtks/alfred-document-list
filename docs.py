import sys
import os.path
import codecs
from workflow import Workflow

ROOT_PATH = os.path.expanduser('~/Documents/')


def main(wf):
    args = wf.args
    dirs = getdirs(ROOT_PATH)
    if len(args) == 0 or all(x != args[0] for x in dirs):
        query = None
        if len(args) >= 1:
            query = args[0]
        for dir in wf.filter(query, dirs):
            desc = ''
            desc_file = os.path.join(ROOT_PATH, dir, '.description')
            if os.path.isfile(desc_file):
                with codecs.open(desc_file, 'r', 'utf-8') as f:
                    desc = f.read()
            wf.add_item(
                dir,
                desc,
                arg=ROOT_PATH + dir,
                autocomplete=dir + ' ',
                icon='public.folder',
                icontype='filetype',
                type='file',
                valid=True,
                quicklookurl=ROOT_PATH+dir)
    else:
        files = getfiles(ROOT_PATH + args[0])
        files.sort()
        query = None
        if len(args) >= 2:
            query = args[1]
        files = wf.filter(query, files)
        for f in files:
            path = os.path.join(ROOT_PATH, args[0], f)
            wf.add_item(
                f,
                'Press shift to preview...',
                arg=path,
                icon=f,
                icontype='fileicon',
                type='file',
                valid=True,
                quicklookurl=path)

    wf.send_feedback()


def getdirs(path):
    dirs = []
    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path, item)):
            dirs.append(item)
    return dirs


def getfiles(path):
    dirs = []
    for item in os.listdir(path):
        if item[0] != '.' and os.path.isfile(os.path.join(path, item)):
            dirs.append(item)
    return dirs


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))