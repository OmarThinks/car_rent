import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import $ from "jquery";
function App() {







//$.support.cors = true;


/*
  var settings = {
    "url": "http://127.0.0.1:5000/users/login/test",
    "method": "POST",
    "timeout": 0,
    "Access-Control-Expose-Headers": "Authorization"
  };

  $.ajax(settings).done(function (response) {
    console.log(response);
  });

*/





/*
  var myHeaders = new Headers();

  var requestOptions = {
    method: 'POST',
    redirect: 'follow'
  };

  fetch("http://127.0.0.1:5000/users/login/test", requestOptions)
    .then(response => response)
    .then(result => console.log(result))
    .catch(error => console.log('error', error));
*/










/*
var myHeaders = new Headers();
myHeaders.append("Cookie", "cantiin=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjEsImV4cCI6MTYxNDIzNTgwMS4xMjYwMTJ9.I-MSjISBeHUOG1HjYkfPP26VfrZIj8KlJ3w79C3KcVc");

var requestOptions = {
  method: 'POST',
  headers: myHeaders,
  redirect: 'follow'
};

fetch("http://127.0.0.1:5000/users/login/test", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
*/


/*

const https = require('https')

const data = JSON.stringify({
  todo: 'Buy the milk'
})

const options = {
  hostname: '127.0.0.1',
  port: 5000,
  path: '/users/login/test',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  }
}

const req = https.request(options, res => {
  console.log(`statusCode: ${res.statusCode}`)

  /*res.on('data', d => {
    process.stdout.write(d)
  })*/
/*  console.log(res);
})

req.on('error', error => {
  console.error(error)
})

//req.write(data)
req.end()

*/










var axios = require('axios');

var config = {
  withCredentials: true,
  method: 'post',

  proxy: {
    protocol: 'http',
    host: '127.0.0.1',
    port: 5000,
    auth: {
      username: 'mikeymike',
      password: 'rapunz3l'
    }
  },
  url: 'http://127.0.0.1:5000/users/login/test',
  "Access-Control-Allow-Headers": "*", // this will allow all CORS requests
  "Access-Control-Allow-Methods": 'OPTIONS,POST,GET', // this states the allowed methods
  //'Access-Control-Allow-Origin': 'http://127.0.0.1:5000',
  "Access-Control-Expose-Headers": "*",
  headers: {
    //'Cookie': 'cantiin=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjEsImV4cCI6MTYxNDIzNTgwMS4xMjYwMTJ9.I-MSjISBeHUOG1HjYkfPP26VfrZIj8KlJ3w79C3KcVc',
    //'Authorization': 'cantiin=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjEsImV4cCI6MTYxNDIzNTgwMS4xMjYwMTJ9.I-MSjISBeHUOG1HjYkfPP26VfrZIj8KlJ3w79C3KcVc'
    'Access-Control-Allow-Origin': "http://127.0.0.1:5000",
    "Access-Control-Allow-Headers": "*", // this will allow all CORS requests
    "Access-Control-Allow-Methods": 'OPTIONS,POST,GET' // this states the allowed methods
    //"Access-Control-Expose-Headers": "*",
  }
};

axios(config)
.then(function (response) {
  console.log(response);
  //console.log(JSON.stringify(response.data));
})
.catch(function (error) {
  console.log(error);
});

/*
axios({
  method: 'post',
  url: 'http://127.0.0.1:5000/users/login/test',
  //crossDomain: true,
  //headers: {'Authorizat': 'XMLHttpRequest'},
  //withCredentials: true,
  "Access-Control-Allow-Origin": "http://127.0.0.1:5000/users/login/test",
  headers: {
    //"Access-Control-Allow-Headers": "*", // this will allow all CORS requests
     // this will allow all CORS requests
    //"Access-Control-Allow-Methods": 'OPTIONS,POST,GET', // this states the allowed methods
    //"Content-Type": "application/json" // this shows the expected content type
    'Access-Control-Allow-Origin': '*',
              'Content-Type': 'application/json',
              'Authorization': "",
              withCredentials: true,
              mode: 'no-cors',
},
})
.then(function (response) {
    console.log(response);
    console.log("Made it");
  })
.catch(function (error){
  console.log("Something went wrong")
});
*/

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
