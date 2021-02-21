import {Component} from "react";
import {loginUsers} from "../server_requests/users.js";
import {handleFailure} from "../functions/handleForm.js";


class Login extends Component {

  state = {
    username:"",
    password:"",
    errors:
    {
      username:"u test",
      password:"p test"
    }
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
    //console.log("username is : " + username.toString());
    //console.log("password is : " + password.toString());

    loginUsers(username,password)
    .then((data)=>{//console.log(data);
      console.log("success");})
    .catch((response) => {handleFailure(response,this);
      })
    }


    render = () =>{
      return(
        <form onSubmit={(e)=>{this.handleSubmit(e)}}>
          Username
          <span className="red_text">*
          </span> : <input type="text" id="username"
          onChange={(e)=>{this.handleChange(e)}}></input>
        <div className="red_text">{this.state.errors.username}</div>
      <br/>
          Password<span className="red_text">*</span> : <input
           type="text" id="password"
          onChange={(e)=>{this.handleChange(e)}}></input>
        <span className="red_text">{this.state.errors.password}</span>
      <br/>
        <button type="submit"> Login </button>
        </form>
        )
    }
}

export default Login;
