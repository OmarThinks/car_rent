# What is this directory:

This directory is create to be a remake of the `src` directory.  
The code in `src` needs to be cleaner.  

# Status:

This drectory in under construction.


# Comparison:

## 1) Validation:
I used to do the user inputs validation at each endpoint.  
Now I have discovered a package called `pydantic`.  
So I will do the validation with it.


## 2) db Models:

For each model I used to create his own CRUD functions.  
Now there will be a class carrying these methods.  
And models will inhert from it.

## 3) receiveing inputs:
I used to receive each input manually.  
Here I will use a package aclled `flask_pydantic`.  
Note: I have contributed in the documentation of this package.


