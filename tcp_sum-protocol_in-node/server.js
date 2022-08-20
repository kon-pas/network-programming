// const MAX = 1000;
const MAX = Number.MAX_SAFE_INTEGER;

const PORT = 2020;
const HOST = "127.0.0.1";

let stack = [];
const encode = buffer => {
  let msg = "";
  let flag_overflow = false;
  let flag_wrong_char = false;
  let previous_character = null;
  buffer.forEach(character => {
    if (previous_character == 13 && character == 10) {
      if (stack.length == 0) msg += "ERROR\r\n";
      else {
        if (flag_wrong_char) {
          msg += "ERROR\r\n";
          flag_overflow = false;
          flag_wrong_char = false;
          stack.length = 0;
        } else {
          let sum = 0;
          stack.join('').split(' ').forEach(e => {
            if (e >= MAX) flag_overflow = true;
            else if (MAX - e <= sum) flag_overflow = true;
            else if (!Number.isNaN(parseInt(e))) sum += parseInt(e);
          });
          stack.length = 0;
          if (flag_overflow) {
            msg += "ERROR\r\n";
            flag_overflow = false;
            flag_wrong_char = false;
          } else msg += sum + "\r\n";
        }
      }
    }
    else if ((48 <= character && character <= 57) || character == 32) stack.push(String.fromCharCode(character));
    else if (character != 13) flag_wrong_char = true;
    previous_character = character;
  });
  return msg;
}

const server = require('net').createServer(socket => {
  socket.on('data', buffer => {
    const msg = encode(buffer);
    socket.write(msg);
  }).on('error', err => {
    console.error(err);
  }).on('end', () => { });
  // socket.pipe(socket);
}).on('error', err => {
  console.error(err);
}).listen({ port: PORT, host: HOST });