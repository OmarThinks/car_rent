import {Component} from "react";

class Navbar extends Component {

  render = () => {
    const logged_in = this.props.logged_in;
    if(logged_in){
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
  }
}

export default Navbar;
