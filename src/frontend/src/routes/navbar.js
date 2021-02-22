import {Component} from "react";
import {eraseCookie} from "../functions/cookies.js";

const logOut = (props) =>{
  eraseCookie();
  //console.log(props);
  props.appComponent.setState({loggedIn:false});
}


const Navbar = (props) => {

    const loggedIn = props.appComponent.state.loggedIn;
    if(loggedIn==true){
      return (
        <div>
        <button onClick={(e)=>{logOut(props)}}>Log Out</button>
        </div>
      )
    }
    return (
      <div>
      <button>Login</button>
      </div>
    )
}

export default Navbar;
