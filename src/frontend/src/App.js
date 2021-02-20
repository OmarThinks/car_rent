import './App.css';
import axios from 'axios';
import $ from "jquery";
import {Component} from "react";


class App extends Component {

state = {logged_in:true};


render = () => {



  return (
    <div className="App">
      <p>{this.state.logged_in.toString()}</p>
    </div>
  );}
}

export default App;
