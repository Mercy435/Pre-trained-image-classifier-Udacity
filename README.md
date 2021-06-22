## Udacity project-- pretrained image classifier

This project is an already trained image classifier; it accepts images and classifies them as dogs or not dogs, 
it also returns the breed or type of image passed. 

It makes use of CNN(Convolutional neural network).
The models used for these classifications are: Restnet, Alexnet and VGG

A summary of results of the classification by these models are outputed, showing which model best classifies the images 
given

Below are the steps to run the project:
1. using the command prompt or terminal, clone the repo to your local computer 
   
2. load files using the desired IDE or code editor of your choice 
   
3. on your command prompt or terminal, do a pip install to get the required modules (ast, pillow, torchvision) 

4. on your terminal, run `python check_images.py` or `python check_images.py --arch model_name`; running the first command 
   uses the default value of the model, the second is used when you want to input the name of
   the model you want to use
   
5. the output from 4 above is the result showing you image classification, breed, count and percentages of performance

6. Alternatively, you can run these scripts `sh run_models_batch_uploaded.sh` or  `run_models_batch_uploaded.sh` on 
   your terminal to see the results of the classifier for uploaded and pet images respectively
   these results for the different models are stored in text files in the format _model_image_folder.txt_