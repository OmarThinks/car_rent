import {Component} from "react";

class Login extends Component {

  state = {
    userName:"",
    password:""
  }
    render = () =>{
      return(
          <form>
            <input type="text"></input>
          </form>
        )
    }
}

export default Login;
