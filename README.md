This is a small python script to pull in failed attempts to login to your machine from potentially malicious sources.  There is no real major checking for accidental login failures yet, so use with caution.  This will only work on linux and is hardcoded for the secure file to be found at '/var/log/secure'.

You can create a whitelist.txt file and populate it with IPs you whish to whitelist so you don't end up accidentally locking yourself out.  I plan to add some logic to the script to not just block anyone who doesn't get in.
