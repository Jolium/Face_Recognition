import encoder

"""
Run this file each time you want to manually update the database.
Other wise it will update each time you start the application.

Drop your pictures in the folder 'images';
Run this file;
And the database is updated with your own pictures.
"""

if __name__ == '__main__':
    # Create database
    encoder.create_database()

    # # Update database adding a non standard folder
    # new_path = './folder/with/new_pictures/'
    # encoder.update_database(path=new_path)
