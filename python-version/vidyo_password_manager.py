import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
import asyncio
import threading
from datetime import datetime
import base64

class VidyoPasswordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Vidyo Password Manager")
        self.root.geometry("700x600")
        
        self.month_usernames = [
            "jan", "feb", "mar", "apr", "may", "jun",
            "jul", "aug", "sep", "oct", "nov", "dec"
        ]
        
        self.setup_ui()
        
    def setup_ui(self):
        # Portal Configuration Frame
        portal_frame = ttk.LabelFrame(self.root, text="Portal Configuration", padding="10")
        portal_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        
        ttk.Label(portal_frame, text="Portal URL:").grid(row=0, column=0, sticky="w", padx=5)
        self.portal_url = ttk.Entry(portal_frame, width=40)
        self.portal_url.grid(row=0, column=1, padx=5)
        self.portal_url.insert(0, "http://your-vidyo-portal.com")
        
        ttk.Label(portal_frame, text="Admin User:").grid(row=1, column=0, sticky="w", padx=5)
        self.admin_user = ttk.Entry(portal_frame, width=20)
        self.admin_user.grid(row=1, column=1, sticky="w", padx=5)
        
        ttk.Label(portal_frame, text="Admin Password:").grid(row=2, column=0, sticky="w", padx=5)
        self.admin_password = ttk.Entry(portal_frame, width=20, show="*")
        self.admin_password.grid(row=2, column=1, sticky="w", padx=5)
        
        # Single User Update Frame
        single_frame = ttk.LabelFrame(self.root, text="Single User Password Update", padding="10")
        single_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        
        ttk.Label(single_frame, text="Username:").grid(row=0, column=0, sticky="w", padx=5)
        self.username_combo = ttk.Combobox(single_frame, values=self.month_usernames, state="readonly", width=10)
        self.username_combo.grid(row=0, column=1, padx=5)
        
        ttk.Label(single_frame, text="New Password:").grid(row=1, column=0, sticky="w", padx=5)
        self.password_entry = ttk.Entry(single_frame, width=20, show="*")
        self.password_entry.grid(row=1, column=1, padx=5)
        
        self.update_btn = ttk.Button(single_frame, text="Update Password", command=self.update_single_password)
        self.update_btn.grid(row=2, column=1, pady=10)
        
        # Bulk Update Frame
        bulk_frame = ttk.LabelFrame(self.root, text="Bulk Password Update", padding="10")
        bulk_frame.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        
        ttk.Label(bulk_frame, text="Password for all:").grid(row=0, column=0, sticky="w", padx=5)
        self.bulk_password = ttk.Entry(bulk_frame, width=20, show="*")
        self.bulk_password.grid(row=0, column=1, padx=5)
        
        ttk.Label(bulk_frame, text="Select Users:").grid(row=1, column=0, sticky="nw", padx=5)
        
        # Create frame for checkboxes
        checkbox_frame = ttk.Frame(bulk_frame)
        checkbox_frame.grid(row=1, column=1, padx=5, pady=5)
        
        self.user_vars = {}\n        for i, username in enumerate(self.month_usernames):
            var = tk.BooleanVar()
            self.user_vars[username] = var
            cb = ttk.Checkbutton(checkbox_frame, text=username, variable=var)
            cb.grid(row=i//3, column=i%3, sticky="w", padx=2)
        
        self.bulk_update_btn = ttk.Button(bulk_frame, text="Bulk Update", command=self.update_bulk_passwords)
        self.bulk_update_btn.grid(row=2, column=1, pady=10)
        
        # Progress Bar
        self.progress = ttk.Progressbar(self.root, mode='determinate')
        self.progress.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        
        # Log Frame
        log_frame = ttk.LabelFrame(self.root, text="Operation Log", padding="10")
        log_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80)
        self.log_text.grid(row=0, column=0, sticky="ew")
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        log_frame.columnconfigure(0, weight=1)
        
    def log_message(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def validate_inputs(self):
        if not self.portal_url.get() or not self.admin_user.get() or not self.admin_password.get():
            messagebox.showerror("Validation Error", "Please fill in all portal configuration fields.")
            return False
        return True
        
    def update_single_password(self):
        if not self.validate_inputs():
            return
            
        username = self.username_combo.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Validation Error", "Please select a username and enter a password.")
            return
            
        # Run in thread to prevent UI blocking
        threading.Thread(target=self._update_password_thread, args=(username, password), daemon=True).start()
        
    def update_bulk_passwords(self):
        if not self.validate_inputs():
            return
            
        selected_users = [user for user, var in self.user_vars.items() if var.get()]
        password = self.bulk_password.get()
        
        if not selected_users or not password:
            messagebox.showerror("Validation Error", "Please select users and enter a password.")
            return
            
        # Run in thread to prevent UI blocking
        threading.Thread(target=self._bulk_update_thread, args=(selected_users, password), daemon=True).start()
        
    def _update_password_thread(self, username, password):
        try:
            self.log_message(f"Starting password update for user: {username}")
            success = self.call_vidyo_api(username, password)
            
            if success:
                self.log_message(f"✓ Password updated successfully for {username}")
                self.password_entry.delete(0, tk.END)
            else:
                self.log_message(f"✗ Failed to update password for {username}")
        except Exception as e:
            self.log_message(f"✗ Error updating {username}: {str(e)}")
            
    def _bulk_update_thread(self, usernames, password):
        self.progress['maximum'] = len(usernames)
        self.progress['value'] = 0
        
        for i, username in enumerate(usernames):
            self._update_password_thread(username, password)
            self.progress['value'] = i + 1
            self.root.update_idletasks()
            
        self.log_message(f"Bulk update completed for {len(usernames)} users.")
        
    def call_vidyo_api(self, username, password):
        """
        Call Vidyo UpdateMember API to change user password
        This is a placeholder implementation - you'll need to implement the actual SOAP call
        """
        try:
            # TODO: Implement actual SOAP call to Vidyo API
            # For now, this is a simulation
            
            portal_url = self.portal_url.get()
            admin_user = self.admin_user.get()
            admin_pass = self.admin_password.get()
            
            # Example of what the actual implementation would look like:
            """
            # Construct SOAP envelope for UpdateMember
            soap_envelope = f'''<?xml version="1.0" encoding="utf-8"?>
            <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                <soap:Header>
                    <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
                        <wsse:UsernameToken>
                            <wsse:Username>{admin_user}</wsse:Username>
                            <wsse:Password>{admin_pass}</wsse:Password>
                        </wsse:UsernameToken>
                    </wsse:Security>
                </soap:Header>
                <soap:Body>
                    <UpdateMember xmlns="http://portal.vidyo.com/admin">
                        <memberID>{username}</memberID>
                        <member>
                            <name>{username}</name>
                            <password>{password}</password>
                        </member>
                    </UpdateMember>
                </soap:Body>
            </soap:Envelope>'''
            
            headers = {
                'Content-Type': 'text/xml; charset=utf-8',
                'SOAPAction': 'UpdateMember'
            }
            
            response = requests.post(
                f"{portal_url}/services/v1_1/VidyoPortalAdminService",
                data=soap_envelope,
                headers=headers,
                auth=HTTPBasicAuth(admin_user, admin_pass),
                timeout=30
            )
            
            return response.status_code == 200 and 'OK' in response.text
            """
            
            # Placeholder simulation
            import time
            time.sleep(1)  # Simulate API call delay
            return True
            
        except Exception as e:
            self.log_message(f"API Error: {str(e)}")
            return False

def main():
    root = tk.Tk()
    app = VidyoPasswordManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()