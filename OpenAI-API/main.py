# Use this file to test all the other functions in the project.

import image_generator
import image_variation

task = input("Enter a task: ")

if task == "g":
    image_generator.generate_image()

if task == "v":
    image_variation.create_variation()