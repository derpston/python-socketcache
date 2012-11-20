import unittest
import socket
import time

import sys
sys.path.insert(0, "../src/")
import socketcache

class TestUDPSocketCache(unittest.TestCase):
   def testGetsSocket(self):
      sc = socketcache.UDPSocketCache("example.com", 80)
      (sock, addr) = sc.get()
      self.assertIsInstance(sock, socket.socket)
  
   def testGetsAddrTuple(self):
      sc = socketcache.UDPSocketCache("example.com", 80)
      (sock, addr) = sc.get()
      self.assertIsInstance(addr, tuple)

   def testCaching(self):
      sc = socketcache.UDPSocketCache("example.com", 80, ttl = 0.1)
      sc.get()

      # Reach into the UDPSocketCache instance and break the host, so if
      # it tries to resolve anything again it'll blow up.
      sc._host = "doesnotexist.example.com"

      # This should not raise an exception because we're calling it within
      # 0.1s of the previous call.
      sc.get()

      # Wait a moment and try again - it should blow up.
      time.sleep(0.2)
      self.assertRaises(Exception, sc.get)

   def testPreservesPort(self):
      sc = socketcache.UDPSocketCache("127.0.0.1", 80)
      (sock, addr) = sc.get()
      (host, port) = addr
      self.assertEqual(port, 80)

   def testWorksWithIPv4Addresses(self):
      sc = socketcache.UDPSocketCache("127.0.0.1", 80)
      (sock, addr) = sc.get()
      (host, port) = addr
      self.assertEqual(host, "127.0.0.1")
   
   def testWorksWithIPv6Addresses(self):
      sc = socketcache.UDPSocketCache("::1", 80)
      (sock, addr) = sc.get()
      (host, port, flow, scope) = addr
      self.assertEqual(host, "::1")
  
   def testPrefersIPv6(self):
      # This will fail if the testing system doesn't have IPv6 support.
      # TODO Detect this with socket.AF_INET6 existance and... how do you
      # mark a test as not applicable/didn't run? Hmm.

      # At the time of test writing, example.com has A and AAAA records.
      # I'm assuming that isn't likely to change.
      sc = socketcache.UDPSocketCache("example.com", 80)
      (sock, addr) = sc.get()
      self.assertEqual(len(addr), 4)
   
   def testRandomBalancing(self):
      # TODO Possibly fudge the socket objects inside, I don't know of a
      # reliable fqdn with multiple A records.
      pass

if __name__ == "__main__":
    unittest.main()
