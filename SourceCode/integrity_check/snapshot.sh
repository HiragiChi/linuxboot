#!/bin/bash

# BOOT="/boot"
# MODULES="/lib/modules/${VERSION}/kernel"
# /lib/modules/4.19.0-16-amd64/kernel

mkdir /tmp/fist 2> /dev/null
HASH_LIST=$1
touch ${HASH_LIST}
echo -n "" > ${HASH_LIST}


sum1=`ls -a -lR ${BOOT} | grep "^-" | wc -l`
sum2=`ls -a -lR ${MODULES} | grep "^-" | wc -l`
sum=`expr $sum1 + $sum2`
count=0
. ${integrity_pwd}/functions.sh

# echo "***${BOOT}***" >> ${HASH_LIST}
read_dir ${BOOT} ${HASH_LIST}
# echo "***${MODULES}***" >> ${HASH_LIST}
read_dir ${MODULES} ${HASH_LIST}
echo 100

# sudo cp ${HASH_LIST} ./
