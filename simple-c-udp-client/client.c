// Spróbuj napisać parę klient-serwer komunikującą się przy pomocy protokołu UDP.
// Pamiętaj o tym, że UDP nie nawiązuje połączeń,
// więc to klient będzie musiał jako pierwszy wysłać jakiś datagram,
// a serwer na niego odpowie. Sprawdź, czy możliwe jest wysyłanie pustych datagramów
// (tzn. o długości zero bajtów) — jeśli tak, to może niech klient właśnie taki wysyła?

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <string.h>
#include <stdbool.h>

#define BUFF_SIZE 50

void handleError(char *msg) {
	perror(msg);
	exit(EXIT_FAILURE);
}

int main(int argc, char* argv[]) {
	int client_fd, server_address_length, rec_len;
	struct sockaddr_in server_address;
	char invite[0];
	char buff[BUFF_SIZE];

	memset(&server_address, 0, sizeof(server_address));
	server_address.sin_family = AF_INET;
	server_address.sin_port = htons(atoi(argv[2])); 
	server_address.sin_addr.s_addr = inet_addr(argv[1]);
	server_address_length = sizeof(server_address);
	if((client_fd = socket(AF_INET, SOCK_DGRAM, 0)) == -1) handleError("Socket error");
	
	if(sendto(client_fd, (const char *)invite, strlen(invite), 0, (const struct sockaddr *) &server_address, sizeof(server_address)) == -1) handleError("Sendto error");
	if((rec_len = recvfrom(client_fd, (char *)buff, BUFF_SIZE, 0, (struct sockaddr *) &server_address, &server_address_length)) == -1) handleError("Recvfrom error"); // ssize_t len = recvfrom(sock, buf, sizeof(buf), 0, NULL, 0);
	else
		for(int i = 0; i < rec_len; i++)
			if((buff[i] >= 32 && buff[i] <= 126)) write(STDOUT_FILENO, &buff[i], 1);

	if(close(client_fd) == -1) handleError("Close error");
	return 0;
}
