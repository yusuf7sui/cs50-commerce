# CS50 - Commerce

The project is an online auction website created as a personal educational exercise. 
It's based on [CS50W Project 2: Commerce](https://cs50.harvard.edu/web/projects/2/commerce/), from Harvard's CS50 course *Web Programming with Python and JavaScript*. The base code was downloaded from [commerce.zip](https://cdn.cs50.net/web/2020/spring/projects/2/commerce.zip) provided by CS50.

## Installation
1. Download Python Version 3.10.0: 
https://www.python.org/downloads/release/python-3100/

**Note:** Newer versions might also work, but have not been tested. 

2. Install the necessary packages:
```
pip install django markdown2
```

**Note:** On Linux and MacOS use the command:
```
pip3 install django markdown2
```

## Usage
1. Change working directory:
```
cd commerce
```

2. Run database migrations:
```
python manage.py migrate 
```

3. Start the development server:
```
python manage.py runserver
```

4. After starting the server, open the following URL on the browser:
http://localhost:8000

## Features
This project fulfills all core requirements from the [CS50W Project 2: Commerce Specification](https://cs50.harvard.edu/web/projects/2/commerce/#specification):

- User authentication (register, login, logout)
- Create auction listings with:
  - Title, description, starting bid
  - Image URL and category
- Active listings overview page (default homepage)
- Detailed listing page with:
  - Current highest bid
  - Add/remove from personal watchlist
  - Place new bids (only if valid)
  - Close auction (if listing creator)
  - Add comments
- Watchlist page for signed-in users
- Category browsing:
  - View all categories
  - View active listings per category
- Django admin interface for managing listings, bids, and comments
- Winner announcement on closed listings
