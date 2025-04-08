import scapy.all as scapy
from datetime import datetime

#Function to log packets
def packet_callback(packet):
    #TimeStamp of packet creation
    time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #Write packet information to file
    dir="C:\\Users\\KIIT0001\\Documents\\MCA Project\\IDS\\HIds\\Core\\network_traffic.txt"
    with open(dir,"a") as log_file:
        log_file.write(f"{time} - {packet.summary()}\n")

#Start monitoring network traffic
def start_sniffing(interface):
    print(f"Starting network monitoring on {interface}...")
    scapy.sniff(iface=interface, prn=packet_callback , store=False)

#Execute main function
if __name__ == "__main__":
    #Specify the network interface (e.g. eth0 or wlan0)
    interface = input("Enter interface: ")
    #interfaces=scapy.get_if_list()
    #print(interfaces)
    start_sniffing(interface)
    #scapy.show_interfaces()