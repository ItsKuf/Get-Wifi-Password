import subprocess

class WiFiPasswordGetter:
    @staticmethod
    def get_linux_wifi_passwords():
        try:
            wifi_connections = subprocess.check_output(['ls', '/etc/NetworkManager/system-connections']).decode('utf-8', errors="backslashreplace").split('\n')
            print("[+] WiFi Networks and Passwords (Linux):")
            print("---------------------------------------------")

            for wifi_connection in wifi_connections:
                if wifi_connection:
                    wifi_pass_output = subprocess.check_output(['cat', f"/etc/NetworkManager/system-connections/{wifi_connection}"]).decode('utf-8', errors="backslashreplace").split('\n')
                    for line in wifi_pass_output:
                        if "psk=" in line:
                            password = line.strip("psk=").strip('"')
                            print(f"{wifi_connection:<30} | {password}")
        except FileNotFoundError:
            print("[!] Error: WiFi configuration directory not found.")
        except subprocess.CalledProcessError:
            print("[!] Error: Failed to retrieve WiFi passwords.")
        except Exception as e:
            print(f"[!] Unexpected error occurred: {e}")

    @staticmethod
    def get_windows_wifi_passwords():
        try:
            wifi_profiles_output = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')
            profiles = [line.split(":")[1][1:-1] for line in wifi_profiles_output if "All User Profile" in line]

            print("[+] WiFi Networks and Passwords (Windows):")
            print("---------------------------------------------")

            for profile in profiles:
                try:
                    profile_details_output = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')
                    password_lines = [line.split(":")[1][1:-1] for line in profile_details_output if "Key Content" in line]
                    if password_lines:
                        password = password_lines[0]
                    else:
                        password = ""
                    print(f"{profile:<30} | {password}")
                except subprocess.CalledProcessError:
                    print(f"{profile:<30} | Error: Failed to retrieve password.")
                except Exception as e:
                    print(f"{profile:<30} | Error: {e}")
        except subprocess.CalledProcessError:
            print("[!] Error: Failed to retrieve WiFi profiles.")
        except Exception as e:
            print(f"[!] Unexpected error occurred: {e}")

def main():
    try:
        system_info = subprocess.check_output(['uname']).decode('utf-8', errors="backslashreplace").split('\n')[0]
    except FileNotFoundError:
        system_info = 'Windows'
    except subprocess.CalledProcessError:
        print("[!] Error: Failed to retrieve system information.")
        return
    except Exception as e:
        print(f"[!] Unexpected error occurred: {e}")
        return

    wifi_getter = WiFiPasswordGetter()

    if system_info == "Linux":
        wifi_getter.get_linux_wifi_passwords()
    else:
        wifi_getter.get_windows_wifi_passwords()

if __name__ == "__main__":
    main()

