# Port Finder

Simple tool to findout which service should listen on specified port.

Port list is based on [mephux ports.json](https://github.com/mephux/ports.json) repo


## Usage
### Installing
```
$ pip install -r requirements.txt
$ chmod +x port.py
#optionaly
# ln -s path/to/port.py /usr/bin/port
$ port -h
```

### Initializing db
Before first run we have to initialize sqlite3 database
```
$ git submodule init
$ git submodule update --recursive --remote
# example usage: ./port.py [-d path/to/sqlite3_database] -i path/to/ports.json
$ ./port -i data/ports.json/ports.json
```
### Querying
To query just simple add port number
```
$ ./port 80
> [+] PORT: 80,
> PROTO: tcp,
> STATUS: Official [11],
> DESCRIPTION:
> Hypertext Transfer Protocol (HTTP)

#mutliple services on same port
$ port 9999
> [+] PORT: 9999,
> PROTO: tcp,
> STATUS: Unofficial,
> DESCRIPTION:
> Hydranode—edonkey2000 TELNET control
> [+] PORT: 9999,
> PROTO: tcp,
> STATUS: Unofficial,
> DESCRIPTION:
> Lantronix UDS-10/UDS100[105] RS-485 to Ethernet Converter TELNET control
> [+] PORT: 9999,
> PROTO: tcp,
> STATUS: Unofficial,
> DESCRIPTION:
> Urchin Web Analytics[citation needed]

#ports using tcp and udp proto
$ port 53
> [+] PORT: 53,
> PROTO: tcp|udp,
> STATUS: Official,
> DESCRIPTION:
> Domain Name System (DNS) 
```
