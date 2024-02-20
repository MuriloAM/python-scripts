from OpenSSL import SSL
import socket

dst = ('www.google.com', 443)
ctx = SSL.Context(SSL.SSLv23_METHOD)
s = socket.create_connection(dst)
s = SSL.Connection(ctx, s)
s.set_connect_state()
s.set_tlsext_host_name(dst[0])

s.sendall('HEAD / HTTP/1.0\n\n')
s.recv(16)

certs = s.get_peer_cert_chain()
for pos, cert in enumerate(certs):
   print("Certificate #" + str(pos))
   for component in cert.get_subject().get_components():
       print("Subject %s: %s" % (component))
   print("notBefore:" + cert.get_notBefore())
   print("notAfter:" + cert.get_notAfter())
   print("version:" + str(cert.get_version()))
   print("sigAlg:" + cert.get_signature_algorithm())
   print("digest:" + cert.digest('sha256'))