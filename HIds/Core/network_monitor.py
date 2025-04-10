import scapy.all as scapy
from datetime import datetime
import pandas as pd

class NetworkMonitor:
    def __init__(self, interface):
        self.interface = interface
        self.log_file_path = r"IDS\HIds\logs\network_traffic.log"
        self.blacklisted_ip_file_path = r"IDS\HIds\logs\blacklisted_IP.csv"

    def packet_callback(self, packet):
        # TimeStamp of packet creation
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Write packet information to file
        with open(self.log_file_path, "a") as log_file:  # Use "a" to append to the log file
            log_file.write(f"{time} - {packet.summary()}\n")
            if packet.haslayer('IP'):
                src_ip = packet['IP'].src
                dst_ip = packet['IP'].dst
                print(f"Packet detected from {src_ip} to {dst_ip}")
                self.check_blacklisted_ip(src_ip)

    def check_blacklisted_ip(self, src_ip):
        with open(self.blacklisted_ip_file_path, "r") as ip_file:
            datareader = pd.read_csv(ip_file)
            # Assuming the blacklisted IPs are in a column named 'IP'
            blacklisted_ips = datareader['IP'].tolist()
            if src_ip in blacklisted_ips:
                print("Warning!!! Request sent from Blacklisted IP!")

    def start_sniffing(self):
        print(f"Starting network monitoring on {self.interface}...")
        scapy.sniff(iface=self.interface, prn=self.packet_callback, store=False)

