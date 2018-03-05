# Port Finder

Simple tool to findout which service should listen on specified port.

Port list is based on [mephux ports.json](https://github.com/mephux/ports.json) repo


## Usage
### Installing
```
$ pip install -r requirements.txt
$ chmod +x port.py
#optionaly
# ln -s port.py /usr/bin/port [-d path/to/sqlite3_database]
$ port -h
```

### Initializing db
Before first run we have to initialize sqlite3 database
```
$ git submodule update --recursive --remote
# $ ./port [-d path/to/sqlite3_database] -i path/to/ports.json
$ ./port -i data/ports.json/ports.json
```
### Querying
To query just simple add port number
```
$ ./port 80
> PORT: 80,
> PROTO: tcp,
> STATUS: Official [11],
> DESCRIPTION:
> Hypertext Transfer Protocol (HTTP)
```
