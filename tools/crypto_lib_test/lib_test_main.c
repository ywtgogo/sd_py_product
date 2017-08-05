#include <stdio.h>
#include <string.h>
#include <stdio.h>
#include "aes256.h"
#include "sha1.h"
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <getopt.h>

#define BLOCK_SIZE 4096
#define SHA1_SIZE 20

unsigned char aesivv[20] = "SandlacusData#@1";
unsigned char aeskey[40] = "SandlacusData#@1SandlacusData#@1";

#define pvPortMalloc malloc
#define pvFree	     free

typedef struct 
{
	unsigned int addr;
	unsigned int length;
} fota_pac_header;

typedef struct
{
	unsigned int addr;
	unsigned int length;
	char block_sha1[1272];
	char img_sha1[32];
} fota_subnode_header;

typedef struct 
{
	char header_sha1[32];
	unsigned int dt;
	unsigned char hwver[4];
	char hw_info[24];
	unsigned char swver[4];
	char sw_info[92];
	fota_subnode_header subnode_header[2];
} fota_node_header;


unsigned char hex_str[21] = {0};

unsigned char aes_input[1024] = "{\"msgid\":\"1231412\",\"t\":\"10\",\"sid\":\"21004444\",\"did\":\"04651543\",\"dt\":\"20481\",\"src\":\"192.168.10.95\",\"p\":\"1\",\"nt\":\"2G\",\"data\":\"1\",\"ts\":\"2223232323232\",\"m\":\"18516524401\",\"fwv\":\"0.0.0.1\",\"hwv\":\"0.0.0.1\",\"man\":\"SANDLUCAS\",\"os\":\"ld\",\"ext\":{}}";
unsigned char aes_input_check[1024] = "{\"msgid\":\"1231412\",\"t\":\"10\",\"sid\":\"21004444\",\"did\":\"04651543\",\"dt\":\"20481\",\"src\":\"192.168.10.95\",\"p\":\"1\",\"nt\":\"2G\",\"data\":\"1\",\"ts\":\"2223232323232\",\"m\":\"18516524401\",\"fwv\":\"0.0.0.1\",\"hwv\":\"0.0.0.1\",\"man\":\"SANDLUCAS\",\"os\":\"ld\",\"ext\":{}}";
unsigned char base64_enc[1500] = {0};
unsigned char base64_check[1500] = "2QTNxkWBuuL0VOXpaVX4anKzkV1FRqglTbQ3QL9NOgBG9yiLUzYJFfa2FmJ3KeMh+uSH/dxymQJRiLxGgVHnKUKpNtzrU+TLRCMX6DpbYkv0KWSPEHjsyMAtI+Ys7pfleTjqfvDXXbwLPvbUyg+zR0Hxw7TXDhEf0iQgenfUEsT6GVZwH+1GgBCjLg8U7mq2OhhvXF+TbB3CqVM/jzCtopsl61gp3G6AK3jwWB+Un3LP+Je1M1nXT9avfhk1gPMZ5hdqEu6LTq0JgM2BiuAheaWBRq5IPDPonjo2VBvThMe/wZ4tLIOoKIVt0eVD1wse";


int uart_encode_decode()
{
	unsigned char ibuf[] = { 0x7e, 0x7d,0x34,0x44 ,0x5d, 0x5e, 0x53, 0xcc, 0x7d, 0xee, 0x11, 0x23, 0xdd, 0x7e, 0x7d, 0x7e, 0x7d};
	int len = sizeof(ibuf);
	printf("len = %d\r\n",len);
	int i,elen,delen;
	unsigned char * eBuf, *dbuf;
	
	printf("origin data:\r\n");
	for (i = 0; i < len; i++)
		printf("0x%x ", ibuf[i]);
	printf("\n");

	eBuf = (unsigned char *)malloc(2 * len);
	elen = uartEncode(ibuf, len, eBuf);
	printf("encoding data:\r\n");
	for (i = 0; i < elen; i++)
		printf("0x%x ", eBuf[i]);
	printf("\n");

	dbuf = (unsigned char *)malloc(elen);
	delen = uartDecode(eBuf, elen, dbuf);
	printf("decoding data:\r\n");
	for (i = 0; i < delen; i++)
		printf("0x%x ", dbuf[i]);
	printf("\n");

	free(dbuf);
	free(eBuf);

	return 0;
}

int aes_test()
{
	AES_KEY enc_key;
	size_t count = 0;
	int len;
	int i;

	unsigned char *unencrypted;
	unsigned char *encrypted;
	unsigned char ivv[SHA1_SIZE] = { '\0' };
	unencrypted = (char *)malloc(BLOCK_SIZE);
	encrypted = (char *)malloc(BLOCK_SIZE);

	memset(encrypted, 0, BLOCK_SIZE);


	len = AES_base64_encrypt(aeskey, aesivv, (unsigned char *)aes_input, (unsigned char *)encrypted, strlen(aes_input));

	printf("%s\r\n", encrypted);


	for (i=0;i<len;i++)
		if (encrypted[i] != base64_check[i])
		{
			printf("encrypt failed\r\n");
		}


	len = AES_base64_decrypt(aeskey, aesivv, (unsigned char *)encrypted, (unsigned char *)unencrypted, strlen(encrypted));

	unencrypted[len]=0;

	printf("%s\r\n", unencrypted);



	free(encrypted);
	free(unencrypted);



}

int main(int argc,char *argv[])
{

	aes_test();
	uart_encode_decode();
	
	return 0;
}
