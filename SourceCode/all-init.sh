#!/bin/sh
# usb=$( cd "$( dirname "$0" )" && pwd ) # usb=bin
usb=/media
cp $usb/tools/ld-2.27.so /bin/

# ld + binary_file
alias dialog="ld-2.27.so $usb/tools/dialog/dialog"
alias diff="ld-2.27.so $usb/tools/diff/diff"
alias file="ld-2.27.so $usb/tools/file/file"
alias clear="ld-2.27.so $usb/tools/clear/clear"

alias openssl="ld-2.27.so $usb/openssl/openssl"
alias clamscan="ld-2.27.so $usb/sig_detect/bin/clamscan"
alias sed="ld-2.27.so $usb/sig_detect/bin/sed"

. $usb/tools/tools-init.sh
. $usb/openssl/openssl-init.sh
. $usb/ml_detect/py-init.sh
# . $usb/sig_detect/clam-init.sh

# for sda mount
insmod /lib/modules/libata.ko
insmod /lib/modules/libahci.ko
insmod /lib/modules/ahci.ko

echo "init success!"
