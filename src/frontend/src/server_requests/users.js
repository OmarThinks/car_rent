import axios from 'axios';
import host from "./host";

console.log(host);

var loginUsers = (username,password) => {
  return new axios({
    method: 'post',
    url: host+'/users/login',
    data:
    {
      username: username,
      password: password
    }
  });
}

//module.exports={"loginUsers":loginUsers};
//module.exports.loginUsers = loginUsers;

export {loginUsers as loginUsers};
