#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <stdbool.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define BUF_SIZE 100

void handleError(char *msg) {
	perror(msg);
	exit(EXIT_FAILURE);
}

int main (int argc, char *argv[]) {
	int client_fd, bytes;

	struct sockaddr_in server_address;
	memset(&server_address, 0, sizeof(server_address));
	server_address.sin_family = AF_INET;
	server_address.sin_addr.s_addr = inet_addr(argv[1]);
	server_address.sin_port = htons(atoi(argv[2]));

	if((client_fd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == -1) handleError("Socket error");

	char buf[BUF_SIZE] = "100 200 300 400";

	socklen_t server_address_length;	// ?

	if(sendto(client_fd, buf, strlen(buf), 0, (struct sockaddr*)&server_address, sizeof(server_address)) == -1) handleError("Sendto error");

	memset(buf, 0, sizeof(buf));

	if((bytes = recvfrom(client_fd, (char *)buf, BUF_SIZE, 0, (struct sockaddr *)&server_address, &server_address_length)) == -1) handleError("Recvfrom error");

	if(write(STDOUT_FILENO,  buf, strlen(buf)) == -1) handleError("Write error");
	
	if(close(client_fd) == -1) handleError("Close error");
}