#!/usr/bin/python

import sys
import socket
import random
import struct
import dnslib.dns

dns_server_ip = '192.168.1.1'
dns_server_port = 53


def pack(value):

    '''pentru a crea header-ul

    '''

    return struct.pack('>H', value)

class HeaderQuery:

	def __init__(self,request):
			self.id = random.randint(0, 65535)
			self.qr = 0 
			'''pentru ca e query este setat pe 0'''
			self.opcode = 0 
			'''standard query'''
			self.aa = 0 
			'''Non authoritative answer'''
			self.tc = 0
			self.rd = 0
			'''IMPORTANT nu dorim sa caute mai departe pe alte servere => recursion not desired'''
			self.ra = 0 
			'''recursion not available'''
			self.rcode = 0
			self.qd_count = 1
			'''Numarul de questions/ answers/ authoritative answers/ Additional answers '''
			self.an_count = 0
			self.ns_count = 0
			self.ar_count = 0
			
			self.nume = request
			self.tip = 1
			self.request_class=1
		
	
	def CreareHeader(self):
			headerFinal = pack(self.id)
			'''Pentru a adauga fiecare flag shiftam auxiliarul in functie de cati biti are fiecare flag'''
			aux = 0
			aux = 0
			aux |= self.qr
			aux <<= 1
			aux |= self.opcode
			aux <<= 4
			aux |= self.aa
			aux <<= 1
			aux |= self.tc
			aux <<= 1
			aux |= self.rd
			aux <<= 1
			aux |= self.ra
			aux <<= 7
			aux |= self.rcode
			headerFinal += pack(aux)
			headerFinal += pack(self.qd_count)
			headerFinal += pack(self.an_count)
			headerFinal += pack(self.ns_count)
			headerFinal += pack(self.ar_count)
			return headerFinal
			
	def Codare_Nume(self):
			nume = self.nume
			if nume.endswith('.'):
				nume = nume[:-1]

			result = b''

			for domain_name in nume.split('.'):
				result += struct.pack('B', len(domain_name))
				result += bytes(domain_name, 'utf-8')
			result += b'\x00'
			return result
			
	def CreareInterogare(self):
			'''encode question

        '''
			result = self.Codare_Nume()
			result += pack(self.tip)
			result += pack(self.request_class)
			return result

	def CreareQuery(self, request):
			mesaj = b''
			self.header = self.CreareHeader()
			mesaj = mesaj + self.header
			self.question = self.CreareInterogare()
			mesaj = mesaj + self.question
			return mesaj




class ClientCache:
	
	'''Clientul care se va conecta la serverul DNS'''
	''' Conexiunea la server-ul dns local pe portul 53'''
	def __init__(self):
		try:
			self.connection_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.connection_socket.connect((dns_server_ip,dns_server_port))
			print('S-a stabilit conexiunea cu serverul')

		except Exception:
			print('Nu se poate conecta la server {0}'.format(dns_server_ip))
	
	def TrimiteQuery(self,request):
		formator=HeaderQuery(request)
		query=formator.CreareQuery(request)
		self.connection_socket.send(query)
		try:
			raspuns = self.connection_socket.recv(100)
			print(raspuns)
		except Exception:
			print('Nu s-a gasit')

		
	def Deconectare(self):
		self.connection_socket.close()
		

if __name__ == '__main__':
	client=ClientCache()
	client.TrimiteQuery(sys.argv[1])
	client.Deconectare
		
	

	
	
	
	
	