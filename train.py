import face_recognition
import os
import pickle
import shutil

data = {}
update = False
train_count = 0


trained_dir = os.listdir('./trained/')
models = os.listdir('./models/')


# if there is a trained data then continue with update processs 
if 'data.sav' in trained_dir:
    data = pickle.load(open('./trained/data.sav', 'rb'))
    update = True
    print('\nThere is a trained data in "trained" directory, update process has been started.\n')
else:
    print('\nTraining process has been started.\n')


# Control deleted models
deleted_models = []
for x in data:
    deleted = True
    for y in models:
        if x == y:
            deleted = False
    if deleted:
        deleted_models.append(x)
        
for z in deleted_models:
    del data[z]
    print('"{0}" has been deleted from trained data successfully.'.format(' '.join(z.split('_'))))
    



# Each person in models directory
for person in models:

    person_dir = os.listdir("./models/" + person)
    name = ' '.join(person.split('_'))
    
    # Train every model
    update_person = True
    
    
    if update:
        # Train only changed model
        update_person = False
        
        # update_person(False) will not change if there are no changes for current model.
        if person not in data:
            update_person = True
        elif len(person_dir) != len(data[person]):
            update_person = True
    
    
    # There are changes or the first training process
    if update_person:
    
        # Delete the whole person's data to not add the same encodings
        if update and person in data:
            del data[person]
        
        # Each image of current model
        for person_img in person_dir:
        
            # Get the face encodings for the face in each image file
            face = face_recognition.load_image_file("./models/" + person + "/" + person_img)
            face_bounding_boxes = face_recognition.face_locations(face)

            #If training image contains exactly one face
            if len(face_bounding_boxes) == 1:
            
                face_enc = face_recognition.face_encodings(face, known_face_locations=face_bounding_boxes)[0]
                
                # Add face encoding for current image with corresponding label (person) to the training data
                if person in data:
                    data[person].append(face_enc)
                else:
                    data[person] = [face_enc]
                
                train_count += 1
                    
            else:
                print(person + "/" + person_img + " was skipped and can't be used for training.")
                
        
        if train_count > 0:
            print('"{0}" trained successfully ({1} image)'.format(name, train_count))
            train_count = 0
        else:
            # if train_count not greater than 0 then the user must have left an empty model directory in "models" directory.
            print('There are no valid images for "{0}", the directory will be deleted'.format(name))
            shutil.rmtree('./models/' + person)
            models.remove(person)
    
    else:
        print('No update found for "{0}"'.format(name))



if len(data) > 1:

    pickle.dump(data, open('trained/data.sav', 'wb'))
    
    if update:
        print('\nUpdate process has been completed successfully.\n')
    else:
        print('\nModels have been trained successfully.\n')

else:
    print('\nTraining Fail! \nYou must have had at least two valid models in "models" directory.\n')

