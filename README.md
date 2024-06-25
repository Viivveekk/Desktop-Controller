# <img src="images/favicon.png" alt="Logo" width="30" height="30"> DESKTOP CONTROLLER

We designed and implemented finger tracking based on a virtual mouse application using a regular webcam. Furthermore, we integrated a speech-to-text converter. While touchscreen technology is popular in mobile devices, it is costly for desktop systems. Therefore, we explored computer vision techniques as an alternative method to create a virtual human-computer interaction device, such as a mouse using a webcam and voice commands using a mic.

## <img src="images/favicon.png" alt="Logo" width="30" height="30"> PROPOSED SYSTEM
![Design](images/proposed_system.png)

## <img src="images/favicon.png" alt="Logo" width="30" height="30"> System Software & Hardware Requirements
**1. IDLE:-** Python version 3.8 and above.

**2. OS:-** Windows 8 and above.

**3. RAM:-** 4GB and above.

**4. WEBCAM:-** An Web is necessary for input. 

{ If webcam not available then you can use third party application like **[DroidCam](https://droidcam.en.softonic.com/)** or any other that can help you to use your mobile cam. But this DroidCam application should be installed in both android and pc devices for usage. }

**4. MICROPHONE**

## <img src="images/favicon.png" alt="Logo" width="30" height="30"> Installation

For better Working Create an Virtual Environment.
1. Navigate to Your Project Directory:

   ```bash
   cd path/to/your/project
   ```
2. Create a Virtual Environment:

   You can use the venv module that comes with Python:

   ```bash
   python -m venv venv
   ```
3. Activate the Virtual Environment:
   
   ```bash
   .\venv\Scripts\activate
   ```
4. Install Requirements:

   ```bash
   pip install -r requirements.txt 
   ```

5. Run the main.py file:

   ```bash
   python main.py
   ```
## <img src="images/favicon.png" alt="Logo" width="30" height="30"> Demonstrated Pics

1. **Right Click**

   ![](images/rc.png)

2. **Multiple Selection**

   ![](images/ms.png)

3. **Brightness Control**

   ![](images/bc.png)

4. **Double Click**

   ![](images/dc.png)


## <img src="images/favicon.png" alt="Logo" width="30" height="30"> Additional Work In the Project

Additionally, we have developed a feature to control the mouse using a mobile device's screen. When the user selects "Mobile Controller," a QR code is displayed on the screen. Scanning this code directs the user to a browser page where they can control the mouse by dragging their finger on the page. However, for this to work, both the PC and the mobile device must be on the same network.

<p float="left">
  <img src="images/QR.png" alt="Image 1" width="500" />
  <img src="images/browserpage.jpg" alt="Image 2" width="200" /> 
</p> 

## <img src="images/favicon.png" alt="Logo" width="30" height="30"> Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## <img src="images/favicon.png" alt="Logo" width="30" height="30"> License

[MIT](LICENSE) Licensed 
