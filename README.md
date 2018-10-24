# AOCLCleaner

Cleaner script for Intel FPGA OpenCL (Quartus II) projects

## Author

André Bannwart Perina

## Introduction

This is a simple Python script used to cleanup Quartus II projects created by using Intel FPGA SDK for OpenCL. This script can either maintain the project with minimal reporting files (i.e. it won't likely compile again without a full ```aoc``` run) or delete the whole project, leaving only the ```.aocx|.aoco``` files.

## Licence

See LICENSE file.

## Prerequisites

* Python 3;

## Downloading the repo

```
$ git clone https://github.com/comododragon/aoclcleaner.git
```

## Examples of use

### Ask for usage help

To get a description of all possible options with the script, run without any arguments:
```
$ python3 aoclcleaner.py
```

### Running as an executable

For convenience, you can enable running the script as an executable by enable its ```x``` flag:
```
$ chmod +x aoclcleaner.py
$ ./aoclcleaner.py
```

### Clean a standard AOCL project located at ```/path/to/project```

```
$ ./aoclcleaner.py /path/to/project
```

### Perform a dry-run

If you want to perform a dry-run (i.e. the script runs normally but it won't remove anything):
```
$ ./aoclcleaner.py -d /path/to/project
```

or
```
$ ./aoclcleaner.py --dry-run /path/to/project
```

### Clean an AOCL project located at ```/path/to/project``` where the project file is ```foo.qpf```

```
$ ./aoclcleaner.py -p foo /path/to/project
```

or
```
$ ./aoclcleaner.py -project-name=foo /path/to/project
```

### Recursively iterate inside ```/path/to/projects``` looking for quartus projects and clean all

```
$ ./aoclcleaner.py -r /path/to/projects
```

or
```
$ ./aoclcleaner.py --recursive /path/to/projects
```

### Aggressive cleanup (delete the whole project)

```
$ ./aoclcleaner.py -a /path/to/project
```

or
```
$ ./aoclcleaner.py --aggressive /path/to/projects
