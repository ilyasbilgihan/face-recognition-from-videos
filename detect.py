import cv2
import pickle
import face_recognition
from sklearn import svm


# Load trained data using svm
encodings = []
names = []
data = pickle.load(open('./trained/data.sav', 'rb'))

for person in data:
    for enc in data[person]:
        encodings.append(enc)
        names.append(person)

clf = svm.SVC(gamma='scale')
clf.fit(encodings,names)
    
    
# Input video
movie = cv2.VideoCapture("input.mp4")
length = int(movie.get(cv2.CAP_PROP_FRAME_COUNT))
k = 0


# Output video resolution
height = 480
ratio = height / movie.get(4)
width = int(movie.get(3) * ratio)


# Output video settings
fourcc = cv2.VideoWriter.fourcc(*'XVID')
output = cv2.VideoWriter('output.avi', fourcc, 60, (width, height))


# Loop through input video frames
while True:

    ret, frame = movie.read()
    
    if not ret:
        break        
    
    k += 1
    print("# {0}/{1}".format(k, length))
    
    
    # Process only every [6k+1]th frame. It means 10 times in a second for a 60fps video.
    if k%6 == 1:
        
        # Face locations for current frame
        face_locations = face_recognition.face_locations(frame)
        face_count = len(face_locations)

        if face_count > 0:
            
            # Face encodings for current frame
            faces_encodings = face_recognition.face_encodings(frame, known_face_locations=face_locations)
            prediction = [(pred, loc) for pred, loc in zip(clf.predict(faces_encodings), face_locations)]
            
    
    
    # Resize current frame to fit it into output video
    frame = cv2.resize(frame, (width, height), interpolation = cv2.INTER_AREA)
    
    
    if face_count > 0:
    
        for name, (y, w, h, x) in prediction:
            
            # Reorganize the location coordinates for resized frame.
            y = int(y * ratio)
            w = int(w * ratio)
            h = int(h * ratio)
            x = int(x * ratio)
            
            # Draw a rectangle around each face
            cv2.rectangle(frame, (x,y), (w,h),(0, 0, 255), 1)
            
            # Print the faces' names for current frame
            print("-", name)
            
            # Put a text below the corresponding face rectangle
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, ' '.join(str(name).split('_')), (x+4, h + 18), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        
        print("")
    
    
    # Write edited frame into output video
    output.write(frame)



movie.release()
cv2.destroyAllWindows()