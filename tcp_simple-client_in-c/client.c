#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <stdbool.h>

#define nbytes 1

void handleError(char *msg) {
  perror(msg);
  exit(EXIT_FAILURE);
}

bool drukowalne(const void *buf) {
  char *characters = (char *)buf;
  int i = 0;
  while (*characters != 0)
  {
    if (!(32 <= *characters) || !(*characters <= 126)) return false;
    characters++;
  }
  return true;
}

int main(int argc, char *argv[]) {
  int client_fd, byte;
  struct sockaddr_in server_address;
  char buf[nbytes];
  bool shouldRead = true;

  memset(&server_address, 0, sizeof(server_address));
  server_address.sin_family = AF_INET;
  server_address.sin_port = htons(atoi(argv[2]));
  server_address.sin_addr.s_addr = inet_addr(argv[1]);

  if((client_fd = socket(AF_INET, SOCK_STREAM, 0)) == -1) handleError("Socket error");
  if(connect(client_fd, (struct sockaddr *)&server_address, sizeof(server_address)) == -1) handleError("Connect error");

  while(shouldRead) {
    switch(byte = read(client_fd, buf, nbytes)) {
      case -1: handleError("Read error");
      case 0: shouldRead = false;
      default: if(drukowalne(buf)) write(STDOUT_FILENO, buf, byte);
    }
  }
  
  if(close(client_fd) == -1) handleError("Close error");

  return 0;
}