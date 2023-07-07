# The Mollybox

#### Description:
This is a movie rating and sharing app for mollywood cinephiles where they can rate and comment on the movies they watched, share them to other users and slso get to know their ratings on movies, then add to wishlist too.

## app.py
Implements routes for the actions like login, register, add, edit, delete, display and wish. When logged in session remembers the user by storing the id as user_id. Open up app.py. Imports CS50’s SQL module and a few helper functions.After configuring Flask and Jinja  store sessions on the local filesystem and CS50’s SQL module to use project.db.
Login Notice uses db.execute (from CS50’s library) to query project.db and also uses check_password_hash to compare hashes of users’ passwords where bcrypt module is used to hash the password. Login “remembers” that a user is logged in by storing his or her user_id, an INTEGER, in session. That way, any of this file’s routes can check which user, if any, is logged in. Finally,once the user has successfully logged in, login will redirect to "/", taking the user to their home page. Meanwhile, logout simply clears session, effectively logging a user out.

Most routes are “decorated” with @login_required (a function defined in helpers.py too). That decorator ensures that, if a user tries to visit any of those routes, he or she will first be redirected to login so as to log in.
Most routes support GET and POST and messages flashed on success and failure both.

## layout.html
Contains the layout of the webpages which has the mobile friednly navigation bar, the tagline intro of the website, flask's message flashing and the background image and the blockbody.

## login.html
Contains the login page where user has to enter the username and password and login. Also has a reset button. Arises error when username/ password is incorrect by checking the database and also when user keeps any inputs blank.

## register.html
Contains the register page where user has to enter a username, password, confirm register. Also has a reset button. Arises error when password is not long enough or too much long, when passwords do not match, also when user keeps any inputs blank. Successful register, inserts user details to the database with hashed password.

## index.html
Displays the movie ratings of user by extracting from the ratings table in the database, where user can add a rating, edit or delete an existing rating.

## new.html
Contains the form to add a new rating to the user's history, which requires inputs in all the blanks.

## edit.html
Contains the editing form for an existing record similar to the new.html

## display.html
Displays all the ratings of users which can be searched and filtered, added to wishlist of the user. Additionally clicking on the movie name redirects to google searched page of the movie.

## wish.html
Displays the wishlist of the user where user can remove a wished movie once watched.

## styles.css
Contains the styles of the html file.

## custom.js
Contains the search function used in display.html

## helpers.py
login required function is added here to make sure certain routes require the user logged in.

## requirements.txt
Describes the packages onwhich the app depends on.
