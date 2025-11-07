<img src="https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2FViivveekk%2FDesktop-Controller&label=visitors&countColor=%23263759&style=flat" alt="Visitor Badge" width="150"/>

# <img src="images/favicon.png" alt="Logo" width="30" height="30"> DESKTOP CONTROLLER

We designed and implemented finger tracking based on a virtual mouse application using a regular webcam. Furthermore, we integrated a speech-to-text converter. While touchscreen technology is popular in mobile devices, it is costly for desktop systems. Therefore, we explored computer vision techniques as an alternative method to create a virtual human-computer interaction device, such as a mouse using a webcam and voice commands using a mic.

## <img src="images/favicon.png" alt="Logo" width="30" height="20"> Maths Used for Virtualization of Mouse

The mathematical concepts used to designed for a gesture-based desktop control system using a webcam and the MediaPipe library. Below are the essential mathematical concepts and formulas used in this system:

1. **Distance Calculations:**
   - **Euclidean Distance:**
     To find the distance between two points \((x1, y1)\) and \((x2, y2)\) on a 2D plane, the following formula is used:
     ```
     distance = sqrt((x2 - x1)^2 + (y2 - y1)^2)
     ```
     This calculates the straight-line distance between the points.

     Code :-

     ```
     dist = (self.hand_result.landmark[point[0]].x - self.hand_result.landmark[point[1]].x)**2
     dist += (self.hand_result.landmark[point[0]].y - self.hand_result.landmark[point[1]].y)**2
     dist = math.sqrt(dist)
     ```

   - **Signed Euclidean Distance:**
     The signed distance between two points considers direction and is computed as:
     ```
     signed_distance = sign * sqrt((x2 - x1)^2 + (y2 - y1)^2)
     ```
     Here, `sign` is determined by comparing the y-coordinates of the points. If the y-coordinate of the first point is less than that of the second point, `sign` is set to 1; otherwise, it is set to -1.

     Code:-

     ```
     sign = -1
     if self.hand_result.landmark[point[0]].y < self.hand_result.landmark[point[1]].y:
        sign = 1
     dist = (self.hand_result.landmark[point[0]].x - self.hand_result.landmark[point[1]].x)**2
     dist += (self.hand_result.landmark[point[0]].y - self.hand_result.landmark[point[1]].y)**2
     dist = math.sqrt(dist)
     return dist * sign
     ```

1. **Ratio Calculation:**
   - **Distance Ratio:**
     To evaluate whether a finger is open or closed, the ratio of two distances is used:
     ```
     ratio = dist1 / dist2
     ```
     In this case, `dist1` represents the distance from the fingertip to the middle knuckle, and `dist2` is the distance from the middle knuckle to the base knuckle. A ratio greater than 0.5 typically indicates an open finger.

     Code:-

     ```
     ratio = round(dist / dist2, 1)
     ```

2. **Pinch Gesture Control:**
   - **Quantified Displacement:**
     For pinch gestures, the displacement magnitude is used to adjust system settings such as volume and brightness:
     ```
     pinch_lv = current_position - start_position
     ```
     `current_position` is the hand's current position, while `start_position` is the position where the pinch gesture began. This displacement is quantified for control applications.

     Code:-

     ```
     pinchlv = round((hand_result.landmark[8].x - Controller.pinchstartxcoord) * 10, 1)
     ```

3. **Cursor Movement Stabilization:**
   - **Damping Adjustment:**
     To smooth out cursor movements and reduce jitter, a damping factor is applied:
     ```
     ratio = factor * sqrt(distance)
     ```
     where `distance` is the squared change in cursor position. Different factors are used based on the distance to stabilize movement. For example:
     ```
     ratio = 0.07 * sqrt(distance) for smaller distances
     ratio = 2.1 for larger distances
     ```

     Code:-

     ```
     distsq = delta_x**2 + delta_y**2
     ratio = 1
     if distsq <= 25:
       ratio = 0
     elif distsq <= 900:
       ratio = 0.07 * (distsq ** (1/2))
     else:
       ratio = 2.1
     x, y = x_old + delta_x * ratio, y_old + delta_y * ratio
     ```

4. **Pinch Gesture Levels:**
   - **Vertical and Horizontal Levels:**
     To assess the level of pinch gestures along different axes:
     - Vertical Pinch Level:
       ```
       pinch_ylv = pinchstart_y - current_y
       ```
       Code:-

       ```
       dist = round((Controller.pinchstartycoord - hand_result.landmark[8].y) * 10, 1)
       ```
          
     - Horizontal Pinch Level:
       ```
       pinch_xlv = current_x - pinchstart_x
       ```
     `pinchstart_x` and `pinchstart_y` are the coordinates at the start of the pinch gesture, and `current_x` and `current_y` are the current hand coordinates.

       Code:-

       ```
       dist = round((hand_result.landmark[8].x - Controller.pinchstartxcoord) * 10, 1)
       ```

These mathematical concepts and formulas enable the accurate detection and interpretation of hand gestures, allowing users to control various system functions through gestures effectively.

## <img src="images/favicon.png" alt="Logo" width="30" height="20"> PROPOSED SYSTEM
<img src="images/proposed_system.png" width="900">

## <img src="images/favicon.png" alt="Logo" width="30" height="20"> System Software & Hardware Requirements
**1. IDLE:-** Python version 3.8 and above.

**2. OS:-** Windows 8 and above.

**3. RAM:-** 4GB and above.

**4. WEBCAM:-** An Webcam is necessary for input. 

{ If webcam not available then you can use third party application like **[DroidCam](https://droidcam.en.softonic.com/)** or any other that can help you to use your mobile cam. But this DroidCam application should be installed in both android and pc devices for usage. }

**5. MICROPHONE**

## <img src="images/favicon.png" alt="Logo" width="30" height="20"> Installation

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

   { If any Python library is not installing due to **errors**, particularly if the error is related to **permissions or the location of the library**, try the following steps:

     **Open Command Prompt as Administrator:** Right-click on the Command Prompt icon and select ‘Run as Administrator’.

     **Install the Library:** Use the command pip install <library-name> to install the problematic library. }

## <img src="images/favicon.png" alt="Logo" width="30" height="20"> Demonstrated Pics

1. **Right Click**

   <img src="images/rc.png" alt="Right Click" style="width: 900px;">

2. **Multiple Selection**

   <img src="images/ms.png" alt="Multiple Selection" style="width: 900px;">

3. **Brightness Control**

   <img src="images/bc.png" alt="Brightness Control" style="width: 900px;">

4. **Double Click**

   <img src="images/dc.png" alt="Double Click" style="width: 900px;">

**For Demo Video [Click Here](https://drive.google.com/file/d/1YZv0VA10cUBe4Hj-AIBDiDsm4ATKt6gr/view?usp=sharing)**


## <img src="images/favicon.png" alt="Logo" width="30" height="20"> Additional Work In the Project

Additionally, we have developed a feature to control the mouse using a mobile device's screen. When the user selects "Mobile Controller," a QR code is displayed on the screen. Scanning this code directs the user to a browser page where they can control the mouse by dragging their finger on the page. However, for this to work, both the PC and the mobile device must be on the same network. This only has feature of left click and cursor movement.

<table>
  <tr>
    <td align="center" colspan="2">
      <img src="images/QR.png" alt="Person 1" width="900" height="600"><br>
      <sub><b>QR Code to Scan</b></sub>
    </td>
  </tr>
  <tr>
    <td align="center" colspan="2">
      <img src="images/browserpage.jpg" alt="Person 2" width="400" height="600"><br>
      <sub><b>Mobile Browser Page</b></sub>
    </td>
  </tr>
</table>


## <img src="images/favicon.png" alt="Logo" width="30" height="20"> Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## <img src="images/favicon.png" alt="Logo" width="30" height="20"> COLLABORATORS

<table border="1">
  <tr>
    <th align="center">Name</th>
    <th align="center">Email</th>
    <th align="center">Git ID</th>
  </tr>
  <tr>
    <td align="center">Vivek Kalwar</td>
    <td align="center"><a href="mailto:vivekkalwar95@gmail.com">vivekkalwar95@gmail.com</a></td>
    <td align="center"><a href="https://github.com/Viivveekk">Viivveekk</a></td>
  </tr>
  <tr>
    <td align="center">Prabel Pandey</td>
    <td align="center"><a href="mailto:prabel397@gmail.com">prabel397@gmail.com</a></td>
    <td align="center"><a href="https://github.com/HiPrabel">HiPrabel</a></td>
  </tr>
  <tr>
    <td align="center">Nadeem Khan</td>
    <td align="center"><a href="mailto:kk0078841@gmail.com">kk0078841@gmail.com</a></td>
    <td align="center"><a href="https://github.com/Luciferkhan007">Luciferkhan007</a></td>
  </tr>
</table>



## <img src="images/favicon.png" alt="Logo" width="30" height="20"> License

[MIT](LICENSE) Licensed 

## <img src="images/favicon.png" alt="Logo" width="30" height="20"> Your Support 

<a href="https://buymeacoffee.com/vivekk99"><img title="Buy us Coffee" src="https://img.shields.io/badge/Donate-BUY US COFFEE  x-blue?style=for-the-badge&logo=github"></a>
