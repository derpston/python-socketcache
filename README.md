python-socketcache
==================

A simple pure python cache of UDP socket objects, supporting a custom TTL, IPv{4,6} and random balancing.

Intended to assist in sending a lot of UDP packets to a host addressed by FQDN without burdening the local resolver. The local machine may not have a caching resolver at all, making it a good idea for the application to manage a cache itself.

Features
--------
* Configurable TTL (though it is not pulled from the DNS records)
* IPv4 and IPv6 support, both optional
* Prefers IPv6 where both the local system supports IPv6 and AAAA records exist
* Supports random address choice for round-robin load balancing
* Pure Python
* Debian/Ubuntu package
* Comes with tests

Example
-------
```python
import socketcache

host = socketcache.UDPSocketCache("example.com", 12345)

# Reuse host object.
(sock, addr) = host.get()
sock.sendto("Hello!", addr)
```
Building a new package
----------------------
* Don't forget to update \__version__ in src/socketcache.py and add a new version block to debian/changelog - the build will fail if the versions don't match.
* dpkg-buildpackage -tc
* Run lint checks:

```shell
$ lintian python-socketcache_0.1.0_all.deb
$ 
```

BUGS
----
Unknown.

TODO
----
(empty)

Contributing
------------
Contributions welcome.

