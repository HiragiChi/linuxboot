#!bin/bash
gcc -w -o server server.c -lssl -lcrypto
gcc -w -o client client.c -lssl -lcrypto
./server 8888
# ./client 127.0.0.1 8888