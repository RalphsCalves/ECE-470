# ECE-470
Introduction to Robotics. Boom, lets automate someone's job.
hi
Some things to think about when taking this course:
  1. Linear Algebra is hard
  2. Python is Hard
  3. Robots are Easy

Some things to think about for ECE 470 Robotics:
  1. Go to Lab to do all your work
  2. You will be using the UR3 and most probably Gazebo Robotic Simulator

# Understanding Robotics: Cheat Sheet / Course Review Sheets
Below are all of the cheat sheets I made for each of the exams

## Notes
<details> 
<summary> Click for ALL NOTES </summary>

    ### Exam 1: 
    <details> <summary> <span style="color: green"> Exam 1 </span> </summary>

    > I know its beautiful
    </details>

    ### Exam 2: 
    <details> <summary> <span style="color: green"> Exam 2 </span> </summary>

    > I know its beautiful
    </details>

</details>

# Bi-Weekly Practice: Labs
Below are all the information about the programs for the labs

## Lab Setup, and Executing the Programs using Command Line
<details> <summary> Click for LAB SETUP </summary>

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
</details>

## Lab Informations
<details> <summary> Click for ALL LABS </summary>
</details>



# Weekly Practice: Prairielearn Homeworks
Below are all the information about the programs I made for the homework

## PrairieLearn Homework 
<details>
	<summary> Click for ALL NOTES </summary>
</details>








