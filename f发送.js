const axios = require('axios');

axios.post('http://localhost:8080/send_private_msg', {
    user_id: 123456789, // 目标用户的 QQ 号
    message: 'Hello, go-cqhttp!', // 要发送的消息内容
  })
  .then((response) => {
    console.log(response.data);
  })
  .catch((error) => {
    console.error(error);
  });
