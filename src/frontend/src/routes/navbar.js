import {Component} from "react";

const Navbar = (props) => {

    const loggedIn = props.appState.loggedIn;
    if(loggedIn==true){
      return (
        <div>
        <button>Log Out</button>
        <button>Create Account</button>
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
