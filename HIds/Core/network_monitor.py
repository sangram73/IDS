import scapy.all as scapy
from scapy.all import sniff
from datetime import datetime
import pandas


#Function to log packets
def packet_callback(packet):
    #TimeStamp of packet creation
    time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #Write packet information to file
    with open(r"HIds\logs\network_traffic.log","a") as log_file:
        log_file.write(f"{time} - {packet.summary()}\n")
        if packet.haslayer('IP'):
            src_ip=packet['IP'].src
            dst_ip=packet['IP'].dst
            print(f"Packet detected from {src_ip} to {dst_ip}")
            with open(r"HIds\logs\blacklisted_IP.csv","r") as IP_file:
                datareader=pandas.read_csv(IP_file)
                for IP in datareader:
                    # print(IP) #testing
                    if(src_ip==IP):
                        print("Warning!!!Request sent from Blacklisted IP!")
        
   

#Start monitoring network traffic
def start_sniffing(interface):
    print(f"Starting network monitoring on {interface}...")
    scapy.sniff(iface=interface, prn=packet_callback , store=False)

#Execute main function
if __name__ == "__main__":
    #Specify the network interface (e.g. eth0 or wlan0)

    scapy.show_interfaces()
    interface = input("Enter interface")

    start_sniffing(interface)
