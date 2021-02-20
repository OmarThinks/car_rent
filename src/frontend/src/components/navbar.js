import {Component} from "react";

const Navbar = (props) => {

  //render = () => {
    const logged_in = props.appState.logged_in;
    if(logged_in==true){
      return (
        <div>
          <p>The user is logged in</p>
        </div>
      )
    }
    return (
      <div>
        <p>The user is not logged in</p>
      </div>
    )
  //}
}

export default Navbar;
