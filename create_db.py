import encoder

"""
Create your initial database with your own pictures.
Drop your picture in the folder images.
"""
if __name__ == '__main__':
    # Create database
    encoder.createData()

    # # Update database adding a new folder ( path='folder/with/new_pictures/' )
    # encoder.updateData(path='img/')
