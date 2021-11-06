# ECE-470
Introduction to Robotics. Boom, lets automate someone's job.

Some things to think about when taking this course:
  1. Linear Algebra is hard
  2. Python is Hard
  3. Robots are not hard

Some things to think about for ECE 470 Robotics:
  1. Go to Lab to do all your work
  2. You will be using the UR3 and Gazebo Robotic Simulator
  
LAB SETUP
=================================
Take my reference from Lab 2, which will help out a lot

*Creating a workspace in Commands Terminal*

    mkdir -p catkin_rbalita2/src  // creates src folder for workspace
    cd catkin_rbalita2/src        // directs to folder created
    catkin_init_workspace         // makes this folder the src folder, and creates the build and devel folders in your workspace
    
*Building the workspace. Always do in Command Terminal*
    
    cd ~/catkin_rbalita2/
    Catkin_make					// build workspace

*After compilation is complete, I can now launch ROS commands. Open Gazebo*
    
    cd catkin_rbalita2/src/ur3_driver 	      // directs to ur3_driver folder
    Roslaunch ur3_driver ur3_gazebo.launch 	// this should open gazebo

    CTRL + SHIFT + N					// opens new tab
    source devel/setup.bash				// do this every time you open a new tab to use tabs


*Make your execute file executable*
    
    Cd ~  							// cd to main
    Cd catkin_rbalita2/src/lab2andDrivers/scripts   // direct to scripts of lab
    chmod +x lab2_exec.py 					// makes the lab2_exec file executable


*See your robot move*
    
    Cd ~ 								  // cd to main
    Cd catkin_rbalita2/src/lab2andDrivers 		  // direct to lab folder

    Rosrun lab2pkg_py lab2_exec.py					// For Gazebo 
    Rosrun lab2pkg_py lab2_exec.py --simulator True		// For simulation
    Rosrun lab2pkg_py lab2_exec.py --simulator False		// Run it on Hardware





