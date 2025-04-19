# Host-Based Intrusion Detection System (HIDS) for Windows

## Project Overview

### **Introduction**

In today’s rapidly evolving cybersecurity landscape, organizations must proactively defend against unauthorized access and malicious activities. This project aims to develop a **Host-Based Intrusion Detection System (HIDS) for Windows**, designed to detect, log, and respond to suspicious activities on a Windows machine. By continuously monitoring system processes, file changes, network activity, and registry modifications, our HIDS provides an extra layer of security against potential threats.

---

### **Objectives**

- **Real-time Monitoring**: Continuously track system events such as process execution, file modifications, and network connections.
- **Anomaly Detection**: Identify suspicious patterns based on predefined rules and behavioral analysis.
- **Logging & Alerts**: Maintain comprehensive logs of detected threats and send alerts when potential attacks occur.
- **User-friendly Configuration**: Allow users to define security rules and customize monitoring preferences.
- **Lightweight & Efficient**: Ensure minimal system overhead while providing robust security.

---

### **Key Features**

#### **1. Process Monitoring**

- Tracks all running processes.
- Detects unauthorized or suspicious process execution.
- Identifies parent-child relationships between processes.

#### **2. File Integrity Monitoring (FIM)**

- Detects changes to critical system files.
- Monitors unauthorized file creation, deletion, and modification.
- Logs hash changes of monitored files.

#### **3. Registry Monitoring**

- Tracks modifications to sensitive Windows registry keys.
- Alerts on unauthorized changes that could indicate malware activity.

#### **4. Network Activity Monitoring**

- Captures active network connections.
- Identifies suspicious outbound/inbound traffic.
- Detects unauthorized communication attempts.

#### **5. Anomaly Detection & Alerting**

- Uses rule-based detection and machine learning (future enhancement).
- Sends alerts via logs, email, or notifications.

---

### **Technology Stack**

- **Programming Language**: Python
- **Monitoring Tools**: Windows APIs, `psutil`, `pyinotify`, `scapy`
- **Logging & Storage**: SQLite / JSON / Syslog
- **Alerting**: Email notifications / Webhooks

---

### **Screenshots**

Here are some screenshots of the HIDS in action:

1. **Main Dashboard**  
   <img src="HIds/utils/Main%20Dashbord.png" alt="Main Dashboar" width="500" height="300">
   *Description: This screenshot shows the main dashboard of the HIDS, displaying real-time monitoring statistics.*

3. **File Integrity Monitoring**  
      <img src="HIds/utils/Ids%20Alert%20popup.png" alt="File Integrity Monitoring" width="500" height="300">
   *Description: This screenshot illustrates the file integrity monitoring feature, highlighting recent changes to critical files.*

5. **Process Activity Monitoring**  
      <img src="HIds/utils/Process%20Monitoring.png" alt="Network Activity Monitoring" width="500" height="300">
   *Description: This screenshot captures the Process activity monitoring interface, showing active connections and alerts for suspicious traffic.*


### **Project Structure**

```bash
Windows-HIDS/
│── hids/                    # Main package
│   │── core/                # Core functionality
│   │   │── process_monitor.py
│   │   │── file_monitor.py
│   │   │── registry_monitor.py
│   │   │── network_monitor.py
│   │── utils/               # Helper utilities
│   │   │── logger.py
│   │   │── config.py
|   |   │── Gui.py
│   │── detection_engine.py  # Analyzes threats
│   │── alert_manager.py     # Handles alerts
│   │── main.py              # Entry point
│── tests/                   # Unit tests
│── docs/                    # Documentation
│── scripts/   
│── Main.py              # Helper scripts
│── requirements.txt         # Dependencies
│── README.md                # Project overview
```

---

### **Collaboration & Version Control**

- **GitHub Repository**: Centralized codebase for team collaboration.
- **Branching Strategy**: Feature branches for development, merged via pull requests.
- **Code Reviews**: Ensuring quality and security of the code.

```bash
git clone https://github.com/sangram73/IDS.git
git branch spbranch
git checkout 
git commit -m "Implemented feature"
git push origin main
```

---

### **Future Enhancements**

✅ Integration with **Machine Learning** for anomaly detection.  
✅ GUI-based **Dashboard** for visualization.  
✅ Support for **Cloud Logging & Analysis**.

---

### **Conclusion**

This project serves as a foundation for a robust and scalable **Windows-based HIDS**. By combining efficient monitoring techniques with real-time analysis, it provides an **essential security tool** for detecting and preventing cyber threats. Our long-term goal is to evolve this project into a fully autonomous **Intrusion Prevention System (IPS)**.

---

## **Contributors**

🚀 **Sangram Panda** & **Satya Prakash Swain**  
🔗 **GitHub**: #  
✉️ **Contact**:

Let's build a **secure future** together! 🔒🚀
