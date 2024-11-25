#importing critical libraries for Fluorospot counter GUI
import tkinter as tk
from tkinter import ttk
import webbrowser
import cv2
import numpy as np
import PIL.Image, PIL.ImageTk
from tkinter import filedialog as fd
import os
import pandas as pd
import pandastable as pdt




#creating the main window
master_window = tk.Tk()
master_window.title("Spot Counter")
master_window.iconbitmap("C:/Programming/Fluorospot_counter/A1.ico")

main_frame = tk.Frame(master_window)
main_frame.pack()

frame_ops = tk.Frame(master_window, background="#cccccc")
frame_ops.place(x =0, y = 0, relwidth = 0.2, relheight = 1)

scroll_canvas = tk.Canvas(master_window, background = "#bfbfbf")
scroll_canvas.place(relx = 0.2, y = 0, relwidth = 0.8, relheight = 0.6)

v_scrollbar = tk.Scrollbar(master_window, orient=tk.VERTICAL, command=scroll_canvas.yview)
v_scrollbar.place(relx=0.994, rely=0, relheight=0.6)
h_scrollbar = tk.Scrollbar(master_window, orient=tk.HORIZONTAL, command=scroll_canvas.xview)
h_scrollbar.place(relx=0.2, rely=0.593, relwidth=0.90)

frame_img = tk.Frame(scroll_canvas, background="red")
frame_img.bind(
        "<Configure>",
        lambda e: scroll_canvas.configure(
            scrollregion=scroll_canvas.bbox("all")
        )
    )

scroll_canvas.create_window((0, 0), window=frame_img, anchor="nw")

#frame_img.place(relx = 0.1, y = 0, relwidth = 0.9, relheight = 0.6)

frame_pandas = tk.Frame(master_window, background="#A9A5A5")
frame_pandas.place(relx = 0.2, rely = 0.6, relwidth = 0.9, relheight = 0.4)

# telling the program to always open fullscreen
master_window.state("zoomed")
master_window.resizable(True, True)
master_window.configure(background = "black")



images = []
img_name = []
img_ref = []
img_keypoints = []
number_of_spots = []


#creating a class for the menu bar
class menuBar(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid()
        self.menu_widget()
        

    #creating different menu widgets
    def menu_widget(self):
        #defining topbar menu
        topBar = tk.Menu(main_frame)
        #first drop-down menu
        firstMenu = tk.Menu(topBar, tearoff=0)
        firstMenu.add_command(label="Open File(s):", command=open_files)
        firstMenu.add_command(label="Exit", command=main_frame.quit)
        topBar.add_cascade(label="File", menu=firstMenu)
        #second drop-down menu
        secondMenu = tk.Menu(topBar, tearoff=0)
        secondMenu.add_command(label="Count Spots:", command=update_count_spots)
        topBar.add_cascade(label="Processing", menu=secondMenu)
        #third drop-down menu
        thirdMenu = tk.Menu(topBar, tearoff=0)
        thirdMenu.add_command(label="Instructions", command= lambda: webbrowser.open("https://github.com/DarkDoomofSol/FluorSpot_Counter/blob/main/README.md"))
        topBar.add_cascade(label="Help", menu=thirdMenu)
                           
        #forming menues
        master_window.config(menu = topBar)

#creating a class for the left Frame functions window  
class oper_wind(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid(sticky= "nw")
        self.file_list()

    def file_list(self):

        global file_listbox, min_area_var, min_circ_var, min_conv_var, min_inertia_var, min_thresh_var, max_thresh_var, min_dist_var, min_repeat_var

        list_label = tk.Label(frame_ops, text = "List of Loaded files:")
        list_label.grid(column=2, row=0, padx=10, pady=(50, 0), columnspan=2)       
        file_listbox = tk.Listbox(frame_ops)
        file_listbox.grid(column=2, row=1, padx=10, pady=5, columnspan=2)
        
        add_file_button = tk.Button(frame_ops, text = "Add file(s):", command = open_files)
        add_file_button.grid(column=2, row=2, padx=10, pady=5, columnspan=1)

        remove_file_button = tk.Button(frame_ops, text = "Clear file(s):", command = clear_file)
        remove_file_button.grid(column=3, row=2, padx=10, pady=5, columnspan=1)

        filt_min_area_Label = tk.Label(frame_ops, text = "Filter by min area:")
        filt_min_area_Label.grid(column=2, row=3, padx=5, pady=(10, 0), columnspan=2)
        min_area_var = tk.DoubleVar(value=10.0)
        min_area_spinbox = tk.Spinbox(frame_ops, from_=0, to=1000, textvariable = min_area_var, justify= "center", command = lambda: update_count_spots())
        min_area_spinbox.grid(column=2, row=4, padx=10, pady=(0, 10), columnspan=2)

        filt_min_circ_Label = tk.Label(frame_ops, text = "Filter by min circularity:")
        filt_min_circ_Label.grid(column=2, row=5, padx=5, pady=(10, 0), columnspan=2)
        min_circ_var = tk.DoubleVar(value=0.01)
        min_circ_spinbox = tk.Spinbox(frame_ops, from_=0, to=1, textvariable = min_circ_var, justify= "center", format = "%.2f", increment = 0.01, command = lambda: update_count_spots())
        min_circ_spinbox.grid(column=2, row=6, padx=10, pady=(0, 10), columnspan=2)

        filt_min_convex_Label = tk.Label(frame_ops, text = "Filter by min convexity:")
        filt_min_convex_Label.grid(column=2, row=7, padx=5, pady=(10, 0), columnspan=2)
        min_conv_var = tk.DoubleVar(value=0.01)
        min_conv_spinbox = tk.Spinbox(frame_ops, from_=0, to=1, textvariable = min_conv_var, justify= "center", format = "%.2f", increment = 0.01, command = lambda: update_count_spots())
        min_conv_spinbox.grid(column=2, row=8, padx=10, pady=(0, 10), columnspan=2)

        filt_min_inertia_Label = tk.Label(frame_ops, text = "Filter by min inertia:")
        filt_min_inertia_Label.grid(column=2, row=9, padx=5, pady=(10, 0), columnspan=2)
        min_inertia_var = tk.DoubleVar(value=0.01)
        min_inertia_spinbox = tk.Spinbox(frame_ops, from_=0, to=1, textvariable = min_inertia_var, justify= "center", format = "%.2f", increment = 0.01, command = lambda: update_count_spots())
        min_inertia_spinbox.grid(column=2, row=10, padx=10, pady=(0, 10), columnspan=2)

        filt_min_dist_Label = tk.Label(frame_ops, text = "Filter by min distance between blobs:")
        filt_min_dist_Label.grid(column=2, row=11, padx=5, pady=(10, 0), columnspan=2)
        min_dist_var = tk.DoubleVar(value=1)
        min_dist_spinbox = tk.Spinbox(frame_ops, from_=1, to=100, textvariable = min_dist_var, justify= "center", increment = 1, command = lambda: update_count_spots())
        min_dist_spinbox.grid(column=2, row=12, padx=10, pady=(0, 10), columnspan=2)

        filt_min_thresh_Label = tk.Label(frame_ops, text = "Filter by min threshhold:")
        filt_min_thresh_Label.grid(column=2, row=13, padx=5, pady=(10, 0), columnspan=1)
        min_thresh_var = tk.DoubleVar(value=10.0)
        min_thresh_spinbox = tk.Spinbox(frame_ops, from_=0, to=200000, textvariable = min_thresh_var, justify= "center", increment = 1, command = lambda: update_count_spots())
        min_thresh_spinbox.grid(column=2, row=14, padx=10, pady=(0, 10), columnspan=1)

        filt_max_thresh_Label = tk.Label(frame_ops, text = "Filter by max threshold:")
        filt_max_thresh_Label.grid(column=3, row=13, padx=5, pady=(10, 0), columnspan=1)
        max_thresh_var = tk.DoubleVar(value=20000.0)
        max_thresh_spinbox = tk.Spinbox(frame_ops, from_=0, to=200000, textvariable = max_thresh_var, justify= "center", command = lambda: update_count_spots())
        max_thresh_spinbox.grid(column=3, row=14, padx=10, pady=(0, 10), columnspan=1)

        filt_threshstep_Label = tk.Label(frame_ops, text = "Filter by thresholdstep:")
        filt_threshstep_Label.grid(column=2, row=15, padx=5, pady=(10, 0), columnspan=2)
        threshstep_var = tk.DoubleVar(value=2)
        threshstep_spinbox = tk.Spinbox(frame_ops, from_=1, to=10, textvariable = threshstep_var, justify= "center", command = lambda: update_count_spots())
        threshstep_spinbox.grid(column=2, row=16, padx=10, pady=(0, 10), columnspan=2)

        filt_min_repeat_Label = tk.Label(frame_ops, text = "Filter by min repeatability:")
        filt_min_repeat_Label.grid(column=2, row=17, padx=5, pady=(10, 0), columnspan=2)
        min_repeat_var = tk.IntVar(value=2)
        min_repeat_spinbox = tk.Spinbox(frame_ops, from_=1, to=10, textvariable = min_repeat_var, justify= "center", command = lambda: update_count_spots())
        min_repeat_spinbox.grid(column=2, row=18, padx=10, pady=(0, 10), columnspan=2)


        count_spots_button = tk.Button(frame_ops, text = "Count Spots:", command = counting_spots)
        count_spots_button.grid(column=2, row=19, padx=10, pady=20, columnspan=2)

#create a button for opening multiple files and storing them in a list
def open_files():
    global img_gray
    file_path = fd.askopenfilenames(title = "Select the images to be analyzed", filetypes=(("All Files", "*.*"),))
    for file_path in file_path:
        if file_path in opened_files:
            continue
        filename = os.path.basename(file_path)
        file_listbox.insert(tk.END, filename)
        img_name.append(filename)    
        img = cv2.imread(file_path)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        images.append(img_gray)
        # Add file path to the set of opened files
        opened_files.add(file_path)
        
    global img_canvas
    global img_label
    global img_tk
    
    max_columns = 12
    img_height, img_width = images[0].shape[:2]  # Assuming all images have same dimensions

    # Create canvas and display each image
    for i, (img, filename) in enumerate(zip(images, img_name)):
        img_tk = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(img))
        img_ref.append(img_tk)  # Append to the list to keep a reference

        row = i // max_columns
        column = i % max_columns

        # Create a canvas for each image
        img_canvas = tk.Canvas(frame_img, width=img_width, height=img_height)
        img_canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        img_canvas.grid(column=column, row=row *2 + 1, padx=10, pady=10)  # Use 'i' for columns

        # Create a label for each image
        img_label = tk.Label(frame_img, text= filename)
        img_label.grid(column=column, row=row * 2, padx=10, pady=10)
                
            
opened_files = set()


#creating a function to clear the file list and images
def clear_file():
    
    for widget in frame_img.winfo_children():
        widget.destroy()
    
    file_listbox.delete(0, tk.END)
    opened_files.clear()
    del images[:]
    del img_ref[:]
    del img_keypoints[:]
    return images if images else None

def update_count_spots():

    params = cv2.SimpleBlobDetector_Params()

    params.filterByColor = False            #dont need it since using only 8-bit grayscale
    
    params.filterByArea = True
    params.minArea = min_area_var.get()
    #params.maxArea = max_area

    params.filterByCircularity = False
    params.minCircularity = min_circ_var.get()
    #params.maxCircularity = max_circ

    params.filterByConvexity = False
    params.minConvexity = min_conv_var.get()
    #params.maxConvexity = max_convex

    params.filterByInertia = False
    params.minInertiaRatio = min_inertia_var.get()
    #params.maxInertiaRatio = max_inertia

    params.minThreshold = min_thresh_var.get()
    params.maxThreshold = max_thresh_var.get()

    params.minDistBetweenBlobs = min_dist_var.get()

    params.minRepeatability = min_repeat_var.get()

    detector = cv2.SimpleBlobDetector_create(params)

    img_keypoints.clear()
    img_ref.clear()

    for img in images:

        keypoints = detector.detect(img)
        img_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (255,0,0), cv2.DrawMatchesFlags_DRAW_RICH_KEYPOINTS)
        img_keypoints.append(img_with_keypoints)

    refresh_image_display()

def counting_spots():
    global df
    params = cv2.SimpleBlobDetector_Params()

    params.filterByColor = False            #dont need it since using only 8-bit grayscale
    
    params.filterByArea = True
    params.minArea = min_area_var.get()
    #params.maxArea = max_area

    params.filterByCircularity = False
    params.minCircularity = min_circ_var.get()
    #params.maxCircularity = max_circ

    params.filterByConvexity = False
    params.minConvexity = min_conv_var.get()
    #params.maxConvexity = max_convex

    params.filterByInertia = False
    params.minInertiaRatio = min_inertia_var.get()
    #params.maxInertiaRatio = max_inertia

    params.minThreshold = min_thresh_var.get()
    params.maxThreshold = max_thresh_var.get()

    params.minDistBetweenBlobs = min_dist_var.get()

    params.minRepeatability = min_repeat_var.get()

    detector = cv2.SimpleBlobDetector_create(params)

    img_keypoints.clear()
    img_ref.clear()

    for img in images:

        keypoints = detector.detect(img)
        img_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (255,0,0), cv2.DrawMatchesFlags_DRAW_RICH_KEYPOINTS)
        img_keypoints.append(img_with_keypoints)
        num_blobs = len(keypoints)

        number_of_spots.append(num_blobs)
    
    df = pd.DataFrame({"Image Name": img_name, "Spot Count": number_of_spots})

      

    refresh_image_display()
    refresh_pandas_display()

def refresh_image_display():

    for widget in frame_img.winfo_children():
        widget.destroy()

    max_columns = 12
    img_height, img_width = images[0].shape[:2]  # Assuming all images have same dimensions

    # Create canvas and display each image
    for i, (img, filename) in enumerate(zip(img_keypoints, img_name)):
        img_tk = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(img))
        img_ref.append(img_tk)  # Append to the list to keep a reference

        row = i // max_columns
        column = i % max_columns

        # Create a canvas for each image
        img_canvas = tk.Canvas(frame_img, width=img_width, height=img_height)
        img_canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        img_canvas.grid(column=column, row=row *2 + 1, padx=10, pady=10)  # Use 'i' for columns

        # Create a label for each image
        img_label = tk.Label(frame_img, text= filename)
        img_label.grid(column=column, row=row * 2, padx=10, pady=10)

def refresh_pandas_display():
    for widget in frame_pandas.winfo_children():
        widget.destroy()
    table = pdt.Table(frame_pandas, dataframe=df)
    table.show()
    

# creating a class for the right frame functions window to display images
class img_wind(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid(sticky= "nw")
        #self.display_img()
    

# creating a class to handle the pandas data frame
class pandas_wind(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid(sticky= "nw")
        #self.display_pandas()

    #def display_pandas(self):
        #df = pd.DataFrame()
        #df = pdt.Table(frame_pandas, dataframe=df)
        #df.show()
        

app = menuBar(main_frame)
app = oper_wind(frame_ops)
app = img_wind(frame_img)
app = pandas_wind(frame_pandas)


master_window.mainloop()
# end of mainloop   



