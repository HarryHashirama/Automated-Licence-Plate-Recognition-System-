import cv2 
import numpy as np 
import sqlite3 
# Connect to SQLite database 
conn = 
sqlite3.connect('number_plates.db')cursor 
= conn.cursor() 
# Create a table to store number plate 
valuescursor.execute(''' 
CREATE TABLE IF NOT EXISTS number_plates ( 
id INTEGER PRIMARY KEY AUTOINCREMENT, 
plate_text TEXT)''') 
conn.commit() 
# Load the pre-trained Haarcascades for license plate detection 
plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 
'haarcascade_russian_plate_number.xml') 
# Function to process the frame and detect number plates 
def process_frame(frame): 
gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.2, 
minNeighbors=5, minSize=(100, 25)) 
36 
for (x, y, w, h) in plates: 
plate_roi = gray[y:y + h, x:x + w] 
plate_text = "DemoPlate" 
# Replace this with the actual OCR implementation 
# Display the number plate 
cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) 
cv2.putText(frame, plate_text, (x, y - 10), 
cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2) 
# Store the number plate in the database 
cursor.execute('INSERT INTO number_plates (plate_text) VALUES (?)', 
(plate_text,)) 
conn.commit() 
return frame 
# Open the webcam 
cap = 
cv2.VideoCapture(0)while 
True: 
ret, frame = cap.read() 
if not ret: 
print("Error reading from webcam") 
break 
# Process the frame and display the result 
processed_frame = process_frame(frame) 
37 
cv2.imshow('Number Plate Detection', processed_frame)# 
Break the loop when 'q' is pressed 
if cv2.waitKey(1) & 0xFF == ord('q'): 
Break 
# Release the webcam and close the database connection 
cap.release() 
cv2.destroyAllWindows() 
conn.close()