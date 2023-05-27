# Find !t  

A Complete Job Search / Job Recommendation systems created  using Django, SQL Database, Scikit-Learn.

## Demo 
Sign Up page 
<hr>
![Demo](https://raw.githubusercontent.com/arkalsekar/Find-it/main/demo/6.PNG)
<br>

Login Page
<hr>
![Demo](https://raw.githubusercontent.com/arkalsekar/Find-it/main/demo/7.PNG)
<br>

Home page 
<hr>
![Demo](https://raw.githubusercontent.com/arkalsekar/Find-it/main/demo/1.PNG)
<br>

Profile Page 
<hr>
![Demo](https://raw.githubusercontent.com/arkalsekar/Find-it/main/demo/2.PNG)
<br>

Relevant Jobs Page 
<hr>
![Demo](https://raw.githubusercontent.com/arkalsekar/Find-it/main/demo/3.PNG)
<br> 

Search Jobs Page 
<hr>
![Demo](https://raw.githubusercontent.com/arkalsekar/Find-it/main/demo/4.PNG)
<br> 

Search Based on Tags Page 
<hr>
![Demo](https://raw.githubusercontent.com/arkalsekar/Find-it/main/demo/5.PNG)
<br> 


## Characteristics

Here are the Features of the Application.
</br>
1. Users can Sign Up.
2. Users can Login.
3. Users can fill their Profile.
4. Based on their Profiles Jobs will be displaced to them on the ```/relevant ``` page.
5. Users can Logout.
6. Admin Users can add more Jobs.

## Setting Up

Clone or Download the this repository and store it on your machine. 
```bash
git clone https://github.com/arkalsekar/Find-it.git
```

## Usage
Once Downloaded or Cloned the Repository, Run the following Commands

```bash
pip install -r requirements.txt
```
Once Installed all the requirements. Run the Following Commands.
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
This is isin't necessary but with this you would be able to login to the website.
```bash
python manage.py createsuperuser
```
This command will finally run the server on localhost://8000
```bash
python manage.py runserver
```
Now head on to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) and access the site.


## License
[MIT](https://choosealicense.com/licenses/mit/)
