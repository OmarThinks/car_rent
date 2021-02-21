import {Component} from "react";
import {loginUsers} from "../server_requests/users.js";
class Login extends Component {

  state = {
    username:"",
    password:""
  }

  handleChange = (e) =>{
    this.setState({
      [e.target.id]:e.target.value
    })
  }

  handleSubmit = (e) => {
    e.preventDefault();
    let username = this.state.username;
    let password = this.state.password;
    console.log("username is : " + username.toString());
    console.log("password is : " + password.toString());

    loginUsers(username,password)
    .then((data)=>{console.log(data);})
    .catch((failure) => {console.log(failure.response);})
  }
    render = () =>{
      return(
        <form onSubmit={(e)=>{this.handleSubmit(e)}}>
          Username: <input type="text" id="username"
          onChange={(e)=>{this.handleChange(e)}}></input><br/>
          Password: <input type="text" id="password"
          onChange={(e)=>{this.handleChange(e)}}></input><br/>
        <button type="submit"> Login </button>
        </form>
        )
    }
}

export default Login;