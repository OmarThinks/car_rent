import './App.css';
import axios from 'axios';
import $ from "jquery";
import {Component} from "react";
import Navbar from "./components/navbar";

class App extends Component {

state = {logged_in:true};

/*
This method will change the loggedin state in the app
It is expected to be boolean
true | false
*/
changeLoggedIn = (newState) =>{
  this.setState(
    {logged_in:newState}
  );
}


render = () => {

  return (
    <div className="App">
      <p>{this.state.logged_in.toString()}</p>
      <Navbar appState={this.state} />
    </div>
  );}
}

export default App;
