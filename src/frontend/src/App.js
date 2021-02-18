import logo from './logo.svg';
import './App.css';
const axios = require('axios').default;

function App() {


axios({
  method: 'post',
  url: 'http://127.0.0.1:5000/users/login/test',
  crossDomain: true
})
.then(function (response) {
    console.log(response);
    console.log("Made it");
  })
.catch(function (error){
  console.log("Something went wrong")
});


  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
