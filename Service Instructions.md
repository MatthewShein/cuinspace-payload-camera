# Instructions

Managing a Camera Script Service with systemd on Raspbian
This guide explains how to navigate to the systemd service directory, control (start, enable, stop, disable) a camera script service named camera_script.service.

1. Accessing the systemd Service Directory:

   Open a terminal window. You can do this by clicking on the terminal icon or searching for "terminal" in the applications menu.

   `cd /etc/systemd/system`  
   
   Press Enter to execute the command. This will change your terminal's working directory to /etc/systemd/system. This is where systemd service files are typically stored.
  
2. Starting the Camera Script Service:

    To start your camera script service manually, use the following command:

    `sudo systemctl start camera_script.service`  

3. Enabling the Camera Script Service:

   To make the camera script service start automatically on boot, use the following command:

   `sudo systemctl enable camera_script.service`  

   This tells systemd to include your service when starting the Raspberry Pi.
  
4. Stopping the Camera Script Service:

   If you need to stop the script temporarily, use this command:

   `sudo systemctl stop camera_script.service`

   This will halt the script's execution, but it will still be configured to start on boot.
   
5. Disabling the Camera Script Service:

   To prevent the camera script service from starting automatically on boot, use the following command:

   `sudo systemctl disable camera_script.service`

   This disables the service but doesn't affect its current execution (if already running).

6. Check Status of Service

   To check to see if the script is running or not, use the following command:

   `sudo systemctl status camera_script.service`

   This shows if the service is Active or Inactive 
