#!/usr/bin/env python3
import os
import sys
import datetime
import platform
import subprocess
import socket
import random
import hashlib
import base64
from threading import Thread
import time
import json
import requests
from cryptography.fernet import Fernet
import netifaces
import scapy.all as scapy

class AdvancedKaliTerminal:
    def __init__(self):
        self.current_dir = os.getcwd()
        self.user = "officialrootman"
        self.hostname = "kali"
        self.running = True
        self.current_time = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
        
        self.commands = {
            'help': self.help,
            'exit': self.exit,
            'clear': self.clear,
            'pwd': self.pwd,
            'whoami': self.whoami,
            'ifconfig': self.ifconfig,
            'nmap': self.nmap_scan,
            'hash': self.hash_string,
            'scan': self.security_scan,
            'ls': self.list_files,
            'cd': self.change_directory,
            'mkdir': self.make_directory,
            'rm': self.remove,
            'cat': self.cat_file,
            'encrypt': self.encrypt_file,
            'decrypt': self.decrypt_file,
            'portscan': self.port_scanner,
            'netdiscover': self.network_discovery,
            'sysinfo': self.system_info,
            'brutefore': self.brute_force_simulation,
            'vulnscan': self.vulnerability_scan,
            'dos': self.dos_simulation,
            'backdoor': self.backdoor_simulation,
            'stealth': self.stealth_scan,
            'firewall': self.firewall_check,
            'exploit': self.exploit_simulation
        }

    def prompt(self):
        return f"\033[91m{self.user}@{self.hostname}\033[0m:\033[94m{self.current_dir}\033[0m$ "

    # Dosya Sistemi İşlemleri
    def list_files(self, *args):
        try:
            path = args[0] if args else '.'
            files = os.listdir(path)
            for f in files:
                if os.path.isdir(os.path.join(path, f)):
                    print(f"\033[94m{f}/\033[0m")
                else:
                    print(f)
        except Exception as e:
            print(f"Hata: {str(e)}")

    def change_directory(self, *args):
        if not args:
            print("Kullanım: cd <dizin>")
            return
        try:
            os.chdir(args[0])
            self.current_dir = os.getcwd()
        except Exception as e:
            print(f"Hata: {str(e)}")

    def make_directory(self, *args):
        if not args:
            print("Kullanım: mkdir <dizin_adı>")
            return
        try:
            os.makedirs(args[0])
            print(f"Dizin oluşturuldu: {args[0]}")
        except Exception as e:
            print(f"Hata: {str(e)}")

    def remove(self, *args):
        if not args:
            print("Kullanım: rm <dosya/dizin>")
            return
        try:
            if os.path.isdir(args[0]):
                os.rmdir(args[0])
            else:
                os.remove(args[0])
            print(f"Silindi: {args[0]}")
        except Exception as e:
            print(f"Hata: {str(e)}")

    def cat_file(self, *args):
        if not args:
            print("Kullanım: cat <dosya>")
            return
        try:
            with open(args[0], 'r') as f:
                print(f.read())
        except Exception as e:
            print(f"Hata: {str(e)}")

    # Şifreleme İşlemleri
    def encrypt_file(self, *args):
        if len(args) != 2:
            print("Kullanım: encrypt <kaynak_dosya> <hedef_dosya>")
            return
        try:
            with open(args[0], 'rb') as f:
                data = f.read()
            encrypted_data = self.cipher_suite.encrypt(data)
            with open(args[1], 'wb') as f:
                f.write(encrypted_data)
            print(f"Dosya şifrelendi: {args[1]}")
        except Exception as e:
            print(f"Hata: {str(e)}")

    def decrypt_file(self, *args):
        if len(args) != 2:
            print("Kullanım: decrypt <şifreli_dosya> <hedef_dosya>")
            return
        try:
            with open(args[0], 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = self.cipher_suite.decrypt(encrypted_data)
            with open(args[1], 'wb') as f:
                f.write(decrypted_data)
            print(f"Dosya şifresi çözüldü: {args[1]}")
        except Exception as e:
            print(f"Hata: {str(e)}")

    # Ağ Tarama ve Güvenlik
    def port_scanner(self, *args):
        if not args:
            print("Kullanım: portscan <hedef_ip>")
            return
        target = args[0]
        print(f"Port taraması başlatılıyor: {target}")
        for port in range(20, 1025):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            if result == 0:
                print(f"Port {port}: Açık")
            sock.close()

    def network_discovery(self, *args):
        print("Ağ keşfi başlatılıyor...")
        for interface in netifaces.interfaces():
            print(f"\nArayüz: {interface}")
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addrs:
                for addr in addrs[netifaces.AF_INET]:
                    print(f"IP Adresi: {addr['addr']}")

    def vulnerability_scan(self, *args):
        if not args:
            print("Kullanım: vulnscan <hedef>")
            return
        target = args[0]
        vulnerabilities = [
            "SQL Injection",
            "Cross-Site Scripting (XSS)",
            "Remote Code Execution",
            "Buffer Overflow",
            "Command Injection"
        ]
        print(f"\nZafiyet taraması başlatılıyor: {target}")
        for vuln in vulnerabilities:
            print(f"\n[*] {vuln} kontrolü yapılıyor...")
            time.sleep(1)
            risk = random.choice(['Yüksek', 'Orta', 'Düşük', 'Temiz'])
            print(f"Risk Seviyesi: {risk}")

    def stealth_scan(self, *args):
        if not args:
            print("Kullanım: stealth <hedef_ip>")
            return
        print(f"Gizli tarama başlatılıyor: {args[0]}")
        print("TCP SYN taraması kullanılıyor...")
        time.sleep(2)
        ports = [21, 22, 23, 25, 53, 80, 443, 3306, 5432]
        for port in ports:
            print(f"Port {port} kontrol ediliyor...")
            time.sleep(0.5)
            status = random.choice(['Filtrelenmiş', 'Açık', 'Kapalı'])
            print(f"Durum: {status}")

    def firewall_check(self, *args):
        if not args:
            print("Kullanım: firewall <hedef_ip>")
            return
        print(f"Firewall analizi başlatılıyor: {args[0]}")
        rules = [
            "INPUT DROP",
            "OUTPUT ACCEPT",
            "FORWARD DROP",
            "TCP/80 ALLOW",
            "TCP/443 ALLOW"
        ]
        for rule in rules:
            print(f"Kural kontrol ediliyor: {rule}")
            time.sleep(1)
            status = random.choice(['Aktif', 'Devre Dışı'])
            print(f"Durum: {status}")

    def exploit_simulation(self, *args):
        if not args:
            print("Kullanım: exploit <hedef> <zafiyet_tipi>")
            return
        exploit_types = {
            "buffer": "Buffer Overflow Exploit",
            "sql": "SQL Injection Exploit",
            "rce": "Remote Code Execution",
            "csrf": "Cross-Site Request Forgery"
        }
        print("\nExploit geliştirme simülasyonu başlatılıyor...")
        print(f"Hedef: {args[0]}")
        if len(args) > 1 and args[1] in exploit_types:
            print(f"Zafiyet tipi: {exploit_types[args[1]]}")
        
        stages = [
            "Keşif yapılıyor...",
            "Zafiyet analizi yapılıyor...",
            "Payload hazırlanıyor...",
            "Exploit test ediliyor...",
            "Sonuçlar raporlanıyor..."
        ]
        
        for stage in stages:
            print(f"\n[*] {stage}")
            time.sleep(1)
            success = random.choice([True, False])
            if success:
                print("Başarılı!")
            else:
                print("Başarısız - Yeni yöntem deneniyor...")

    def system_info(self, *args):
        print("\n=== Sistem Bilgileri ===")
        print(f"İşletim Sistemi: {platform.system()}")
        print(f"Sürüm: {platform.version()}")
        print(f"Makine: {platform.machine()}")
        print(f"İşlemci: {platform.processor()}")
        print(f"Hostname: {socket.gethostname()}")
        print(f"IP Adresi: {socket.gethostbyname(socket.gethostname())}")
        print(f"Python Sürümü: {sys.version}")

    def brute_force_simulation(self, *args):
        if len(args) < 2:
            print("Kullanım: bruteforce <hedef> <servis>")
            return
        
        target = args[0]
        service = args[1]
        
        print(f"\nBrute force saldırısı simülasyonu başlatılıyor...")
        print(f"Hedef: {target}")
        print(f"Servis: {service}")
        
        passwords = ["123456", "password", "admin", "root", "letmein"]
        total = len(passwords)
        
        for i, pwd in enumerate(passwords, 1):
            print(f"\rDenenen şifre: {pwd} ({i}/{total})", end="")
            time.sleep(0.5)
            if random.random() < 0.2:  # %20 başarı şansı
                print(f"\nBaşarılı! Şifre bulundu: {pwd}")
                return
        print("\nBrute force başarısız - şifre bulunamadı.")

    def dos_simulation(self, *args):
        if not args:
            print("Kullanım: dos <hedef_ip> [port]")
            return
        
        target = args[0]
        port = int(args[1]) if len(args) > 1 else 80
        
        print(f"\nDoS saldırısı simülasyonu başlatılıyor...")
        print(f"Hedef: {target}:{port}")
        
        packets = 1000
        for i in range(packets):
            progress = (i + 1) / packets * 100
            print(f"\rİlerleme: {progress:.1f}% ({i+1}/{packets} paket)", end="")
            time.sleep(0.01)
        print("\nDoS simülasyonu tamamlandı.")

    def backdoor_simulation(self, *args):
        if not args:
            print("Kullanım: backdoor <hedef_ip>")
            return
        
        print(f"\nBackdoor oluşturma simülasyonu...")
        stages = [
            "Hedef sistem analiz ediliyor...",
            "Güvenlik açıkları tespit ediliyor...",
            "Payload hazırlanıyor...",
            "Bağlantı kuruluyor...",
            "Persistent bağlantı oluşturuluyor..."
        ]
        
        for stage in stages:
            print(f"[*] {stage}")
            time.sleep(1)
            if random.random() < 0.1:  # %10 başarısızlık şansı
                print("Hata: Bağlantı başarısız!")
                return
        print("Backdoor başarıyla oluşturuldu!")

    def run(self):
        self.clear()
        print("\033[92m" + """
╔══════════════════════════════════════════════════════╗
║              Advanced Kali Linux Terminal            ║
║            Geliştirici: officialrootman             ║
║               Gelişmiş Terminal v2.0                ║
║                                                     ║
║  Yeni Özellikler:                                  ║
║  - Dosya Sistemi İşlemleri                         ║
║  - Ağ Tarama Araçları                              ║
║  - Şifreleme/Şifre Çözme                           ║
║  - Güvenlik Testleri                               ║
║  - Exploit Geliştirme Simülasyonu                  ║
╚══════════════════════════════════════════════════════╝
        """ + "\033[0m")
        
        while self.running:
            try:
                command = input(self.prompt())
                if command.strip():
                    self.execute_command(command)
            except KeyboardInterrupt:
                print("\nÇıkış için 'exit' yazın.")
            except Exception as e:
                print(f"Hata: {str(e)}")

if __name__ == "__main__":
    terminal = AdvancedKaliTerminal()
    terminal.run()