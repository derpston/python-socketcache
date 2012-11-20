import random
import socket
import time

__version__ = "0.1.0"

class UDPSocketCache:
   """Maintains a cache of SOCK_DGRAM socket objects for `ttl` seconds, preferring IPv6 over IPv4 and respecting random balancing. `ttl` defaults to 60 seconds, and `family` defaults to both IPv4 and v6."""
   def __init__(self, host, port, ttl = 60, family = socket.AF_UNSPEC):
      self._host = host
      self._port = port
      self._ttl = ttl
      self._family = family

      self._next_update = None
      self._v4sockets = []
      self._v6sockets = []

   def _refresh(self):
      """Refreshes the internal socket cache. Performs a blocking DNS lookup."""
      v6new = []
      v4new = []
      sockets = socket.getaddrinfo(self._host, self._port, self._family, socket.SOCK_DGRAM)
      for (family, socktype, proto, canonname, sockaddr) in sockets:
         sock = socket.socket(family, socktype, proto)

         if family == socket.AF_INET:
            v4new.append((sock, sockaddr))
         
         try:
            if family == socket.AF_INET6:
               v6new.append((sock, sockaddr))
         except AttributeError:
            # No v6 support on this system.
            pass
      
      # Update socket lists if there are any results at all. If there were
      # no results, update the _next_update threshold anyway to continue
      # returning the old results.
      if len(v6new) > 0 or len(v4new) > 0:
         self._v6sockets = v6new
         self._v4sockets = v4new
      self._next_update = time.time() + self._ttl

   def get(self):
      """Returns a tuple of (sock, addr) where sock is a socket object suitable for sending UDP packets to addr."""
      if self._next_update is None or time.time() > self._next_update:
         self._refresh()
      
      # Prefer to return v6 sockets if we have any.
      if len(self._v6sockets) > 0:
         return random.choice(self._v6sockets)
      elif len(self._v4sockets) > 0:
         return random.choice(self._v4sockets)
      else:
         return None

