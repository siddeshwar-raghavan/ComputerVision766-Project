## SAR Only train
Training using the SAR images, by turning off the transfer learning. This uses the weights from the transfer learning to aid to the training of the various SAR images/ processed SAR images given as input.

What's the advantage you ask?
Reduced training time and test time from 600 minutes to 100 minutes. 

This was achieved by storing the weights generated during transfer learning for the first time and using these weights in the subsequent runs skipping  the transfer learning step entirely. As the transfer learning was optimised at 150 epochs and uses the same set of train images, hence the weights generated during each run will be the same. Since all attempts to improve performance by adding filters were only applied to SAR images! Code changes were made on the baseline code for this, and it saved significant time in running the entire cycle multiple times.


Baseline scripts are from SpaceNet 6 competition - https://github.com/CosmiQ/CosmiQ_SN6_Baseline