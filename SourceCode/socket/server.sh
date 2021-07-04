#!bin/bash
gcc -w -o server server.c -lssl -lcrypto
gcc -w -o client client.c -lssl -lcrypto
./server 6666
# ./client 127.0.0.1 6666
