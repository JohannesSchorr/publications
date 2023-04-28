# Publications from ORCID

Read your bibliographic data from [orcid.org](https://orcid.org/) and transform it to a markdown file. 

## Prerequesites

You need following things: 
- a valid *ORCID*
- [requests](https://requests.readthedocs.io/en/latest/) installed

## Usage
To parse the data of an [orcid.org](https://orcid.org/)-profile, 
you must pass a the ORCID to ``publications.py`` as an argument.

```
$ python publications.py [ORCID]
```

Using my [ORCID: 0009-0008-8267-272X](https://orcid.org/0009-0008-8267-272X) this looks as follows. 

```
$ python publications.py '0009-0008-8267-272X'
```

This creates a ``publications.txt``-file in the directory, where you called ``publications.py``.
In the ``publications.txt``-file all works from the given ORCID-profile are listed and sorted by year starting with your latest publication.

## Background

For my homepage I wanted to list my publications on one site.
This project is inspired by this [blogpost](https://chrisholdgraf.com/blog/2022/orcid-auto-update/) by Chris Holdgraf. 