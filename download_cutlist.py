from cutlists import Cutlist
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        num_args = len(sys.argv)
        filename = sys.argv[1]

        if num_args > 2:
            filesize = sys.argv[2]
        else:
            filesize = 0
        
        if num_args > 3:
            folder = sys.argv[3]
        else:
            folder = ''

        c=Cutlist(filename,filesize)
        ret = c.search(mode='ofsb')
        if ret == 1:
            ret = c.search(mode='name')

        c.sort_cutlists()
        ret=c.download(toprated=True, folder=folder)

        exit(ret)

    else:
        print 'Usage: ' + sys.argv[0] + ' filename filesize'