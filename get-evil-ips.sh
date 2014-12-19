#!/bin/sh

cat /var/log/secure | grep "Failed password for" | ./ipgrep.sh | sort | uniq
