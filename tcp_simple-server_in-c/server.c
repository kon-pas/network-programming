#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <sys/socket.h>

void handleError(char *msg) {
  perror(msg);
  exit(EXIT_FAILURE);
}

int main(int argc, char *argv[]) {
  int server_fd, client_fd;
  struct sockaddr_in server_address;
  char *msg = "Hello, world!\r\n";

  memset(&server_address, 0, sizeof(server_address));
  server_address.sin_family = AF_INET;
  server_address.sin_port = htons(atoi(argv[1]));
  server_address.sin_addr.s_addr = htonl(INADDR_ANY);

  if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == -1) handleError("Socket error");
  if(bind(server_fd, (struct sockaddr *)&server_address, sizeof(server_address)) == -1) handleError("Bind error");
  if(listen(server_fd, 1) == -1) handleError("Listen error");

  while(1) {
    if((client_fd = accept(server_fd, NULL, 0)) == -1) handleError("Accept error");
    else {
      if(write(client_fd, msg, strlen(msg)) == -1) handleError("Write error");
      if(close(client_fd) == -1) handleError("Close error");
    }
  }

  return 0;
}