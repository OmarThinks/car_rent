import {Component} from "react";
import {loginUsers} from "../server_requests/users.js";
import {handleFailure} from "../functions/handleForm.js";
import {setCookie, eraseCookie} from "../functions/cookies.js";
import { TextField } from '@material-ui/core';


const logOut = (props) =>{
  eraseCookie();
  //console.log(props);
  props.appComponent.setState({loggedIn:false});
}



class Login extends Component {

  state = {
    username:"",
    password:"",
    errors:
    {
      username:"",
      password:""
    }
  }

  handleChange = (e) =>{
    //console.log(e.target.id);
    //console.log(typeof(e.target.id));
    let location = "errors." + e.target.id.toString();
    var errors = {...this.state.errors}
    errors[e.target.id] = "";
    this.setState({
      [e.target.id]:e.target.value,
      errors
    })
    //console.log(this.state);
  }

  handleSubmit = (e) => {
    e.preventDefault();
    let username = this.state.username;
    let password = this.state.password;
    //console.log("username is : " + username.toString());
    //console.log("password is : " + password.toString());

    loginUsers(username,password)
    .then((data)=>{
      //console.log(data);
      let authHeader = data.headers.authorization;
      //console.log(authHeader);
      //console.log("success");
      setCookie(authHeader, 7);
    this.props.appComponent.setState({loggedIn:true});
    })
    .catch((response) => {handleFailure(response,this);
      })
    }


    render = () =>{
      //console.log("google");
      if (this.props.appComponent.state.loggedIn == true)
      {
        return(
      <div>
        <button onClick={(e)=>{logOut(this.props)}}>Log Out</button>
      </div>
        )
      }

      let usernameError = false;
      let passwordError = false;
      if (this.state.errors.username != "") 
        {usernameError = true ;}
      if (this.state.errors.password != "") 
        {passwordError = true ;}
      return(
<div>

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
  <div>
    <form>
      <TextField id="username" label="Username" variant="outlined" error={usernameError} 
          helperText={this.state.errors.username} required={true}/>
      <TextField id="ppassword" label="Password" variant="outlined" error={passwordError} 
          helperText={this.state.errors.password} required={true}/>
    </form>
  </div>
</div>
        )
    }
}

export default Login;
