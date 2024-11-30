# Animal Tracker Application

This is a Python application designed to track the location of an animal in real-time using data retrieved from an Arduino server. It displays the animal's location on a Google Map using Google Maps API and alerts you if the animal goes outside a designated safe zone.

**Demo Video:**


## System Requirements

* **Operating System:** Windows (tested with Windows 10)
* **Recommended Screen Size:** Maximum 16 inches
* **Python:** Version 3.8 or later
* **Development Environment:** Visual Studio 2022 (2019 may work, but not guaranteed)

## Installation and Setup

1. **Download the application:**
   - Download the application archive (e.g., ZIP file).

2. **Extract the files:**
   - Extract the downloaded archive to a new directory on your computer.

3. **Open the Solution:**
   - Open the provided solution file named `AnimalTracker.sln` using Visual Studio 2022.

4. **Enable Solution Explorer (Optional):**
   - If the Solution Explorer isn't already visible on the right side of the Visual Studio window, go to the **View** menu and select **Solution Explorer**. This helps you navigate the project files.

5. **Create Virtual Environment (Optional):**
   - Visual Studio may prompt you to create a virtual environment for the project.
     - If prompted, select "Create" and accept the default settings.
   - This virtual environment automatically installs all required project dependencies.

6. **Run the Application:**
   - Once the virtual environment is created (or if you choose not to create one), click the "Run" button (typically a green play button) on the Debug toolbar in Visual Studio.

## Using the Application

**1. Sign Up:**

   - Enter your email address for future login and password resets.
   - Create a secure password.
   - You will be prompted to define a safe zone for your animal. The application provides default coordinates for the VGU Campus safe zone (you can modify these):
      - Latitude: 11.107301
      - Longitude: 106.613331
      - Radius (meters): 200
   - Click "Continue" to complete your registration.

**2. Log In:**

   - Enter the email address you used during registration.
   - Enter your corresponding password.

**3. Reset Password (if needed):**

   - Click "Forgot Password?".
   - Enter the registered email address.
   - Check your email inbox for a Reset Code sent from `animaltrackergroup2@gmail.com`.
   - Enter the received code in the designated field.
   - Click "Reset password" to update your password and return to the Log-in page.

**4. Homepage:**

   - The homepage displays the following features:
      - **Log Out:** Button to log out of your account (located on the left-hand side).
      - **About Us:** Button providing information about the application (located on the left-hand side).
      - **Embedded Google Map:** This map shows the real-time location of your tracked animal as a red marker. The map updates as the animal moves, displaying a red path to indicate its movement.
      - **Safe Zone Alerts (Right-hand side):** If the animal's location goes outside the predefined safe zone, an alert will appear here. The newest alert will be displayed on top.

**5. Reset Safe Zone (if needed):**

   - Enter your registered email address.
   - Define new coordinates for the updated safe zone (you can use the following example):
      - Latitude: 11.108781
      - Longitude: 106.611521
      - Radius (meters): 200
   - Click "Continue" to save the changes and return to the Homepage with the updated safe zone boundaries.

## License
[this is just a repo for testing only]
