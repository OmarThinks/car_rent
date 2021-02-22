import './App.css';
import axios from 'axios';
import $ from "jquery";
import {Component} from "react";
import Navbar from "./routes/navbar";
import Login from "./routes/login";
import {getCookie} from "./functions/cookies.js";

class App extends Component {

state = {loggedIn:false};

/*
This method will change the loggedin state in the app
It is expected to be boolean
true | false
*/
changeLoggedIn = (newState) =>{
  this.setState(
    {loggedIn:newState}
  );
}


componentDidMount(){
  let cookie = getCookie();
  //console.log(getCookie());
  if(cookie){
    this.setState({loggedIn:true})
  }

}


render = () => {
  /*var loggedInMessage = "User is not logged in";
  if (this.state.loggedIn) {
    loggedInMessage = "User is logged in";
  }*/
  let cookieValue = getCookie();
  return (
    <div className="App">
      <Navbar appComponent={this} />
      <p>Cookie Value is: {cookieValue}</p>
      
      <Login appComponent={this}/>
    </div>
  );}
}

export default App;
