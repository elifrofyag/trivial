Group 2 - Animal Tracker Application

Our demo video also shows how to setup and use our application visually. 

===================================
Getting things running 

Recommended device screen size of maximum 16 inches.

In order to run our application, these 2 must be installed: 
- Python 3.8 or later
- Visual Studio 2022 (2019 may work but we cannot guarantee)

To run the application:
1. Extract the archive to a new directory
2. Open the solution file "AnimalTracker.sln" 
3. Click "View" on the top Tool bar to open the Solution Explorer on the right-hand side to view all the files in this directory.
4. Visual Studio should prompt you to create a virtual environment. Create one with default settings
5. If you are using Python 3.12 and VS warns you about being not officially supported, ignore the warning
6. Creating the virtual environment will automatically install all required dependencies. Once complete, run the program using the run button on the debug toolbar on top of VS. 


===================================
Using the application

1. Sign up:
- Enter your email that you will be using when you want to change the password or sign in.
- Enter your password.
- You will be asked to enter the coordinates of the safe zone that you want your animal to be inside. You can enter the coordinates of the safe zone (VGU Campus) we provide below:
	- Latitude: 11.107301
	- Longitude: 106.613331
	- Radius (meters): 200
- Click "Continue" to confirm your registration

2. Log in:
- Enter the email that you already signed up with
- Enter the corresponding password.

3. Reset Password:
- Click "Forgot Password?" to reset your password
- Enter the email that you signed up with
- Check your email inbox for the Reset Code sent by animaltrackergroup2@gmail.com
- Enter the code into the box as requested
- Click "Reset password" to change your password and return to Log-in Page.

4. Homepage:
- On the left-hand side, there are "Log out" and "About us" buttons if you need these functions.
- In the middle is an embedded Google Map that shows the real-time location of your tracked animal (red marker) retrieved from the dataset downloaded from Arduino Server. Whenever your animal moves, there will be a red line showing their route.
- If the GPS of the animal's location is outside of the preset safe zone, an alert on the right-hand side will be prompted. The newest alert will stay on top of the previous ones.

5. Reset Safe Zone:
- Enter your email
- Enter new coordinates for the new safe zone. You can use the following:
	- Latitude: 11.108781
	- Longitude: 106.611521
	- Radius (meters): 200 
- Click "Continue" to save changes and return to the Hompage with the updated safe zone.

