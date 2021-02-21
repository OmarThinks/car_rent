import {Component} from "react";
import {eraseCookie} from "../functions/cookies.js";

const logOut = () =>{
  eraseCookie();

}


const Navbar = (props) => {

    const loggedIn = props.appComponent.state.loggedIn;
    if(loggedIn==true){
      return (
        <div>
        <button onClick={()=>{logOut()}}>Log Out</button>
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
