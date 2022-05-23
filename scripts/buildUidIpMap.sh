#!/usr/bin/env bash

function truncateFile () {
  truncate -s 0 "$dir/ips-nginx.txt"
  truncate -s 0 "$dir/ips-http-output.txt"
}

function parseFileForHTTP () {
  while read uid
  do
    echo "https://${albURL}/web/${uid}"
  done <"$dir/ips.txt" >>"$dir/ips-http-output.txt"
}

function parseFileForNginxWoutIP () {
  idx=100
  while read uid
  do
    echo "location /web/${uid} {"
    echo "proxy_pass https://${baseIp}${idx}:5601;"
    echo "}"
   (( idx++ ))
  done <"$dir/ips.txt" >>"$dir/ips-nginx.txt"
}

if [[ $# -ne 2 ]]; then
  echo "2 args are required"
  echo "arg 1 - the base ip"
  echo "arg 2 - the alb url"
fi

dir="./scripts/output"
if [[ ! -d "$dir" ]]; then
  mkdir "$dir"
fi

cat ./scripts/new-uid.txt > "$dir/ips.txt"
baseIp="$1"
albURL="$2"

truncateFile
parseFileForNginxWoutIP
parseFileForHTTP

