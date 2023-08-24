# ESXiBrute
This script allows you to connect to ESXi hosts using different combinations of credentials (username and password), Inshort it is used to bruteforce ESXi Host Credentials. It can be useful for testing and validating various credentials against multiple hosts.

You can refer to [Attacking and Pentesting ESXi Hosts article here](https://www.hackingdream.net/2023/08/attacking-and-pentesting-vmware-esxi.html)

## Install

```
 pip install pyVim
 git clone https://github.com/Bhanunamikaze/ESXiBrute.git
 cd ESXiBrute
 python ESXi_Brute.py --hosts hosts.txt --usernames usernames.txt --passwords passwords.txt --cert cert.pem [--output output.csv]
```

## Usage

### ESXi_Brute 
```
python ESXi_Brute.py --hosts hosts.txt --usernames usernames.txt --passwords passwords.txt --cert cert.pem [--output output.csv]
--hosts: Path to the file containing a list of hostnames.
--usernames: Path to the file containing a list of usernames.
--passwords: Path to the file containing a list of passwords.
--cert: Path to vCenter Root certificate.
--output: (Optional) Path to the output CSV file. If not specified, the output will be displayed on the screen.
```

### Resxtop_Brute.sh

Resxtop_Brute.sh - script is used to Bruteforce Usernames and Passwords for multiple hosts at once (No Parallel Processing or Multi Threading)

Download and Install [Resxtop from VMWare](https://developer.vmware.com/web/tool/8.0/resxtop)

```
export LD_LIBRARY_PATH=/usr/lib/vmware/resxtop/
chmod +x Resxtop_Brute.sh
./Resxtop_Brute.sh hosts.txt usernames.txt passwords.txt
```

## Note
- cert.pem is requried ESX first checks whether a certificate file is available. If not, ESXCLI checks whether a thumbprint of the target server is available. If not, you receive an error saying cert or thumbprint not valid. To Resolve this issue, you need to download a valid vCenter root certificate from https://vcenter.domain.com/certs/download.zip.
- Once you have the certificate, convert it to .pem file using below command
   - openssl x509 -in your_certificate.crt -out your_certificate.pem -outform PEM
