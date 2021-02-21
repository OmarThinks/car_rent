import {Component} from "react";

class Login extends Component {

  state = {
    username:"",
    password:""
  }

  handleChange = (e) =>{
    this.setState({
      [e.target.id]:e.target.value
    })
  }
    render = () =>{
      return(

        <form>
          Username: <input type="text" id="username"
          onChange={(e)=>{this.handleChange(e)}}></input><br/>
          Password: <input type="text" id="password"
          onChange={(e)=>{this.handleChange(e)}}></input><br/>
        <button type="submit"> Login </button>
        </form>
        )
    }
}

export default Login;
