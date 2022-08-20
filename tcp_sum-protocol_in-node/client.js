const MSG = "\r\n10 20 abc\r\n999 1\r\n1000 0\r\n10   20 30";
const MSG_2 = "\r\n";

const PORT = 2020;
const HOST = "127.0.0.1";

const client = require('net').createConnection({ port: PORT, host: HOST }, () => {
  client.write(MSG);
}).on('data', buffer => {
  console.log(buffer.toString());
  client.end();
}).on('error', err => {
  console.error(err);
})