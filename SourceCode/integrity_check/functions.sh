#!/bin/bash
function hash_entry() {
    hash=`openssl dgst -sm3 $1`
    index=`expr index "${hash}" \=`
    hash=${hash:$((index+1)):${#hash}}
    entry=${hash}" "$1
    echo ${entry}
}

function read_dir(){
for file in `ls -a $1` #注意此处这是两个反引号，表示运行系统命令
do
    if [[ ${file} = "." || ${file} = ".." ]]
    then continue 
    fi

    if [ -d $1"/"$file ] #注意此处之间一定要加上空格，否则会报错
    then
        read_dir $1"/"$file $2
    else
        absolute_path=$1"/"$file
        # hash=`sudo openssl dgst -sm3 ${absolute_path}`
        # index=`expr index "$hash" \=`
        # hash=${hash:$((index+1)):${#hash}}
        # entry=${hash}" "${absolute_path}
        hash_entry ${absolute_path} >> $2
        count=$((count+1))
        count_100=`expr $count \* 100`
        echo `expr $count_100 / $sum`
    fi
done
}
