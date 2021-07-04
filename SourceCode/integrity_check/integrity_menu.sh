#!/bin/bash

# 路径设置
usb=/media
integrity_pwd=$usb/integrity_check
os_path="/boot"
# 这里获取的是最新的版本，可能没有考虑更新的问题
VERSION=`ls ${os_path}/lib/modules | awk 'END {print}'`
BOOT="${os_path}/boot"
MODULES="${os_path}/lib/modules/${VERSION}/kernel"

# Add "Update the standard kernel snapshot"
while true
do
    dialog --clear --no-cancel --ok-label "Select" --title "Integrity Check" \
        --menu 'Select the function to perform:' 18 55 10 \
        '1' ' Check the integrity of kernel files' \
        '2' ' View the checking results' \
        '3' ' Recovery kernel files' \
        '4' ' Exit' \
        2>/tmp/fist/int_option
# '2' ' Generate the snapshot of specified directory' \
# '3' ' Check the integrity of specified directory' \
    int_option=$(cat /tmp/fist/int_option)

    case "$int_option" in
        "1" )
            # standard files
            LIST_ST=${integrity_pwd}/standard/checksum_standard_${VERSION}.log
            TAR_ST=${integrity_pwd}/standard/tar_checksum_standard_${VERSION}.log
            # If run in the first time, generate standard snapshot.
            is_first=`cat ${integrity_pwd}/is_first`
            if [ $is_first -eq 1 ] 
            then
                # init
                dialog --infobox "Generating snapshot of kernel files for the first time..." 20 60
                touch ${LIST_ST} && touch ${TAR_ST}
                . ${integrity_pwd}/snapshot.sh ${LIST_ST} | dialog --gauge "Generating snapshots for the first time..." 20 60
                . ${integrity_pwd}/tar_snapshot.sh ${TAR_ST}
                # end init
                . ${integrity_pwd}/clear_snapshot.sh
                echo 0 > ${integrity_pwd}/is_first
                clear
                continue
            fi

            # check according to the standard file
            TIME=`date +"%y_%m_%d_%H_%M_%S"`
            LIST_CU=/tmp/fist/checksum_${VERSION}_${TIME}.log
            TAR_CU=/tmp/fist/tar_checksum_${VERSION}_${TIME}.log
            # tar_snapshot
            dialog --infobox "Quick checking..." 20 60
            . ${integrity_pwd}/tar_snapshot.sh ${TAR_CU}
            # tar_check
            sum=0
            tar_pass=1
            for hash in `cat $TAR_CU`
            do
                if [ `expr $sum % 2` -eq 1 ]; then sum=$((sum+1)); continue; fi
                found=0
                for s in `cat $TAR_ST`
                do
                    if [ $hash = $s ]; then found=1; break; fi 
                done
                if [ $found -eq 0 ]; then tar_pass=0; break; fi
                sum=$((sum+1))
            done

            if [ $tar_pass -eq 1 ]
            then dialog --msgbox "Pass the check!" 20 60
            else
                if (dialog --title "S-Safety" --yesno "The kernel files have been changed. \nDo you want to check in detail?" 20 60)
                then
                    # snapshot of files
                    dialog --infobox "Generating snapshot of kernel files..." 20 60
                    . ${integrity_pwd}/snapshot.sh ${LIST_CU} | dialog --gauge "Generating snapshots..." 20 60
                    dialog --msgbox "Work done. \nSee the results." 20 60
                    # checking
                    DIFF=/tmp/fist/diff.log
                    RESULT=/tmp/fist/diff_result.log
                    # CURRENT=./checksum_current.log
                    # STANDARD=./checksum_standard.log
                    touch ${DIFF} && diff ${LIST_CU} ${LIST_ST} > ${DIFF}
                    touch ${RESULT} && echo -n "" > ${RESULT}
                    LINES=1
                    while read line
                    do
                        if [[ ${#line} -le 20 && ${line} != "---" ]]
                        then 
                            pos=`expr index "$line" adc - 1`
                            file_line=`sed -n "$((LINES+1)) p" ${DIFF}`
                            file_name=${file_line:`expr index "$file_line" / - 1`:${#file_line}} # current
                            case ${line:$pos:1} in
                                "a" )
                                    echo "Missing: ${file_name}" >> ${RESULT}
                                ;;
                                "d" )
                                    echo "New added: ${file_name}" >> ${RESULT}
                                ;;
                                "c" )
                                    standard_file_line=`sed -n "$((LINES+3)) p" ${DIFF}`
                                    standard_file_name=${standard_file_line:`expr index "$standard_file_line" / - 1`:${#standard_file_line}}
                                    if [ $standard_file_name = $file_name ]
                                    then
                                        echo "Modified: ${standard_file_name}" >> ${RESULT}
                                    else
                                        echo "Modified: from ${standard_file_name} to ${file_name}" >> ${RESULT}
                                    fi
                                ;;
                                "*" )
                                    echo "Something wrong." >> ${RESULT}
                                ;;
                            esac
                        fi
                        LINES=$((LINES+1))
                    done < ${DIFF}
                    dialog --title "The result of integrity check" --textbox ${RESULT} 20 70
                else clear
                fi
            fi
            clear
        ;;

        "2" )
            # 
        ;;

        "3" )
            # 
        ;;

        # "2" )
        #     USER_PATH_FILE=/tmp/fist/integrity_path
        #     if (dialog --title "Choose a file or a directory" --fselect "/boot/" 12 60 2>${USER_PATH_FILE})
        #     then 
        #         USER_PATH=$(cat ${USER_PATH_FILE})
        #         if [ -e ${USER_PATH} ] 
        #         then dialog --msgbox "You've chosen: ${USER_PATH} \nA snapshot will be generated." 20 60
        #         else dialog --msgbox "The path ${USER_PATH} is not vaild, please choose again." 20 60
        #         fi
        #         # Generate log file and save it.
        #         dialog --infobox "Generating snapshot..." 20 60
        #         sleep 1 # ./snapshot.sh
        #         dialog --msgbox "Work done!" 20 60
        #     else clear
        #     fi
        # ;;

        # "3" )
        # dialog --msgbox "Same as the checking of kernel files" 20 60
        # ;;

        "4" )
            # Go back to func_menu
            . ${integrity_pwd}/clear_snapshot.sh
            clear
            break
        ;;
    esac
done
