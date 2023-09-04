# Capstone Project
# Autonomous Plant Watering System Senior Design

Faculty Mentor: TBD

Team Members: Javier Padilla, Alexis Torres, Ian Skillman, Kiet Le, Evan LeBel, Jesus Hernandez, Jaime Sanchez

Project Description:
Due to changes in the weather and busy work weeks, it can be challenging to keep track of when you last watered your plants. Our Watering System will automate the need to keep track of the last time you watered your plants and give you more time to enjoy seeing your plants grow. This can create longevity in plants including flowers and plants that can feed humans for years to come. 
Specifically, the project will focus on a single unit that contains a small to medium-sized plant. Attached to the unit will be multiple sensors that will detect/measure/record moisture, temperature, humidity, sunlight, and the water level of an in-unit source. Using a Web UI, the user will be able to manually control and set custom watering settings for the unit. 

Team Composition
4 software engineers developing the software that will use algorithms to automate the watering system based on conditions received from the sensors. All of which can be monitored and manually activated on a remote Web UI. 
3 embedded systems engineers working on communication between sensors and microcontroller, as well as any drivers necessary for the attached LCD display or features that are going to be added. Adding additional electronics to power the microcontroller (including a battery pack and solar cell)



Objectives
Embedded Systems Development: Efficient and reliable embedded systems that control hardware components and devices.
Firmware and Software Development: Creating software and firmware to control and interact with hardware components, creating communication with full functionality.
Networking and Communication: Designing systems that can communicate with each other using various communication protocols (TCP or UDP), such as Wi-Fi or Bluetooth.
Test and Validation: Develop test plans and methodologies to ensure that the designed systems and components meet performance and reliability requirements.
Usability and User Experience: Design software interfaces that are user-friendly experience for end-users.
Scalability and Performance: Build software that can handle increased user loads and data info while maintaining optimal performance.
Compatibility: Develop software that is compatible with multiple devices, operating systems, and browsers, to ensure consistent user experience across platforms.
Code Reviews: Collaborative code reviews to maintain code quality, pass knowledge, and resolve code-related issues.
Documentation: Create comprehensive documentation to outline software functionality, architecture, APIs, and usage guidelines.
Data Management: Design a robust data management system to ensure data integrity for software data storage and processing.
Teams
Embedded Systems Team:

Members: Ian Skillman, Evan LeBel, and Jaime Sanchez
Subsystems: Plant Microcontroller, Hub, Wireless, PCB Design
Roles: Firmware/Software, PCB Designer, Hardware Test/Validation, RF, Power, and Data Packet design
Members: 
Ian     - Sensors communication and plant Micro and Water Mechanics
	Evan  - Plant info and Water Mechanics/System Designer/HUB Master/PCB design
	Jaime - Communications/PCB design
Team Timeline:
Checkpoint 1: APIs - TBD
Checkpoint 2: Plant Microcontroller  - TBD
Checkpoint 3: Hub Microcontroller - TBD
Checkpoint 4: Plant-Hub Communication - TBD 
Checkpoint 5: Water Mechanics Design  - TBD
Checkpoint 6: Custom PCB Schematics - TBD 
Checkpoint 7: Final Casing/Housing - TBD



Design Idea:
A plant module will have 3 attached sensors: Light, moisture, and temperature. These sensors will communicate with a custom PCB where the microcontroller will be located. Each plant will have its own sensors and microcontroller, but can also be expanded to accommodate multiple plants per microcontroller. The microcontroller will periodically read the sensors and, based on the sensor data, enable or disable a water pump that delivers water into the plant's soil. The water flow will be fixed, with the amount of water released determined by a time-based factor. The water pump will be connected to a water tank equipped with a sensor to monitor the water level within the tank. This sensor will communicate with the hub, which will be responsible for broadcasting notifications regarding the need to refill the tank. Each microcontroller will communicate with the hub via Bluetooth to periodically send current sensor readings from the plants. The hub can receive multiple data packets from various microcontrollers. Bluetooth will utilize the TCP protocol to prevent interference. The hub will then relay the received data packets over Wi-Fi to be accessed by the PC user for reading and analysis.

Demonstrations of multiple Plant modules per tank/HUB


Software Team: Web Development

Members: Alexis Torres, Kiet Le, Javier Padilla, and Jesus Hernandez
Subsystems: Server / UI - Backend/Front End
Roles:
	Front End Dev: Alexis Torres and Javier Padilla
	Backend Dev: Kiet Le and Jesus Hernandez
Description:
The software team's primary responsibility involves developing the web application, which serves as the user interface for the project. This entails creating a comprehensive, full-stack application capable of storing both user and plant data. Additionally, the software team will manage the critical communication link between the user and the microcontroller.

To ensure a seamless user experience, the team will focus on crafting an intuitive and user-friendly interface, accompanied by an aesthetically pleasing user interface design.

Requirements: 
User Friendly UI
Dark/Light Mode
Language Setting
English
Spanish
Etc.
Account System
Admin Level Control
System Customization
Manual Control
Adding and Configuring Plant Profile
Standard User Level
Monitoring 
Monitoring
Graphical Sensor Data Display
Water Level
Light Detection
Moisture Level
Etc.
System Settings Customization
Custom Plant Profiles
Water Needs
Lights Needs
Data Transmission Rate
New Plant Integration
History
Saving Packets Received from the system
Maintaining History of Notification Events / System Events
Notifications 
SMS
Email
Upscale:
App Development:
Convert the web app into a mobile app that can be accessed on both IOS and Android. 
System Design Draft:
<INPUT PROJECT NAME>
Project Description: <NEEDS WORK>

Team Composition
4 software engineers developing the software that will use algorithms to automate the watering system based on conditions received from the sensors. All of which can be monitored and manually activated on a remote Web UI. 
3 embedded systems engineers working on communication between sensors and microcontroller, as well as any drivers necessary for the attached LCD display or features that are going to be added. Adding additional electronics to power the microcontroller (including a battery pack and solar cell)
Objectives <Fill in Data>
Teams
Embedded Systems Team: <NEED WORK>

Members: Ian Skillman, Evan LeBel, and Jaime Sanchez
Subsystems: Plant Microcontroller, Hub, Wireless, PCB Design
Roles: Firmware/Software, PCB Designer, Hardware Test/Validation, RF, Power, and Data Packet design
Members: 
Ian     - 
	Evan  - 
	Jaime - 
Team Timeline:
Software Team: Web Development

Members: Alexis Torres, Kiet Le, Javier Padilla, and Jesus Hernandez
Subsystems: Server / UI - Backend/Front End
Roles:
	Front End Dev: Alexis Torres and Javier Padilla
	Backend Dev: Kiet Le and Jesus Hernandez
Description:
The software team's primary responsibility involves developing the web application, which shall function as a tool for doctors to monitor patient’s health. This entails creating a comprehensive, full-stack application capable of storing both user and sensor data. Additionally, the software team will manage the critical communication link between the user and the microcontroller. 

To ensure a seamless user experience, the team will focus on crafting an intuitive and user-friendly interface, accompanied by an aesthetically pleasing user interface design.


The goal is to set a framework for health monitoring, where more wearable devices can interface with the web application.  

Requirements: 
User Friendly UI
Dark/Light Mode
Language Setting
English
Spanish
Etc.
Account System
Admin/ Doctor Level Control
System Customization
Manual Control
Adding and Configuring Patient Profile
Standard User Level
Monitoring their own device data
Monitoring
Graphical Sensor Data Display


Etc.
System Settings Customization
Data Transmission Rate
New device integration
History
Saving Packets Received from the system
Maintaining History of Notification Events / System Events
Notifications 
SMS
Email

Upscale:
App Development:
Convert the web app into a mobile app that can be accessed on both IOS and Android. 
Interface for health monitoring wearable devices

System Design Draft:
