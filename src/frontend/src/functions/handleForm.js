var handleFailure = (response,parentObject) =>
{
  //console.log("handle failure");
  let errorCleaned = digestErrorResponse(response);
  //console.log(errorCleaned);
  //console.log(parentObject.state);
  let newErrors = {};
  for(let property in parentObject.state.errors)
  {newErrors[property] = "";}
  //console.log(newErrors);
  /*newErrors now looks like this:
    {username:"",password:""}
  */
  for(let property in errorCleaned)
  {newErrors[property] = errorCleaned[property];}
  //console.log(newErrors);
  parentObject.setState({errors:newErrors})
}



/*
digestErrorResponse
INPUTS:
  - response: the response of the error itself
  - NOTE: It predicts a pydantic like mistake
FUNCTION:
  - digest this error response and return a clean dictionary
OUTPUT:
  - A clean dictionary of the places of the errors
  - Example:
    {
      username: "short username",
      password: "lohn password"
    }
*/
var digestErrorResponse = (response) =>
{
  let responseBody = response.response.data.validation_error.body_params;
  //console.log(responseBody);
  const toReturn = {};
  responseBody.map(errorObject => {
    //console.log(errorObject);
    let errorLocation = errorObject.loc[0];
    let errorMessage = errorObject.msg;
    //console.log(errorLocation);
    //console.log(errorMessage);
    toReturn[errorLocation] = errorMessage;
  })
  //console.log(toReturn);
  return toReturn;
}

export { handleFailure as handleFailure}
