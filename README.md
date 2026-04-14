# 🕸️ Arachne: A Ransomware Defense Simulator

### Overview
Arachne ek Python-based cybersecurity tool hai jo **Honey-file (Tripwire)** technique ka use karke ransomware attacks ko detect aur block karta hai. Ye system real-time mein sensitive directories ko monitor karta hai aur kisi bhi unauthorized modification par malicious process ko turant kill kar deta hai.

---

### 🛡️ How it Works (Logic)
Arachne "Honey-files" ka ek trap bichata hai. In files ko normal user touch nahi karta, lekin ransomware (jo saara data encrypt karne ki koshish karta hai) inhe modify zaroor karega.
1. **Monitoring:** `watchdog` library ka use karke folder par nazar rakhi jati hai.
2. **Detection:** Jaise hi koi honey-file rename ya modify hoti hai, alarm trigger ho jata hai.
3. **Identification:** `psutil` ke zariye us PID (Process ID) ka pata lagaya jata hai jo ye change kar raha hai.
4. **Neutralization:** Agar wo process 'Safe List' mein nahi hai, toh use system-level par **Kill** kar diya jata hai.



---

### 🚀 Installation
1. Repository ko clone karein:
   ```bash
   git clone [https://github.com/Krishang-Gulati/Arachne-Ransomware-Simulator.git](https://github.com/Krishang-Gulati/Arachne-Ransomware-Simulator.git)