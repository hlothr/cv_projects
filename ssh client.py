import subprocess
import paramiko
import os
import ipaddress
import pyperclip
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed


class SSHConnectionManager:
    def __init__(self):
        self.lock = threading.Lock()  # Initialize a lock for thread safety
        self.VAR_EXIST = None
        self.FILE_LOCATION = os.getcwd()
        self.SSH_ADDRESSES_FILE = os.path.join(self.FILE_LOCATION, "all_ssh_addrs.txt")
        self.FILEZILLA_PATH_FILE = os.path.join(self.FILE_LOCATION, "filezilla.txt")
        self.USERNAMES_FILE = os.path.join(self.FILE_LOCATION, "username.txt")
        self.SUCCESSFUL_CONNECTIONS_FILE = os.path.join(self.FILE_LOCATION, "successful_connections.txt")
        self.ip_list = []

    def get_local_ips(self):
        proc = subprocess.run(['powershell', '-Command', 'Get-NetIPAddress -InterfaceAlias * | Select-Object IpAddress'],
                              capture_output=True, text=True)
        local_ips = [line.strip() for line in proc.stdout.splitlines() if ':' in line]
        return local_ips

    def scan_network(self):
        proc = subprocess.run(['powershell', '-Command', 'arp -a'], capture_output=True, text=True)
        output = proc.stdout

        # Splitting the output by double newline to separate interfaces
        interface_lines = output.split('\n')

        # Check if there are at least 2 interface blocks
        if len(interface_lines) < 2:
            messagebox.showerror("Error", "Second interface not found in ARP output.")
            return output

        # Extracting the second interface block
        lines = interface_lines
        self.ip_list = []
        # Iterate through lines to find the interface line with the desired IP prefix
        for line in lines:
            if line.startswith('Interface'):
                edit = line.split(" ")
                edit = edit[1]
                edit = '.'.join(edit.split('.')[:3])
                self.ip_list.append(edit)
                self.VAR_EXIST = True

        # If IP_PREFIX is not set, show an error
        if len(interface_lines) == 0:
            messagebox.showerror("Error", "No suitable interface")

        return output

    def creating_list(self, network_scan_output):
        interface_lines = network_scan_output.split('\n')

        # Check if there are at least 2 interface blocks
        if len(interface_lines) < 2:
            messagebox.showerror("Error", "Second interface not found in ARP output.")

        # Extracting the second interface block
        lines = interface_lines
        ip_list = []
        # Iterate through lines to find the interface line with the desired IP prefix
        for line in lines:
            if line.startswith('Interface'):
                edit = line.split(" ")
                edit = edit[1]
                edit = '.'.join(edit.split('.')[:3])
                ip_list.append(edit)
                self.VAR_EXIST = True

        # If IP_PREFIX is not set, show an error
        if len(interface_lines) == 0:
            messagebox.showerror("Error", "No suitable interface")

        return ip_list

    def check_ip(self, ip, usernames):
        for username in usernames:
            try:
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(str(ip), username=username, timeout=1)
                print(f"The {ip} is a server, connecting with username {username}...")
                ssh_client.close()
                # Log successful connection if it's unique
                if not self.is_ip_username_logged(ip, username):
                    with self.lock:
                        with open(self.SUCCESSFUL_CONNECTIONS_FILE, 'a') as f:
                            f.write(f"{ip},{username}\n")
                return ip
            except paramiko.AuthenticationException:
                print(f"Failed to authenticate with {ip} using username {username}.")
            except paramiko.SSHException as e:
                print(f"An error occurred while connecting to {ip}: {e}")
            except Exception as e:
                print(f"Unexpected error with IP address {ip}: {e}")
        return None

    def is_ip_username_logged(self, ip, username):
        with self.lock:
            if os.path.exists(self.SUCCESSFUL_CONNECTIONS_FILE):
                with open(self.SUCCESSFUL_CONNECTIONS_FILE, 'r') as f:
                    for line in f:
                        logged_ip, logged_username = line.strip().split(',')
                        if logged_ip == ip and logged_username == username:
                            return True
        return False

    def find_servers(self):
        def task():
            if os.path.exists(self.SSH_ADDRESSES_FILE):
                os.remove(self.SSH_ADDRESSES_FILE)
            self.find_ip()

        thread = threading.Thread(target=task)
        thread.start()

    def add_username(self):
        username = simpledialog.askstring("Input", "Enter username:")
        if username:
            with open(self.USERNAMES_FILE, 'a') as uf:
                uf.write(username + '\n')
            messagebox.showinfo("Info", "Username added.")

    def connect_ssh(self):
        if not os.path.exists(self.SSH_ADDRESSES_FILE):
            messagebox.showerror("Error", "Please search for servers first.")
            return

        with open(self.SSH_ADDRESSES_FILE, 'r') as f:
            addresses = [line.strip() for line in f if line.strip()]

        if not addresses:
            messagebox.showerror("Error", "No servers found.")
            return

        def on_connect():
            selected_ip = ip_listbox.get(tk.ACTIVE)
            port = port_entry.get()
            username = username_entry.get()

            if not selected_ip:
                messagebox.showerror("Error", "No IP address selected.")
            elif not port:
                messagebox.showerror("Error", "No port specified.")
            elif not username:
                messagebox.showerror("Error", "No username specified.")
            else:
                def ssh_task():
                    try:
                        with open(self.FILEZILLA_PATH_FILE, 'r') as f:
                            filezilla_path = f.readline().strip()
                        os.startfile(filezilla_path)
                    except Exception as e:
                        messagebox.showerror("Error", str(e))
                    pyperclip.copy(selected_ip)
                    os.system(f"start /wait cmd /k ssh {username}@{selected_ip} -p {port}")

                ssh_thread = threading.Thread(target=ssh_task)
                ssh_thread.start()

        def on_ip_select(event):
            selected_ip = ip_listbox.get(tk.ACTIVE)
            username_entry.delete(0, tk.END)  # Clear the entry
            # Autofill the username based on the log file
            with self.lock:
                if os.path.exists(self.SUCCESSFUL_CONNECTIONS_FILE):
                    with open(self.SUCCESSFUL_CONNECTIONS_FILE, 'r') as f:
                        for line in f:
                            ip, user = line.strip().split(',')
                            if ip == selected_ip:
                                username_entry.insert(0, user)
                                break

        connect_window = tk.Toplevel()
        connect_window.title("Connect via SSH")
        connect_window.columnconfigure(0, weight=1)
        connect_window.rowconfigure(1, weight=1)

        tk.Label(connect_window, text="Available IPs:").grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        ip_listbox = tk.Listbox(connect_window)
        ip_listbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        for addr in addresses:
            ip_listbox.insert(tk.END, addr)
        ip_listbox.bind('<<ListboxSelect>>', on_ip_select)  # Bind the selection event

        tk.Label(connect_window, text="Port:").grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        port_entry = tk.Entry(connect_window)
        port_entry.grid(row=3, column=0, sticky="ew", padx=10, pady=10)

        port_entry.insert(0, "22")  # Prepopulate with "22"

        tk.Label(connect_window, text="Username:").grid(row=4, column=0, sticky="ew", padx=10, pady=10)
        username_entry = tk.Entry(connect_window)
        username_entry.grid(row=5, column=0, sticky="ew", padx=10, pady=10)

        tk.Button(connect_window, text="Connect", command=on_connect).grid(row=6, column=0, sticky="ew", padx=10, pady=10)

    def save_filezilla_path(self):
        filezilla_path = filedialog.askopenfilename(title="Select FileZilla executable", filetypes=[("Executable files", "*.exe")])
        if filezilla_path:
            with open(self.FILEZILLA_PATH_FILE, 'w') as f:
                f.write(filezilla_path)
            messagebox.showinfo("Info", "FileZilla path saved.")

    def find_ip(self):
        if not self.VAR_EXIST:
            messagebox.showerror("Error", "IP prefix not determined. Please run 'Additional Network Info' first.")
            return

        mask_list = []
        for i in self.creating_list(self.scan_network()):
            ip_list = ipaddress.ip_network(f'{i}.0/24')

            mask_list.append(ip_list)
        if not os.path.exists(self.USERNAMES_FILE):
            messagebox.showerror("Error", "Please add at least one username first.")
            return

        with open(self.USERNAMES_FILE, 'r') as uf:
            usernames = [line.strip() for line in uf if line.strip()]

        if not usernames:
            messagebox.showerror("Error", "No usernames found.")
            return
        valid_ips = []
        for unique_ip_range in mask_list:
            with ThreadPoolExecutor(max_workers=255) as executor:
                future_to_ip = {executor.submit(self.check_ip, ip, usernames): ip for ip in unique_ip_range}
                for future in as_completed(future_to_ip):
                    ip = future_to_ip[future]
                    result = future.result()
                    if result:
                        valid_ips.append(result)
        if valid_ips:
            with self.lock:
                with open(self.SSH_ADDRESSES_FILE, 'a') as f:
                    for ip in valid_ips:
                        f.write(str(ip) + '\n')

        if not valid_ips:
            messagebox.showinfo("Info", "No servers found.")
        else:
            messagebox.showinfo("Info", "Server search complete.")

    def main(self):
        root = tk.Tk()
        root.title("SSH Connection Manager")

        # Lock window dimensions
        root.resizable(False, False)

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        frame = tk.Frame(root)
        frame.grid(row=0, column=0, sticky="nsew")

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        tk.Button(frame, text="Additional Network Info", command=self.scan_network).grid(row=0, column=0, sticky="ew", padx=10,
                                                                                        pady=10)
        tk.Button(frame, text="Find Servers", command=self.find_servers).grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        tk.Button(frame, text="Add Username", command=self.add_username).grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        tk.Button(frame, text="Connect via SSH", command=self.connect_ssh).grid(row=3, column=0, sticky="ew", padx=10, pady=10)
        tk.Button(frame, text="Save FileZilla Path", command=self.save_filezilla_path).grid(row=4, column=0, sticky="ew",
                                                                                           padx=10, pady=10)

        root.mainloop()


if __name__ == "__main__":
    ssh_manager = SSHConnectionManager()
    ssh_manager.main()
