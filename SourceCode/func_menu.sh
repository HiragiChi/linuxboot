#!/bin/bash

mkdir /tmp/fist 2> /dev/null
usb=/media

while true
do
# 3 and 4 may combine
# '3' ' Detect malware' \
    dialog --clear --no-cancel --ok-label "Select" --title "LIST Function Menu" \
        --menu 'Select the function to perform:' 18 50 10 \
        '1' ' Boot OS directly' \
        '2' ' Check the integrity of files' \
        '3' ' Detect malware by ClamAV' \
        '4' ' Detect malware by Machine Learning' \
        '5' ' Send file to the sandbox' \
        '6' ' Enter recovery shell' \
        2>/tmp/fist/func_option

    func_option=$(cat /tmp/fist/func_option)

    case "$func_option" in
        "1" )
            # use heads script to boot os
            dialog --clear --msgbox "Boot OS derectly" 20 60
        ;;
        "2" )
            . $usb/integrity_check/integrity_menu.sh
        ;;
        "3" )
            . $usb/sig_detect/clamav_detect.sh
        ;;
        "4" )
            ML_PATH_FILE=/tmp/fist/ml_path_to_check
            if (dialog --title "Choose a file or a directory" --fselect "/" 12 60 2>${ML_PATH_FILE})
            then
                ML_PATH=`cat ${ML_PATH_FILE}`
            fi
            $usb/ml_detect/ML_detect.sh ${ML_PATH}
        ;;
        "5" )
            dialog --clear --msgbox "Conmunicate with cuckoo..." 20 60
        ;;
        "6" )
            clear
            break
        ;;
    esac
done