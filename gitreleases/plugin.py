#!/usr/bin/python

from sh import git,tar
import re


def _get_next_tags():
    maxv=[0,0,0]
    rever=re.compile(r'^\s*v(\d+)\.(\d+)\.(\d+)\s*$')
    for tag in git.tag(l='v*.*.*'):
        ver = rever.match(tag)
        if ver:
            maxv = max(maxv,map(int,ver.groups()))
    maxv[2] += 1
    return maxv

def _get_branch():
    branch = git('rev-parse','--abbrev-ref', 'HEAD')
    return branch

def _archive(includes):
    tar_args = [git.archive('--format=tar','HEAD'),'czf','archive.tar.gz']
    for pttrn in includes:
        tar_args.append('--include')
        tar_args.append(pttrn)
    import debug
    tar_args.append('@-')
    tar(*tar_args)


def main():
    nextv = _get_next_tags()
    print nextv
    print _get_branch()
    _archive(['assets/*','dependencies/*','dist/*'])
    print '***'

if __name__ == "__main__":
    main()
