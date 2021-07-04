#!/bin/bash

# BOOT="/boot"
# MODULES="/lib/modules/${VERSION}/kernel"

mkdir /tmp/fist 2> /dev/null
HASH_TAR=$1
touch ${HASH_TAR}
echo -n "" > ${HASH_TAR}

# maybe move the tar to USB
BOOT_TAR=/tmp/fist/boot_${VERSION}_${TIME}.tar
MODULES_TAR=/tmp/fist/modules_${VERSION}_${TIME}.tar
tar -cf ${BOOT_TAR} ${BOOT} 2> /dev/null
tar -cf ${MODULES_TAR} ${MODULES} 2> /dev/null

. ${integrity_pwd}/functions.sh
hash_entry ${BOOT_TAR} >> ${HASH_TAR}
hash_entry ${MODULES_TAR} >> ${HASH_TAR}

# sudo cp ${HASH_TAR} ./

