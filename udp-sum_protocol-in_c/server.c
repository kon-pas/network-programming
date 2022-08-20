// UINT32_MAX = 4294967295

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <limits.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <stdint.h>
#include <unistd.h>

#define PORT 2020
#define TRUE 1
#define BUFFER_SIZE 9999
#define MESSAGE_ERROR "ERROR"
#define PRINT_ON_SERVER_SIDE 0

typedef int descriptor;
typedef char* string;

void handle_error(int status, char *message) {
  if(status == -1) {
    perror(message);
    exit(EXIT_FAILURE);
  }
}

uint32_t power(uint32_t x, uint32_t y) {
  if (y == 0) return 1;
  else if (y % 2 == 0) return power(x, y / 2) * power(x, y / 2);
  else return x * power(x, y/2) * power(x, y / 2);
}

string decode_message(ssize_t message_length, char buffer[BUFFER_SIZE]) {
  uint32_t sum = 0;
  uint32_t number;
  uint32_t addition;
  uint32_t number_length;
  uint32_t number_index;
  uint32_t index;
  string message = malloc(message_length);
  for(index = 0; index < message_length; ++index) {
    while(buffer[index] == ' ') ++index;
    if('0' <= buffer[index] && buffer[index] <= '9') {
      number_length = 0;
      while('0' <= buffer[index + number_length] && buffer[index + number_length] <= '9') {
        ++number_length;
      }
      number = 0;
      number_index = 0;
      for(number_index = index; number_index < index + number_length; ++number_index) {
        addition = (buffer[number_index]- 48) * power(10, number_length - (number_index - index) - 1);
        if (number > UINT32_MAX - addition) return MESSAGE_ERROR;
        else number += addition;
        
      }
      if (sum > UINT32_MAX - number) return MESSAGE_ERROR;
      else sum += number;
      index += number_length - 1;
    }
    else if(buffer[index] == '\r' && buffer[index+1] == '\n') {
      if(index + 1 == message_length - 1) break;
      else return MESSAGE_ERROR;
    }
    else if(buffer[index] == 10) {
      if(index == message_length - 1) break;
      else return MESSAGE_ERROR; 
    } 
    else return MESSAGE_ERROR;
  }
  sprintf(message, "%u", sum);
  return message;
}

int main() {
  struct sockaddr_in server_address;
  struct sockaddr_in client_address;
  descriptor server_file_descriptor;
  string buffer = malloc(BUFFER_SIZE);
  string message;
  ssize_t message_length;
  socklen_t client_address_length = (socklen_t) sizeof(client_address);
  socklen_t server_address_length = (socklen_t) sizeof(server_address);

  memset(&server_address, 0, server_address_length);
  memset(&client_address, 0, client_address_length);
  server_address.sin_family = AF_INET;
  server_address.sin_port = htons(PORT);
  server_address.sin_addr.s_addr = htonl(INADDR_ANY);

  handle_error(server_file_descriptor = socket(
    (int) AF_INET,
    (int) SOCK_DGRAM,
    (int) 0
  ), "Socket");

  handle_error(bind(
    (int) server_file_descriptor,
    (const struct sockaddr*) &server_address,
    (socklen_t) server_address_length
  ), "Bind");

  while(TRUE) {
    buffer = malloc(BUFFER_SIZE);

    handle_error(message_length = recvfrom(
      (int) server_file_descriptor,
      (void *restrict) buffer,
      (size_t) (BUFFER_SIZE - 1),
      (int) 0,
      (struct sockaddr *restrict) &client_address,
      (socklen_t *restrict) &client_address_length
    ), "Recvfrom");

    message = decode_message(message_length, buffer);

    handle_error(sendto(
      (int) server_file_descriptor,
      (const void *) message,
      (size_t) strlen(message), 
      (int) 0,
      (const struct sockaddr *) &client_address,
      (socklen_t) client_address_length
    ), "Sendto");

    if(PRINT_ON_SERVER_SIDE) printf("%s\n", message);
  }

  handle_error(close(
    (int) server_file_descriptor
  ), "Close");

  return 0;
}