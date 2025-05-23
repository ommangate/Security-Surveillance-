# import cv2
# import os
# import serial
# import smtplib
# from datetime import datetime
# from email.message import EmailMessage
# import threading

# # ========== EMAIL CONFIGURATION ==========
# EMAIL_SENDER = 'mangateom4@gmail.com'
# EMAIL_PASSWORD = 'mchz xtdf gurm fwxr'
# EMAIL_RECEIVER = 'javafuklkstackdeveloper22@gmail.com'

# def send_email_alert(image_path):
#     def email_thread():
#         try:
#             msg = EmailMessage()
#             msg.set_charset('utf-8')  # Force UTF-8 encoding

#             msg['Subject'] = 'Face Detected Alert'
#             msg['From'] = EMAIL_SENDER
#             msg['To'] = EMAIL_RECEIVER
#             msg.set_content('A face was detected. See attached image.', charset='utf-8')

#             # Use basename and encode filename safely
#             filename = os.path.basename(image_path)
#             with open(image_path, 'rb') as f:
#                 img_data = f.read()
#                 msg.add_attachment(img_data, maintype='image', subtype='jpeg', filename=filename)

#             with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
#                 smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
#                 smtp.send_message(msg)
#             print(f"✅ Email sent: {filename}")
#         except Exception as e:
#             print(f"❌ Email failed: {e}")

#     threading.Thread(target=email_thread).start()


# # ========== SERIAL + CAMERA SETUP ==========
# arduino = serial.Serial('/dev/cu.usbmodem101', 9600)  # Update port if needed
# print("Connected to Arduino")

# base_dir = os.getcwd()
# haar_cascade_path = os.path.join(base_dir, 'haarcascade_frontalface_default.xml')
# captures_dir = os.path.join(base_dir, 'captures')
# video_dir = os.path.join(base_dir, 'Video')

# os.makedirs(captures_dir, exist_ok=True)
# os.makedirs(video_dir, exist_ok=True)

# face_cascade = cv2.CascadeClassifier(haar_cascade_path)
# cap = cv2.VideoCapture(0)
# if not cap.isOpened():
#     print("Error: Could not open camera.")
#     exit()

# frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# fps = 20.0

# status = "IDLE"
# out = None

# # ========== MAIN LOOP ==========
# while True:
#     if arduino.in_waiting:
#         line = arduino.readline().decode().strip()
#         print("Arduino:", line)

#         if line == "CAPTURE" and status != "CAPTURING":
#             print("Switching to photo capture mode")
#             if out:
#                 out.release()
#                 out = None
#             status = "CAPTURING"

#         elif line == "CLEAR" and status != "RECORDING":
#             print("Resuming video recording")
#             video_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.mp4'
#             video_path = os.path.join(video_dir, video_filename)

#             fourcc = cv2.VideoWriter_fourcc(*'avc1')  # H.264 codec for macOS
#             out = cv2.VideoWriter(video_path, fourcc, fps, (frame_width, frame_height))

#             if not out.isOpened():
#                 print("Error: Failed to open video writer.")
#             else:
#                 print("Recording to:", video_filename)

#             status = "RECORDING"

#     ret, frame = cap.read()
#     if not ret:
#         print("Error: Failed to read from camera.")
#         break

#     if status == "RECORDING" and out:
#         out.write(frame)

#     elif status == "CAPTURING":
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = face_cascade.detectMultiScale(gray, 1.3, 5)

#         for (x, y, w, h) in faces:
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

#         if len(faces) > 0:
#             img_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.jpg'
#             img_path = os.path.join(captures_dir, img_name)
#             cv2.imwrite(img_path, frame)
#             print("📸 Face captured:", img_name)
#             send_email_alert(img_path)
#             status = "IDLE"

#     cv2.imshow('Surveillance', frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         print("Quitting...")
#         break

# # ========== CLEANUP ==========
# cap.release()
# if out:
#     out.release()
# cv2.destroyAllWindows()



import cv2
import os
import serial
import smtplib
from datetime import datetime
from email.message import EmailMessage
import threading

# ========== EMAIL CONFIGURATION ==========
EMAIL_SENDER = 'mangateom4@gmail.com'
EMAIL_PASSWORD = 'mchz xtdf gurm fwxr'
EMAIL_RECEIVER = 'harshwardhanp101@gmail.com'

def send_email_alert(image_path):
    def email_thread():
        try:
            msg = EmailMessage()
            msg.set_charset('utf-8')  # Force UTF-8 encoding

            msg['Subject'] = 'Face Detected Alert'
            msg['From'] = EMAIL_SENDER
            msg['To'] = EMAIL_RECEIVER
            msg.set_content('A face was detected. See attached image.', charset='utf-8')

            filename = os.path.basename(image_path)
            with open(image_path, 'rb') as f:
                img_data = f.read()
                msg.add_attachment(img_data, maintype='image', subtype='jpeg', filename=filename)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
                smtp.send_message(msg)
            print(f"✅ Email sent: {filename}")
        except Exception as e:
            print(f"❌ Email failed: {e}")

    threading.Thread(target=email_thread, daemon=True).start()


# ========== SERIAL + CAMERA SETUP ==========
arduino = serial.Serial('/dev/cu.usbmodem101', 9600)  # Update port if needed
print("Connected to Arduino")

base_dir = os.getcwd()
haar_cascade_path = os.path.join(base_dir, 'haarcascade_frontalface_default.xml')
captures_dir = os.path.join(base_dir, 'captures')
video_dir = os.path.join(base_dir, 'Video')

os.makedirs(captures_dir, exist_ok=True)
os.makedirs(video_dir, exist_ok=True)

face_cascade = cv2.CascadeClassifier(haar_cascade_path)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = 20.0

status = "IDLE"
out = None

# ========== MAIN LOOP ==========
while True:
    if arduino.in_waiting:
        line = arduino.readline().decode().strip()
        print("Arduino:", line)

        if line == "CAPTURE" and status != "CAPTURING":
            print("Switching to photo capture mode")
            if out:
                out.release()
                out = None
            status = "CAPTURING"

        elif line == "CLEAR" and status != "RECORDING":
            print("Resuming video recording")
            video_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.mp4'
            video_path = os.path.join(video_dir, video_filename)

            fourcc = cv2.VideoWriter_fourcc(*'avc1')  # H.264 codec for macOS
            out = cv2.VideoWriter(video_path, fourcc, fps, (frame_width, frame_height))

            if not out.isOpened():
                print("Error: Failed to open video writer.")
            else:
                print("Recording to:", video_filename)

            status = "RECORDING"

    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to read from camera.")
        break

    if status == "RECORDING" and out:
        out.write(frame)

    elif status == "CAPTURING":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        if len(faces) > 0:
            img_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.jpg'
            img_path = os.path.join(captures_dir, img_name)
            cv2.imwrite(img_path, frame)
            print("📸 Face captured:", img_name)
            send_email_alert(img_path)
            status = "IDLE"

    cv2.imshow('Surveillance', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Quitting...")
        break

# ========== CLEANUP ==========
cap.release()
if out:
    out.release()
cv2.destroyAllWindows()
