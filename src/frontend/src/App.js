import './App.css';
import axios from 'axios';
import $ from "jquery";
import {Component} from "react";
import Navbar from "./components/navbar";

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



render = () => {
  var loggedInMessage = "User is not logged in";
  if (this.state.loggedIn) {
    loggedInMessage = "User is logged in";
  }
  return (
    <div className="App">
      <Navbar appState={this.state} />
      <p>{loggedInMessage}</p>
      <button onClick={()=>{this.changeLoggedIn(true)}}>Log me in</button>
    </div>
  );}
}

export default App;
