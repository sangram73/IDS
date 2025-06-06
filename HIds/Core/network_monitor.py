import scapy.all as scapy
from datetime import datetime
import pandas as pd
import threading
import time

class NetworkMonitor:
    def __init__(self, interface):
        self.interface = interface
        self.log_file_path = r"HIds\logs\network_traffic.log"
        self.blacklisted_ip_file_path = r"HIds\logs\blacklisted_IP.csv"
        self.sniffing = False  # Flag to control sniffing

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
        self.sniffing = True
        # Start sniffing in a separate thread
        threading.Thread(target=self._sniff).start()

    def _sniff(self):
        scapy.sniff(iface=self.interface, prn=self.packet_callback, store=False, stop_filter=self.stop_filter)

    def stop_filter(self, packet):
        return not self.sniffing  # Stop sniffing if sniffing is set to False

    def stop_sniffing(self):
        print("Stopping network monitoring...")
        self.sniffing = False  # Set the flag to False to stop sniffing

# # Example usage:
# monitor = NetworkMonitor("Intel(R) Wi-Fi 6E AX211 160MHz")
# monitor.start_sniffing()
# # ... some time later ...
# time.sleep(5)
# monitor.stop_sniffing()