import os

this_dir = os.path.dirname(os.path.abspath(__file__))
jar = this_dir + "/picklejar/"
num_posts = 100
file_path_name = jar + 'reddit-data-' + str(num_posts) + '-posts-processed'
file_path = file_path_name + ".json"
