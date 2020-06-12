import encoder

"""
For manually create a database
Drop your pictures in the folder 'images'
Create database with your own pictures
"""
if __name__ == '__main__':
    # Create database
    encoder.create_database()

    # # Update database adding a non standard folder
    # new_path = './folder/with/new_pictures/'
    # encoder.update_database(path=new_path)
