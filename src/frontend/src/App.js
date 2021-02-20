import './App.css';
import axios from 'axios';
import $ from "jquery";
import {Component} from "react";
import {Navbar} from "./components/navbar";

class App extends Component {

state = {logged_in:true};

changeLoggedIn = (newState) =>{
  this.setState(
    {logged_in:newState}
  );
}


render = () => {

  return (
    <div className="App">
      <p>{this.state.logged_in.toString()}</p>
      <Navbar logged_in={this.state.logged_in} />
    </div>
  );}
}

export default App;
