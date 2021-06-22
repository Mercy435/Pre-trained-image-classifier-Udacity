#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# */AIPND-revision/intropyproject-classify-pet-images/check_images.py
#
# TODO 0: Add your information below for Programmer & Date Created.                                                                             
# PROGRAMMER: Isaac M
# DATE CREATED: 21/06/2021                                 
# REVISED DATE: 
# PURPOSE: Classifies pet images using a pretrained CNN model, compares these
#          classifications to the true identity of the pets in the images, and
#          summarizes how well the CNN performed on the image classification task. 
#          Note that the true identity of the pet (or object) in the image is 
#          indicated by the filename of the image. Therefore, your program must
#          first extract the pet image label from the filename before
#          classifying the images using the pretrained CNN model. With this 
#          program we will be comparing the performance of 3 different CNN model
#          architectures to determine which provides the 'best' classification.
#
# Use argparse Expected Call with <> indicating expected user input:
#      python check_images.py --dir <directory with images> --arch <model>
#             --dogfile <file that contains dognames>
#   Example call:
#    python check_images.py --dir pet_images/ --arch vgg --dogfile dognames.txt
##

# Imports python modules
from time import time, sleep

# Imports print functions that check the lab
from print_functions_for_lab_checks import *

# Imports functions created for this program
from get_input_args import get_input_args
from get_pet_labels import get_pet_labels
from classify_images import classify_images
from adjust_results4_isadog import adjust_results4_isadog
from calculates_results_stats import calculates_results_stats
from print_results import print_results

# Main program function defined below
start_time = time()


def main():
    # TODO 0: Measures total program runtime by collecting start time
    start_time = time()

    # TODO 1: Define get_input_args function within the file get_input_args.py


import argparse


def get_input_args():
    """
        Retrieves and parses the 3 command line arguments provided by the user when
        they run the program from a terminal window. This function uses Python's 
        argparse module to created and defined these 3 command line arguments. If 
        the user fails to provide some or all of the 3 arguments, then the default 
        values are used for the missing arguments. 
        Command Line Arguments:
          1. Image Folder as --dir with default value 'pet_images'
          2. CNN Model Architecture as --arch with default value 'vgg'
          3. Text File with Dog Names as --dogfile with default value 'dognames.txt'
        This function returns these arguments as an ArgumentParser object.
        Parameters:
         None - simply using argparse module to create & store command line arguments
        Returns:
         parse_args() -data structure that stores the command line arguments object  
        """
    # Create Parse using ArgumentParser
    parser = argparse.ArgumentParser()
    # Create 3 command line arguments as mentioned above using add_argument() from ArguementParser method

    parser.add_argument('--dir', type=str, default='pet_images/',
                        help='path to folder of images')
    parser.add_argument('--arch', default='vgg')
    parser.add_argument('--dogfile', default='dognames.txt')
    # Replace None with parser.parse_args() parsed argument collection that
    # you created with this function
    return parser.parse_args()


in_arg = get_input_args()

# Function that checks command line arguments using in_arg
check_command_line_arguments(in_arg)

# This function retrieves 3 Command Line Arugments from user as input from
# the user running the program from a terminal window. This function returns
# the collection of these command line arguments from the function call as
# the variable in_arg

from os import listdir


def get_pet_labels(image_dir):
    in_files = listdir(image_dir)
    results_dic = dict()
    for idx in range(0, len(in_files), 1):
        if in_files[idx][0] != ".":
            pet_label = ""
            word_pet_label = in_files[idx].lower().split("_")
            for word in word_pet_label:  # German shepherd dog 04890.jpg
                if word.isalpha():
                    pet_label += word + " "

            pet_label = pet_label.strip()
            if in_files[idx] not in results_dic:
                results_dic[in_files[idx]] = [pet_label]
            else:
                print("** Warning: Duplicate files exist in directory:",
                      in_files[idx])
    return results_dic


results = get_pet_labels(in_arg.dir)
print(results)

# Function that checks Pet Images in the results Dictionary using results
check_creating_pet_image_labels(results)

# TODO 3: Define classify_images function within the file classiy_images.py
# Once the classify_images function has been defined replace first 'None'
# in the function call with in_arg.dir and replace the last 'None' in the
# function call with in_arg.arch  Once you have done the replacements your
# function call should look like this:
#             classify_images(in_arg.dir, results, in_arg.arch)
# Creates Classifier Labels with classifier function, Compares Labels,
# and adds these results to the results dictionary - results

from classifier import classifier


def classify_images(images_dir, results_dic, model):
    for key in results_dic:
        model_label = classifier(images_dir + key, model)
        model_label = model_label.lower().strip()
        truth = results_dic[key][0]
        #         print((truth, model_label))
        if truth in model_label:
            results_dic[key].extend([model_label, 1])
        else:
            results_dic[key].extend([model_label, 0])
    #         print(results_dic[key])


classify_images(in_arg.dir, results, in_arg.arch)

# Function that checks Results Dictionary using results
check_classifying_images(results)


# TODO 4: Define adjust_results4_isadog function within the file adjust_results4_isadog.py
def adjust_results4_isadog(results_dic, dogfile):
    dognames_dic = dict()
    with open(dogfile, "r") as infile:
        # Reads in dognames from first line in file
        line = infile.readline()
        while line != "":
            line = line.strip('\n')
            if line not in dognames_dic:
                dognames_dic[line] = 1
            line = infile.readline()
    for key in results_dic:
        if results_dic[key][0] in dognames_dic:
            if results_dic[key][1] in dognames_dic:
                results_dic[key].extend((1, 1))
            else:
                results_dic[key].extend((1, 0))
        else:
            if results_dic[key][1] in dognames_dic:
                results_dic[key].extend((0, 1))
            else:
                results_dic[key].extend((0, 0))
                # Once the adjust_results4_isadog function has been defined replace 'None'
        # in the function call with in_arg.dogfile  Once you have done the 
        # replacements your function call should look like this: 
        #          adjust_results4_isadog(results, in_arg.dogfile)
        # Adjusts the results dictionary to determine if classifier correctly 
        # classified images as 'a dog' or 'not a dog'. This demonstrates if 
        # model can correctly classify dog images as dogs (regardless of breed)


adjust_results4_isadog(results, in_arg.dogfile)

# Function that checks Results Dictionary for is-a-dog adjustment using results
check_classifying_labels_as_dogs(results)


# TODO 5: Define calculates_results_stats function within the file calculates_results_stats.py
def calculates_results_stats(results_dic):
    # This function creates the results statistics dictionary that contains a
    results_stats_dic = dict()
    # Sets all counters to initial values of zero so that they can
    # be incremented while processing through the images in results_dic
    results_stats_dic['n_dogs_img'] = 0
    results_stats_dic['n_match'] = 0
    results_stats_dic['n_correct_dogs'] = 0
    results_stats_dic['n_correct_notdogs'] = 0
    results_stats_dic['n_correct_breed'] = 0
    # process through the results dictionary
    for key in results_dic:
        # Labels Match Exactly
        if results_dic[key][2] == 1:
            results_stats_dic['n_match'] += 1
        if results_dic[key][3] == 1 and results_dic[key][2] == 1:
            results_stats_dic['n_correct_breed'] += 1
        # Pet Image Label is a Dog - counts number of dog images
        if results_dic[key][3] == 1:
            results_stats_dic['n_dogs_img'] += 1
            # Classifier classifies image as Dog (& pet image is a dog)
            # counts number of correct dog classifications
            if results_dic[key][4] == 1:
                results_stats_dic['n_correct_dogs'] += 1
        else:
            if results_dic[key][3] == 0 and results_dic[key][4] == 0:
                results_stats_dic['n_correct_notdogs'] += 1
        # Calculates run statistics (counts & percentages) below that are calculated
        # using the counters from above.

        # calculates number of total images
    results_stats_dic['n_images'] = len(results_dic)

    # calculates number of not-a-dog images using - images & dog images counts
    results_stats_dic['n_notdogs_img'] = (results_stats_dic['n_images'] -
                                          results_stats_dic['n_dogs_img'])
    # Calculates % correct for matches.
    results_stats_dic['pct_match'] = (results_stats_dic['n_match'] / results_stats_dic['n_images']) * 100.0
    # Calculates % correct dogs
    results_stats_dic['pct_correct_dogs'] = (results_stats_dic['n_correct_dogs'] / results_stats_dic[
        'n_dogs_img']) * 100.0
    # Calculates results_stats_dic[ % correct breed of dog
    results_stats_dic['pct_correct_breed'] = (results_stats_dic['n_correct_breed'] / results_stats_dic[
        'n_dogs_img']) * 100.0

    # Calculates % correct not-results_stats_dic[a-dog images
    # Uses conditional statement for when no 'not a dog' images were submitted
    if results_stats_dic['n_notdogs_img'] > 0:
        results_stats_dic['pct_correct_notdogs'] = (results_stats_dic['n_correct_notdogs'] /
                                                    results_stats_dic['n_notdogs_img']) * 100.0
    else:
        results_stats_dic['pct_correct_notdogs'] = 0.0
    return results_stats_dic

    # summary of the results statistics (this includes counts & percentages). This
    # dictionary is returned from the function call as the variable results_stats
    # Calculates results of run and puts statistics in the Results Statistics
    # Dictionary - called results_stats


results_stats = calculates_results_stats(results)

# Function that checks Results Statistics Dictionary using results_stats
check_calculating_results(results, results_stats)


# TODO 6: Define print_results function within the file print_results.py
def print_results(results_dic, results_stats_dic, model,
                  print_incorrect_dogs=False, print_incorrect_breed=False):
    # Once the print_results function has been defined replace 'None'
    # in the function call with in_arg.arch  Once you have done the
    # replacements your function call should look like this:
    #      print_results(results, results_stats, in_arg.arch, True, True)
    # Prints summary results, incorrect classifications of dogs (if requested)
    # and incorrectly classified breeds (if requested)
    # Prints summary statistics over the run
    print("\n\n*** Results Summary for CNN Model Architecture", model.upper(),
          "***")
    print("{:20}: {:3d}".format('N Images', results_stats_dic['n_images']))
    print("{:20}: {:3d}".format('N Dog Images', results_stats_dic['n_dogs_img']))
    print("N Not-Dog Images: {}".format(results_stats_dic['n_notdogs_img']))
    # Prints summary statistics (percentages) on Model Run
    print(" ")
    for key in results_stats_dic:
        if "p" in key:
            print("{}:{}".format(key, results_stats_dic[key]))
        # IF print_incorrect_dogs == True AND there were images incorrectly 
        # classified as dogs or vice versa - print out these cases
    if (print_incorrect_dogs and
            ((results_stats_dic['n_correct_dogs'] + results_stats_dic['n_correct_notdogs'])
             != results_stats_dic['n_images'])
    ):
        print("\nINCORRECT Dog/NOT Dog Assignments:")

        # process through results dict, printing incorrectly classified dogs
        for key in results_dic:
            if (results_dic[key][3] == 1 and results_dic[key][4] == 0) or (
                    results_dic[key][3] == 0 and results_dic[key][4] == 1):
                print("{},{}".format(results_dic[key][0], results_dic[key][1]))

        # IF print_incorrect_breed == True AND there were dogs whose breeds
        # were incorrectly classified - print out these cases                    
    if (print_incorrect_breed and
            (results_stats_dic['n_correct_dogs'] != results_stats_dic['n_correct_breed'])):
        print("\nINCORRECT Dog Breed Assignment:")

        # process through results dict, printing incorrectly classified breeds
        for key in results_dic:

            # Pet Image Label is-a-Dog, classified as-a-dog but is WRONG breed
            if (sum(results_dic[key][3:]) == 2 and
                    results_dic[key][2] == 0):
                print("Real: {:>26}   Classifier: {:>30}".format(results_dic[key][0],
                                                                 results_dic[key][1]))


print_results(results, results_stats, in_arg.arch, True, True)

# TODO 0: Measure total program runtime by collecting end time
end_time = time()

# TODO 0: Computes overall runtime in seconds & prints it in hh:mm:ss format
tot_time = end_time - start_time  # calculate difference between end time and start time
print("\n** Total Elapsed Runtime:",
      str(int((tot_time / 3600))) + ":" + str(int((tot_time % 3600) / 60)) + ":"
      + str(int((tot_time % 3600) % 60)))

# Call to main function to run the program
if __name__ == "__main__":
    main()
