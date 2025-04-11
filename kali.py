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
import json
import threading
import time
import psutil
import colorama
from colorama import Fore, Back, Style
from cryptography.fernet import Fernet

class AdvancedTerminal:
    def __init__(self):
        colorama.init(autoreset=True)
        self.current_dir = os.getcwd()
        self.user = "officialrootman"
        self.hostname = socket.gethostname()
        self.running = True
        self.history = []
        self.env_vars = {}
        self.session_id = hashlib.md5(str(time.time()).encode()).hexdigest()
        self.init_encryption()
        self.banner_shown = False
        
        # Komut sözlüğü
        self.commands = {
            'help': self.help,
            'exit': self.exit,
            'clear': self.clear,
            'pwd': self.pwd,
            'cd': self.cd,
            'ls': self.ls,
            'dir': self.ls,
            'cat': self.cat,
            'echo': self.echo,
            'mkdir': self.mkdir,
            'rm': self.rm,
            'cp': self.cp,
            'mv': self.mv,
            'history': self.show_history,
            'date': self.show_date,
            'whoami': self.whoami,
            'sysinfo': self.system_info,
            'ps': self.process_list,
            'kill': self.kill_process,
            'ping': self.ping,
            'ipconfig': self.ipconfig,
            'encrypt': self.encrypt_file,
            'decrypt': self.decrypt_file,
            'hash': self.hash_file,
            'search': self.search_files,
            'tree': self.show_tree,
            'monitor': self.system_monitor,
            'calc': self.calculator,
            'env': self.show_env,
            'setenv': self.set_env,
            'banner': self.show_banner
        }

    def init_encryption(self):
        """Şifreleme anahtarını başlatır"""
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    def prompt(self):
        """Terminal görünümünü oluşturur"""
        time_str = datetime.datetime.now().strftime("%H:%M:%S")
        return f"{Fore.CYAN}{self.user}@{self.hostname} {Fore.YELLOW}[{time_str}] {Fore.GREEN}{self.current_dir}{Fore.WHITE}\n$ "

    def execute_command(self, command):
        """Komutu çalıştırır"""
        if not command.strip():
            return

        self.history.append(command)
        parts = command.split()
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd in self.commands:
            try:
                self.commands[cmd](*args)
            except Exception as e:
                print(f"{Fore.RED}Hata: {str(e)}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Hata: '{cmd}' komutu bulunamadı.{Style.RESET_ALL}")

    # Temel Komutlar
    def help(self, *args):
        """Yardım menüsünü gösterir"""
        print(f"{Fore.YELLOW}Kullanılabilir Komutlar:{Style.RESET_ALL}")
        commands_help = {
            'help': 'Bu yardım menüsünü gösterir',
            'exit': 'Terminalden çıkar',
            'clear': 'Ekranı temizler',
            'pwd': 'Mevcut çalışma dizinini gösterir',
            'cd': 'Dizin değiştirir',
            'ls/dir': 'Dizin içeriğini listeler',
            'cat': 'Dosya içeriğini gösterir',
            'echo': 'Metin yazdırır',
            'mkdir': 'Yeni dizin oluşturur',
            'rm': 'Dosya veya dizin siler',
            'cp': 'Dosya kopyalar',
            'mv': 'Dosya taşır',
            'history': 'Komut geçmişini gösterir',
            'date': 'Tarih ve saati gösterir',
            'whoami': 'Mevcut kullanıcıyı gösterir',
            'sysinfo': 'Sistem bilgilerini gösterir',
            'ps': 'Çalışan işlemleri listeler',
            'kill': 'İşlem sonlandırır',
            'ping': 'Ağ bağlantısını test eder',
            'ipconfig': 'Ağ yapılandırmasını gösterir',
            'encrypt': 'Dosya şifreler',
            'decrypt': 'Şifrelenmiş dosyayı çözer',
            'hash': 'Dosya hash değerini hesaplar',
            'search': 'Dosya arar',
            'tree': 'Dizin ağacını gösterir',
            'monitor': 'Sistem kaynaklarını izler',
            'calc': 'Hesap makinesi',
            'env': 'Ortam değişkenlerini gösterir',
            'setenv': 'Ortam değişkeni ayarlar',
            'banner': 'Terminal başlığını gösterir'
        }
        
        for cmd, desc in commands_help.items():
            print(f"{Fore.GREEN}{cmd:12}{Fore.WHITE} - {desc}")

    def exit(self, *args):
        """Terminalden çıkar"""
        print(f"{Fore.YELLOW}Oturum sonlandırılıyor... Güle güle!{Style.RESET_ALL}")
        self.running = False

    def clear(self, *args):
        """Ekranı temizler"""
        os.system('cls' if platform.system() == 'Windows' else 'clear')

    def pwd(self, *args):
        """Mevcut dizini gösterir"""
        print(self.current_dir)

    def cd(self, *args):
        """Dizin değiştirir"""
        if not args:
            self.current_dir = os.path.expanduser("~")
        else:
            try:
                new_dir = os.path.abspath(os.path.join(self.current_dir, args[0]))
                if os.path.exists(new_dir) and os.path.isdir(new_dir):
                    os.chdir(new_dir)
                    self.current_dir = new_dir
                else:
                    print(f"{Fore.RED}Hata: Dizin bulunamadı: {args[0]}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Hata: {str(e)}{Style.RESET_ALL}")

    def ls(self, *args):
        """Dizin içeriğini listeler"""
        try:
            path = args[0] if args else '.'
            items = os.listdir(path)
            for item in items:
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    print(f"{Fore.BLUE}{item}/{Style.RESET_ALL}")
                else:
                    print(item)
        except Exception as e:
            print(f"{Fore.RED}Hata: {str(e)}{Style.RESET_ALL}")

    # Dosya İşlemleri
    def cat(self, *args):
        """Dosya içeriğini gösterir"""
        if not args:
            print(f"{Fore.RED}Hata: Dosya adı gerekli{Style.RESET_ALL}")
            return
        try:
            with open(args[0], 'r') as f:
                print(f.read())
        except Exception as e:
            print(f"{Fore.RED}Hata: {str(e)}{Style.RESET_ALL}")

    def echo(self, *args):
        """Metin yazdırır"""
        print(' '.join(args))

    def mkdir(self, *args):
        """Yeni dizin oluşturur"""
        if not args:
            print(f"{Fore.RED}Hata: Dizin adı gerekli{Style.RESET_ALL}")
            return
        try:
            os.makedirs(args[0])
            print(f"Dizin oluşturuldu: {args[0]}")
        except Exception as e:
            print(f"{Fore.RED}Hata: {str(e)}{Style.RESET_ALL}")

    # Sistem Bilgileri
    def system_info(self, *args):
        """Sistem bilgilerini gösterir"""
        print(f"{Fore.YELLOW}=== Sistem Bilgileri ==={Style.RESET_ALL}")
        print(f"İşletim Sistemi: {platform.system()} {platform.release()}")
        print(f"Makine: {platform.machine()}")
        print(f"İşlemci: {platform.processor()}")
        print(f"Python Sürümü: {sys.version.split()[0]}")
        print(f"Hostname: {socket.gethostname()}")
        print(f"IP Adresi: {socket.gethostbyname(socket.gethostname())}")

    def process_list(self, *args):
        """Çalışan işlemleri listeler"""
        print(f"{Fore.YELLOW}Çalışan İşlemler:{Style.RESET_ALL}")
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                info = proc.info
                print(f"PID: {info['pid']:5} CPU: {info['cpu_percent']:5.1f}% MEM: {info['memory_percent']:5.1f}% NAME: {info['name']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    def system_monitor(self, *args):
        """Sistem kaynaklarını izler"""
        try:
            while True:
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                
                print(f"\r{Fore.CYAN}CPU: {cpu_percent:5.1f}% | "
                      f"RAM: {memory.percent:5.1f}% | "
                      f"Disk: {disk.percent:5.1f}%{Style.RESET_ALL}", end='')
                
                if msvcrt.kbhit():  # Windows için
                    if msvcrt.getch() == b'\x1b':  # ESC tuşu
                        break
        except KeyboardInterrupt:
            print("\nİzleme sonlandırıldı.")

    def calculator(self, *args):
        """Basit hesap makinesi"""
        if len(args) < 3:
            print(f"{Fore.RED}Kullanım: calc <sayı1> <işlem> <sayı2>{Style.RESET_ALL}")
            return
        
        try:
            num1 = float(args[0])
            operator = args[1]
            num2 = float(args[2])
            
            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                result = num1 / num2
            else:
                print(f"{Fore.RED}Geçersiz işlem{Style.RESET_ALL}")
                return
            
            print(f"{Fore.GREEN}Sonuç: {result}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Hata: {str(e)}{Style.RESET_ALL}")

    def show_banner(self, *args):
        """Terminal başlığını gösterir"""
        banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════╗
║             Advanced Python Terminal v1.0              ║
║          Geliştirici: officialrootman                ║
║     Oturum ID: {self.session_id[:8]}                         ║
║     Tarih: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}           ║
╚══════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
        print(banner)

    def run(self):
        """Terminal döngüsünü başlatır"""
        self.clear()
        if not self.banner_shown:
            self.show_banner()
            self.banner_shown = True
        
        while self.running:
            try:
                command = input(self.prompt())
                self.execute_command(command)
            except KeyboardInterrupt:
                print("\nÇıkış için 'exit' yazın.")
            except Exception as e:
                print(f"{Fore.RED}Hata: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    terminal = AdvancedTerminal()
    terminal.run()