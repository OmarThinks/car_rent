# Running Cantiin #

## Python 3.7.9 : ##
This backend works using Python 3.7.9  
You can download python from this link:  
<a href="https://www.python.org/downloads/release/python-379/"
target="_blank">
Download Python</a>  
For more Information, and if you do not have python 
installed on your computer, I recommend watchng this video 
on youtube:  
<a href="https://www.youtube.com/watch?v=UvcQlPZ8ecA"
target="_blank">
Youtube: How to Install Python 3.8.2 on Windows 10</a>



## Displaying Code Using Code Editor (Not Essential) : ##
You can download any text editor.  
This is a list of the text editors, choose one:
1. **Sublime Text 3 (I use it and recommend it)**  
It is very light weight, dark interface, comfortable to your eyes.
2. Atom
3. Notepad++
4. Visual Studio Code

**NOTE**: This step is **not essential**.
To run the code you do not need a text editor, however.


## SECRET: ##
The **`SECRET`** variable is responsible for generating JWT token.  
**You Must Change The Value Of This Variable**.  
You can find it in this file

<b>

```directory
src/__init__.py
```

</b>
First line.
<b>

```python
SECRET="change me"
```

</b>

**You must give it another value, long random text.**  
For Example:  

<b>

```python
SECRET = "lkjgf697465adsuadsjknda5sdads7a8sd6asdaliuaurfjshgjdfada4sd68a7deeaWIUDIUDASJDALKSDJauhjaaAUuYUYIUHHGYTYTYSAUGHzb8547687654564DAHSDUIAWEYSAYGDWYUATWARDADAW8D7A64DS5A1DASDKJASLIUDASHDKAJSGJHASDFATWRAUJGSDHDWA6DS4A68S4687687a56d46sd4a65sd7asdalskijdalkjsdakdbhjdvasdasydaiuwywew687ew8a56ajhdakhdaasdhgahjksdgasdytayusdtasda5d6sa4d65jshdajshdausdaa"
```

</b>


## Using the command line : ##
On **Windows**, you might need to download **Gitbash**, you can
 find it in this link:  
<a href="https://git-scm.com/downloads"
target="_blank">
Download Git Bash</a>  
After installing this, you can now 
**run linux commands on windows**.  
If you don't have gitbash on your computer, or if you don't
know how to use Linux command line, I recommend that you 
watch this video on youtube:  
<a href="https://www.youtube.com/watch?v=qdwWe9COT9k"
target="_blank">
Youtube: How to Install Git Bash on Windows 10</a>



## cd into the project directory : ##
1. Using normal **Windows File Expolorer** get in the 
project directory
2. **Right click** any where
3. Select the option **Git Bash Here**
4. now **a window will open**

For more information, or if you don't know how to cd into the
project directory, I recommend watching this video on Youtube:  
<a href="https://www.youtube.com/watch?v=oQc-2gsjgDg"
target="_blank">
Youtube: Git Bash, Bash Basics</a>






## Creating virtual environment: ##
In git bash, run these commands:

<b>

```bash
pip install virtualenv
```

</b>

Create a folder called **env** inside project directory  
Then run these commands: 

<b>

```bash
virtualenv env --python=3.7.9
```

</b>

The previous command will create the virtual environment 
in the folder with the version of 3.7.9

<b>

```bash
source env/Scripts/activate
```

</b>

The previous code will run the virtual environment.


## Installing requirements : ##
After you have done cd into project directory, now run this command:  

<b>

```bash
pip install -r requirements.txt
```

</b>

For More info, i recommend watchng this video on Youtube:  
<a href="https://www.youtube.com/watch?v=empqyr7vZ8o"
target="_blank">
Youtube: Requirements.txt file for Python Projects | Install python dependencies in bulk | Data Magic</a>


## Running the project (On Local Host): ##
In git bash, run this command:

<b>

```bash
python cantiin.py
```

</b>

Now, you can in your browser, in the address bar, type this link: 
<a href="http://127.0.0.1:5000/" target="_blank">

```url
http://127.0.0.1:5000/
```

</a>
Then press Enter, Now you have it running on your browser.  
You turn the server off by pressing: 
`crtl` + `c`





## Postman testing : ##
To Test API Endpoints  
In bash run this command: 

<b>

```bash
python cantiin.py
``` 

</b>

and then run the postman collection.  
For info about how to run postman collections, 
I recommend watching this Youtube video:  
<a href="https://www.youtube.com/watch?v=t5n07Ybz7yI"
target="_blank">
Youtube: The Basics of Using Postman for API Testing</a>





## Unit Testing : ##
To test the SQLAlchemy models, and the functions.  
In bash run this command: 

<b>

```bash
python unit_tests.py
``` 

</b>

## Running the project (For Production): ##
In git bash, run this command:

<b>

```bash
python application.py
``` 

</b>

The best way to run the application for production is like that:
<b> 

```bash
export FLASK_APP=application.py
export FLASK_RUN_HOST=127.0.0.1
export FLASK_ENV=development
export FLASK_DEBUG=0
flask run
``` 

</b>