import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import os

class VideoPlayerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Learn About Desktop Controller")
        self.master.configure(bg='#101010')

        icon = Image.open("./images/favicon.png")
        self.master.iconphoto(True, ImageTk.PhotoImage(icon))

        # Maximize the window
        self.master.state('zoomed')

        # Get screen dimensions
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()

        # Set video canvas dimensions
        self.video_width = self.screen_width
        self.video_height = self.screen_height

        # Create a Canvas widget to display the video
        self.video_canvas = tk.Canvas(self.master, bg="#101010", bd=0, highlightthickness=0, width=self.video_width, height=self.video_height)
        self.video_canvas.grid(row=0, column=1, sticky=tk.NSEW)

        # Create a Text widget for the description label
        self.description_label = tk.Text(self.master, font=("Helvetica", 12), fg="#FFFFFF", bg="#101010", wrap=tk.WORD)
        self.description_label.grid(row=1, column=1, sticky=tk.NSEW)

        initial_text = "\n\nWelcome to Learn About of Desktop Controller. \n\n\n\n\nGetting Confused? No Worries! Take charge with our quick 30-second gesture \n\ntutorials. These tutorials walk you through the proper techniques for each \n\ngesture, ensuring clarity and understanding. Just choose the gesture you're \n\nuncertain about from the options available, and let us guide you step by step."
        self.display_info(initial_text)

        # Menu bar frame for buttons
        self.menu_frame = tk.Frame(self.master, bg="#333333")

        # Back button
        back_img = Image.open("./images/back_button.png")  # Assuming you have a back_button.png image
        back_img = back_img.resize((40, 40))
        self.back_photo = ImageTk.PhotoImage(back_img)
        self.back_btn = tk.Button(self.menu_frame, image=self.back_photo, bg="#333333", activebackground="#555555", bd=0, relief=tk.FLAT, command=self.go_back)
        self.back_btn.pack(fill=tk.X, padx=10, pady=8)

        buttons_info = [
            ("  Palm Recognition", "demo_media/palm.mp4", 1270, 608, "  Palm Recognition\n  No action will perform or the cursor will stop moving when all the five fingers are up."),
            ("  Cursor Movement", "demo_media/cursor.mp4", 1270, 608, "  Cursor Movement\n  When both index and middle fingers are up."),
            ("  Left Click", "demo_media/leftclick.mp4", 1270, 608, "  Left Click\n  Lower the index finger and raise the middle finger."),
            ("  Right Click", "demo_media/rightclick.mp4", 1270, 608, "  Right Click\n  Lower the middle finger and raise the index finger."),
            ("  Double Click", "demo_media/doubleclick.mp4", 1270, 608, "  Double Click\n  Join both index finger and middle finger then double click action perform."),
            ("  Scrolling", "demo_media/scrolling.mp4", 1270, 608, "  Scrolling\n  In the left hand, make a pinch of the index finger and thumb and raise all the rest of the fingers and \n  then move your hand vertically and horizontally."),
            ("  Multiple Item Selection", "demo_media/multipleselection.mp4", 1270, 608, "  Multiple Item Selection\n  Select multiple items with ease."),
            ("  Volume Control", "demo_media/volumecontrol.mp4", 1270, 608, "  Volume Control\n  In the right hand, make a pinch of the index finger and thumb and raise all the rest of the fingers and \n  move your hand vertically."),
            ("  Brightness Control", "demo_media/brightnesscontrol.mp4", 1270, 608, "  Brightness Control\n  In the right hand, make a pinch of the index finger and thumb and raise all the rest of the fingers and \n  move your hand horizontally."),
            ("  Drag and Drop", "demo_media/draganddrop.mp4", 1270, 608, "  Drag and Drop\n  Lower all the fingers after selecting the element then drag the element and drop it wherever you want."),
            #("  Voice Command", "demo_media/test2.mp4", 1270, 608, "  Voice Command\n  Control your desktop using voice commands."),
            ]
        
        self.buttons = []
        self.selected_button = None   # To keep track of the selected button
        for btn_text, btn_video_path, btn_width, btn_height, btn_description in buttons_info:
            button = tk.Button(self.menu_frame, text=btn_text, font=("Helvetica", 14, "bold"), fg="#00FF00", bg="#333333", activebackground="#00FF00", activeforeground="#333333", bd=0, relief=tk.FLAT, command=lambda video_path=btn_video_path, width=btn_width, height=btn_height, description=btn_description: self.select_button(video_path, width, height, description))
            button.pack(fill=tk.X, padx=10, pady=8)
            button.bind("<Enter>", lambda event, button=button: self.on_hover(event, button))
            button.bind("<Leave>", lambda event, button=button: self.on_leave(event, button))
            self.buttons.append(button)

        # Position the menu frame at the top-left corner
        self.menu_frame.grid(row=0, column=0, sticky=tk.NW)

        self.current_video = None

        # Bind the close_window() function to the window closing event
        self.master.protocol("WM_DELETE_WINDOW", self.on_window_close)

    def display_info(self, info_text):
        # Display informational text on the video canvas
        self.video_canvas.delete("all")  # Clear previous content
        
        # Calculate the x and y coordinates for the image and text
        text_x = self.video_width/8  # Center the text
        y_position = 70  # Set the y-coordinate for both the image and text
                
        # Display the informational text
        # Display the informational text with different font sizes for each line
        lines = info_text.split("\n")
        font_sizes = [32, 32, 32,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,18,16,20,20,20]  # Define the font sizes for each line
        y = y_position
        for i, line in enumerate(lines):
            self.video_canvas.create_text(text_x, y, text=line, fill="#39FF14", font=("Helvetica", font_sizes[i]), anchor=tk.NW)
            y += font_sizes[i] + 5  # Adjust vertical spacing between lines
            
    def play_video(self, video_path, video_width=None, video_height=None, description=""):
        # Stop the current video if it's playing
        if self.current_video:
            self.current_video.release()

        cap = cv2.VideoCapture(video_path)

        if video_width is None:
            video_width = self.video_width
        if video_height is None:
            video_height = self.video_height

        fps = cap.get(cv2.CAP_PROP_FPS)

        # Function to update the video frame
        def update_frame():
            start_time = cv2.getTickCount()
            ret, frame = cap.read()
            if ret:
                # Convert the frame to RGB format
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Resize frame
                resized_frame = cv2.resize(rgb_frame, (video_width, video_height))

                # Convert the frame to ImageTk format
                image = Image.fromarray(resized_frame)
                photo = ImageTk.PhotoImage(image=image)

                self.video_canvas.config(width=video_width, height=video_height)
                self.video_canvas.create_image(0, 0, anchor=tk.NW, image=photo)
                self.video_canvas.image = photo
                time_taken = cv2.getTickCount() - start_time
                delay = max(1, int((1.0 / fps - time_taken / cv2.getTickFrequency()) * 1000))
                self.master.after(delay, update_frame)
            else:
                # Rewind and play the video again
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.master.after(30, update_frame)

        # Start the video playback
        update_frame()
        self.current_video = cap

    def select_button(self, video_path, video_width, video_height, description):
        # Play the selected video
        self.play_video(video_path, video_width, video_height, description)

        # Split the description into a heading and a sentence
        if "\n" in description:
            heading, sentence = description.split("\n", 1)
        else:
            heading = description
            sentence = ""

        # Format the description label with a larger and bolder heading
        heading_text = f"{heading}\n"
        formatted_text = f"{heading_text}{sentence}"
    
        self.description_label.config(font=("Helvetica", 20))
        self.description_label.delete(1.0, tk.END)  # Clear previous content
        self.description_label.insert(tk.END, formatted_text)

        # Unhighlight previously selected button
        if self.selected_button:
            self.selected_button.config(bg="#333333", fg="#00FF00")

        # Highlight the selected button
        for button in self.buttons:
            button_text = button["text"]
            if button_text == description.split('\n')[0]:
                button.config(bg="#00FF00", fg="#333333")
                self.selected_button = button

    def go_back(self):
        # Close the current window
        self.master.destroy()
        # Run the previous Python file
        os.system('python main.py')

    def on_hover(self, event, button):
        button.config(bg="#555555", fg="#FFFFFF")

    def on_leave(self, event, button):
        if button != self.selected_button:
            # Check if the button is currently highlighted, and if so, maintain the highlight color
            if button['bg'] == "#00FF00":
                button.config(bg="#00FF00", fg="#333333")
            else:
                button.config(bg="#333333", fg="#00FF00")
        else:
            button.config(bg="#00FF00", fg="#333333")

    def on_window_close(self):
        # Display a confirmation dialog when attempting to close the window
        confirm_close = messagebox.askyesno("Exit Desktop Controller", "Are you sure you want to exit Learn About?")
        if confirm_close:
            self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayerApp(root)
    root.mainloop()
