import ssl
import argparse
import csv
from pyVim import connect
from concurrent.futures import ThreadPoolExecutor

def read_file_content(file_path):
    with open(file_path, 'r') as file:
        content = file.read().strip()
    return content

def connect_to_host(host, user, password, cert_path):
    ssl_context = ssl.create_default_context(cafile=cert_path)
    
    try:
        service_instance = connect.SmartConnect(
            host=host,
            user=user,
            pwd=password,
            port=443,
            sslContext=ssl_context
        )
        return host, user, password, "Success"
    except Exception as e:
        return host, user, password, str(e)

def disconnect_from_host(service_instance, host):
    if service_instance:
        connect.Disconnect(service_instance)

def main():
    parser = argparse.ArgumentParser(description="Connect to ESXi hosts using different combinations of credentials.")
    parser.add_argument("--hosts", required=True, help="Path to the hosts file")
    parser.add_argument("--usernames", required=True, help="Path to the usernames file")
    parser.add_argument("--passwords", required=True, help="Path to the passwords file")
    parser.add_argument("--cert", required=True, help="Path to the certificate file")
    parser.add_argument("--output", help="Path to the output CSV file")
    args = parser.parse_args()

    try:
        with open(args.hosts, 'r') as file:
            hostnames = file.read().splitlines()

        with open(args.usernames, 'r') as file:
            usernames = file.read().splitlines()

        with open(args.passwords, 'r') as file:
            passwords = file.read().splitlines()

        if args.output:
            with open(args.output, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["Host", "Username", "Password", "Status"])
        else:
            print("Connecting to hosts...")

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for host in hostnames:
                for username in usernames:
                    for password in passwords:
                        futures.append(executor.submit(connect_to_host, host, username, password, args.cert))

            for future in futures:
                host, username, password, error_message = future.result()
                if error_message:
                    if "incorrect user name or password" in error_message.lower(): 
                        status = "Wrong Creds"
                    else:
                        status = "Error: " + error_message
                else:
                    status = "Success"

                if args.output:
                    with open(args.output, 'a', newline='') as csvfile:
                        csv_writer = csv.writer(csvfile)
                        csv_writer.writerow([host, username, password, status])
                else:
                    print("Host:", host, "Username:", username, "Password:", password, "Status:", status)

                if status == "Success":
                    # Add required actions on the connected host here
                    disconnect_from_host(service_instance, host)
                    if not args.output:
                        print("Disconnected from host:", host)
                if not args.output:
                    print("-" * 40)

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
