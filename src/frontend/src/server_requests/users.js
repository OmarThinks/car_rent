import axios from 'axios';
import host from "./host";

//console.log(host);

var loginUsers = (username,password) => {
  return axios({
    method: 'post',
    url: host+'/users/login',
    data:
    {
      username: username,
      password: password
    }
  });
}

export {loginUsers as loginUsers};
