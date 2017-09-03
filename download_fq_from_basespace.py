import sys, os, glob, logging
from BaseSpacePy.api.BaseSpaceAPI import BaseSpaceAPI
from BaseSpacePy.model.QueryParameters import QueryParameters as qp
listOptions = qp({'Limit': 1024})

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')
myAPI = BaseSpaceAPI()

p = sys.argv[1]
user = myAPI.getUserById('current')
logging.info("User Name: %s" % str(user))
projects = myAPI.getProjectByUser(listOptions)
project_list = [project.Name for project in projects]

try:
    idx = project_list.index(sys.argv[1])
    project = projects[idx]
except ValueError:
    message = '"%s" is not in your projects. Available projects are:\n%s' % \
              (sys.argv[1],
               '\n'.join(project_list))
    logging.error(message)
    sys.exit(1)

downloaded = glob.glob('*fastq.gz') # get already downloaded fastq

logging.info("Retrieving samples from project %s" % sys.argv[1])
samples=project.getSamples(myAPI,listOptions)
logging.info("Samples for this project: %s" % str(samples))

for sample in samples:
    logging.info("Retrieving files in sample %s" % str(sample))
    for f in sample.getFiles(myAPI):
        if f.Name not in downloaded:
            logging.info("Downloading file %s" % f.Name)
            f.downloadFile(myAPI, '.')
