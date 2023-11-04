Used to gather Linkedin jobs in a sheet.  

# How to use
Git clone this repository. In the folder, set the python version (>3.7):
```
pyenv local 3.9.10
```
Create and initiate a python env :
```
python -m venv .venv
source .venv/bin/activate
```

Install requirements:
```
pip install -r requirements.txt
```

In your browser, access linkedin.com, login into your account, open the browser console (F12), and go to the 'Application' tab. In the 'Storage' section, click on 'Cookies', then 'www.linkedin.com' and copy the value of 'li_at'.

Set the li_at env variable. For example, in zsh:
```
export LI_AT_COOKIE=<copied li_at here>
```

Run main.py, passing the LinkedIn query:
```
python main.py 'software AND rust'
```
