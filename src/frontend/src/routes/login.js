import {Component} from "react";
import {loginUsers} from "../server_requests/users.js";
class Login extends Component {

  state = {
    username:"",
    password:"",
    usernameError:"username error",
    passwordError:"password error"
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
          Username<span className="red_text">*</span> : <input type="text" id="username"
          onChange={(e)=>{this.handleChange(e)}}></input>
        <span className="red_text">{this.state.usernameError}</span>
      <br/>
          Password<span className="red_text">*</span> : <input
           type="text" id="password"
          onChange={(e)=>{this.handleChange(e)}}></input> 
        <span className="red_text">{this.state.passwordError}</span>
      <br/>
        <button type="submit"> Login </button>
        </form>
        )
    }
}

export default Login;
