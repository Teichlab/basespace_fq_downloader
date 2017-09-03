# basespace_fq_downloader
A fastq downloader from basespace that actually works.

# Description
If using walk up service, the sequencing data won't go through Sanger pipeline. The files are located in Illumina BaseSpace.

Illumina has a python script for downloading data, but it won't give you fastq files. You can download fastq files following this instruction https://gist.github.com/lh3/54f535b11a9ee5d3be8e but you have to do it one by one.

This script download all fastq files associated with a project. I found out that when you have many files in a project, the download often stops randomly, and gives you an error message like this:

`ssl.SSLError: ('The read operation timed out',)`

This script handles that situation by ignoring already downloaded fastq files, so if donwload terminates prematurally, simply run it again.

# Usage
1. Go to this link and follow the instructions to get you access credentials including Client Id, Client Secret, and Access Token (Illumina's python script is also there): https://help.basespace.illumina.com/articles/tutorials/using-the-python-run-downloader/

2. Create a file called `.basespacepy.cfg` in your home directory with the following content:

```
[DEFAULT]
clientKey = your_Client_Id
clientSecret = your_Client_Secret
accessToken = your_Access_Token
apiServer = https://api.basespace.illumina.com/
apiVersion = v1pre3
```

3. Protect that file by `chmod 600 ~/.basespacepy.cfg`

4. Install BaseSpacePy (seems to be python 2 only): https://github.com/basespace/basespace-python-sdk

5. Create a directory where you want to put your fastq files, and run:

```
python download_fq_from_basespace.py your_project_name
```
