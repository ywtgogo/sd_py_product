LIB_SRC_PATH ?= /home/jenkins/sboxwifi_esp_opt_production/crypto

all: lib_test
lib_test: aes256.c aes256.h sha1.c sha1.h crc.c crc.h uartEncodeDecode.c uartEncodeDecode.h
	gcc -g aes.c sha1.c crc.c uartEncodeDecode.c  lib_test_main.c -o lib_test -std=c99

aes256.c:
	ln -sf $(LIB_SRC_PATH)/aes256.c aes256.c

aes256.h:
	ln -sf $(LIB_SRC_PATH)/aes256.h aes256.h

aes.c:
	aes256.c aes256.h

sha1.c:
	ln -sf $(LIB_SRC_PATH)/sha1.c sha1.c

sha1.h:
	ln -sf $(LIB_SRC_PATH)/sha1.h sha1.h

crc.c:
	ln -sf $(LIB_SRC_PATH)/crc.c crc.c

crc.h:
	ln -sf $(LIB_SRC_PATH)/crc.h crc.h

uartEncodeDecode.c:
	ln -sf $(LIB_SRC_PATH)/uartEncodeDecode.c uartEncodeDecode.c

uartEncodeDecode.h:
	ln -sf $(LIB_SRC_PATH)/uartEncodeDecode.h uartEncodeDecode.h


.PHONY:clean all
clean:
	rm lib_test 
