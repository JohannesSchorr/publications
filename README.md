# Publications from ORCID

Read your bibliographic data from [orcid.org](https://orcid.org/) and transform it to a Markdown or [reStructuredText](https://docutils.sourceforge.io/rst.html) file. 

## Prerequesites

You need following things: 
- a valid *ORCID*
- [requests](https://requests.readthedocs.io/en/latest/) installed

Persons on the orcid-profile must be marked as follows to be recognised / distinguished by ``publications.py``.

Make sure that the **authors**  are marked at least with one of the following: 

- ``'author'`` 
- ``'Writing - original draft'``
- ``'Writing - review & editing'``

**Editors** may be marked as ``'editor'``.

## Usage

### Quickstart

To parse the data of an [orcid.org](https://orcid.org/)-profile, 
you must pass the corresponding ID to ``publications.py`` as an argument.

```
$ python publications.py [ORCID]
```

Using my [ORCID: 0009-0008-8267-272X](https://orcid.org/0009-0008-8267-272X) this looks as follows. 

```
$ python publications.py '0009-0008-8267-272X'
```

This creates a ``publications.txt``-file in the directory, where you called ``publications.py``.
In the ``publications.txt``-file all works from the given ORCID-profile are listed and sorted by year starting with your latest publication.

### Choosing the format

In case you like reStructuredText over Markdown pass ``-format='rst'`` to ``publications.py`` as follows. 
Markdown (``'md'``) is the default configuration.

```
$ python publications.py [ORCID] -format='rst'
```

### Output in other directory

To output the ``publications.txt``-file in another directory pass ``-path='[other/directory/]'`` to ``publications.py``. 
The default is the directory where the file is called (``'./'``).

```
$ python publications.py [ORCID] -path='../my/other/directory/'
```

## Background

For my homepage I wanted to list my publications on one site.
This project is inspired by this [blogpost](https://chrisholdgraf.com/blog/2022/orcid-auto-update/) by Chris Holdgraf. 