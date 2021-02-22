import {Component} from "react";
import {loginUsers} from "../server_requests/users.js";
import {handleFailure} from "../functions/handleForm.js";
import {setCookie, eraseCookie} from "../functions/cookies.js";
//import { TextField } from '@material-ui/core';
import { TextField, InputAdornment, IconButton } from "@material-ui/core";
import VisibilityIcon from '@material-ui/icons/Visibility';
import VisibilityOffIcon from '@material-ui/icons/VisibilityOff';
import { Button } from '@material-ui/core';


const logOut = (props) =>{
  eraseCookie();
  //console.log(props);
  props.appComponent.setState({loggedIn:false});
}



class Login extends Component {

  state = {
    username:"",
    password:"",
    showPassword:false,
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


    changePasswordShow(e){
      this.setState({showPassword:!this.state.showPassword});
    }

    render = () =>{
      //console.log("google");
      if (this.props.appComponent.state.loggedIn == true)
      {
        return(
      <div>      
<Button variant="contained" color="secondary" size="large" onClick={(e)=>{logOut(this.props)}}>
  Log Out
</Button>
      </div>
        )
      }

      let usernameError = false;
      let passwordError = false;
      if (this.state.errors.username != "") 
        {usernameError = true ;}
      if (this.state.errors.password != "") 
        {passwordError = true ;}

      let passwordType="password";
      if(this.state.showPassword==true)
        {passwordType="text";}

      return(
<div>

        <form  onSubmit={(e)=>{this.handleSubmit(e)}} noValidate >
      <TextField id="username" label="Username" variant="outlined" error={usernameError} 
          helperText={this.state.errors.username} required={true}
           margin="normal" defaultValue="" fullWidth={true}
           onChange={(e)=>{this.handleChange(e)}}/>
      <TextField id="password" type={passwordType} label="Password" variant="outlined" error={passwordError} 
          helperText={this.state.errors.password} required={true}
          margin="normal" defaultValue="" fullWidth={true}
          onChange={(e)=>{this.handleChange(e)}}
          InputProps={{ // <-- This is where the toggle button is added.
    endAdornment: (
      <InputAdornment position="end">
        <IconButton
          aria-label="toggle password visibility"
          onClick={(e)=>{this.changePasswordShow()}}
          //onMouseDown={handleMouseDownPassword}
        //}
        >
          {this.state.showPassword ? <VisibilityIcon /> : <VisibilityOffIcon />}
        </IconButton>
      </InputAdornment>
    )
  }}
          />

<Button type="submit" variant="contained" color="primary" size="large">
  Login
</Button>
      </form>
</div>
        )
    }
}

export default Login;
