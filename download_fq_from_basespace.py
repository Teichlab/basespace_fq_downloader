#!/usr/bin/env python2.7

from __future__ import print_function

import sys, os, glob, logging
from argparse import ArgumentParser

from BaseSpacePy.api.BaseSpaceAPI import BaseSpaceAPI
from BaseSpacePy.model.QueryParameters import QueryParameters as qp


list_options = qp({'Limit': 1024})

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S',
)
bs = BaseSpaceAPI()


user = bs.getUserById('current')
logging.info("User Name: %s", user)
projects = bs.getProjectByUser(list_options)
project_list = [project.Name for project in projects]

cli = ArgumentParser()
cli.add_argument('project', nargs='?', help='Which project to download files from. When not specified, list projects instead.')
cli.add_argument('--dry-run', '-n', action='store_true', help='Only show which files would be downloaded without downloading them.')
cli.add_argument('--dir', '-d', default='.', help='Directory to download samples to.')
args = cli.parse_args()

if not args.project:
    print(*project_list, sep='\n')
    sys.exit(0)

p = args.project

try:
    idx = project_list.index(p)
    project = projects[idx]
except ValueError:
    logging.error(
        '%r is not in your projects. Available projects are:\n%s',
        p, '\n'.join(project_list),
    )
    sys.exit(1)

# get already downloaded fastq
downloaded = {f.split('/')[-1] for f in glob.glob(args.dir + '/*fastq.gz')}

logging.info("Retrieving samples from project %s", p)
samples = project.getSamples(bs, list_options)
logging.info("Samples for this project: %s", samples)

for sample in samples:
    logging.info("Retrieving files in sample %s", sample)
    for f in sample.getFiles(bs):
        if f.Name not in downloaded:
            logging.info("Downloading file %s", f.Name)
            if args.dry_run:
                continue
            f.downloadFile(bs, args.dir)
