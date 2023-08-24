#!/bin/bash

# run resxtop
run_resxtop() {
    local host="$1"
    local user="$2"
    local password="$3"

    command="resxtop -a --server $host"
    echo -e "$user\n$password" | $command
}

# Read hosts, users, and passwords from separate files
read_credentials_from_files() {
    hosts=($(cat hosts.txt))
    users=($(cat users.txt))
    passwords=($(cat passwords.txt))
}

read_credentials_from_files

# Iterate through all combinations of users, hosts, and passwords
for host in "${hosts[@]}"; do
    for user in "${users[@]}"; do
        for password in "${passwords[@]}"; do
            run_resxtop "$host" "$user" "$password"
        done
    done
done
