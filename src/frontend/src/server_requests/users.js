import axios from 'axios';


function loginUsers(username,password){
  return axios({
  method: 'post',
  url: host+'/users/login',
  data: {
    username: username,
    password: password
  }
});
}
