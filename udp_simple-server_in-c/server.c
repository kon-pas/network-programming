#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <string.h>

#define BUFF_SIZE 1
#define MESSAGE	"Hello, world!\r\n"

void handleError(char *msg) {
	perror(msg);
	exit(EXIT_FAILURE);
}

int main(int argc, char* argv[])
{
	int server_fd, client_address_length;
	struct sockaddr_in server_address;
	struct sockaddr_in client_address;
	char buf[BUFF_SIZE];

	memset(&server_address, 0, sizeof(server_address));
	server_address.sin_family = AF_INET;
	server_address.sin_addr.s_addr = htonl(INADDR_ANY); 
  server_address.sin_port = htons(atoi(argv[1]));

	memset(&client_address, 0, sizeof(client_address));

	if((server_fd = socket(AF_INET, SOCK_DGRAM, 0)) == -1) handleError("Socket error");
	if(bind(server_fd, (struct sockaddr *)&server_address, sizeof(server_address)) == -1) handleError("Bind error");

	while(1) {
		client_address_length = sizeof(client_address);
		if(recvfrom(server_fd, (char *)buf, BUFF_SIZE - 1, 0, (struct sockaddr *) &client_address, &client_address_length) == -1) handleError("Recvfrom error");
		if(sendto(server_fd, (const char *)MESSAGE, strlen(MESSAGE), 0, (const struct sockaddr *) &client_address, client_address_length) == -1) handleError("Sendto error");
	}

	if(close(server_fd) == -1) handleError("Close error");

	return 0;
}