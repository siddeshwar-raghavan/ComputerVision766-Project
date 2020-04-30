## SAR Only train
Training using the SAR images, by turning off the transfer learning. This uses the weights from the transfer learning to aid to the training of the various SAR images/ processed SAR images given as input.

What's the advantage you ask?
We had to run training on the optical images for nearly 120 epochs (we had set it at 150 epochs) to get minimal losses. Running of 120 epochs take 6 hours on a large scale AWS GPU and this seemed unnecessary as the optical images didn't change in the logic flow. Hence decided to use the weights obtained from training the optical images and using it for the subsequent runs, this reduced the completion time from 600 minutes (~ 10 hours) to 100 minutes (~ 1 hour 20 mins)