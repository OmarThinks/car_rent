var handleFailure = (response) =>
{
  console.log("handle failure");
  digestErrorResponse(response)
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
  console.log(responseBody);

  const toReturn = {};
  responseBody.map(errorObject => {

    console.log(errorObject);
    let errorLocation = errorObject.loc[0];
    let errorMessage = errorObject.msg;
    console.log(errorLocation);
    console.log(errorMessage);
    //console.log(errorObject.loc[0]);
    //console.log(errorObject.msg);
    //return({location: errorLocation, message: errorMessage})
    toReturn[errorLocation] = errorMessage;
  })
    //return((errorObject))
  console.log(toReturn);
  return toReturn;
}

export { handleFailure as handleFailure}
