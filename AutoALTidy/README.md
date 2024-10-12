# AutoALTidy<br>
### Auto Active Learning - Tidy Version **(Maybe)**
### Limitation
You still need to run [**`initial_random_select.py`**](https://github.com/Gratia2533/cryyy/blob/main/main_pts/initial_random_select.py) first to generate **`partial_box/initial`** before proceeding.<br>

The current version has a fixed dataset configuration, with 70, 10, and 20 samples for Training, Validation, and Test, respectively.<br>
File names must follow the format **`micrograph_{i}`**, where **i is sequential**. Overall, further optimization is still needed.<br>

The folder structure should be like the following:

```bash

Dataset/
├── mrc/    #For all micrographs
│   ├── train/micrograph_{i}.mrc for i in range (0, 70)
│   ├── valid/micrograph_{i}.mrc for i in range (70, 80)
│   └── test/micrograph_{i}.mrc for i in range (80, 100)
├── box/    #For Groundtruth .box files
│   ├── train/micrograph_{i}.mrc for i in range (0, 70)
│   ├── valid/micrograph_{i}.mrc for i in range (70, 80)
│   └── test/micrograph_{i}.mrc for i in range (80, 100)
│   #The folder(including file) above here should prepare in advance
├── partial_box/    #Annotation of particles that increase with each iteration
│   ├── initail/micrograph_{i}.mrc for i in range (0, 70)   #Generate by initial_random_select.py manually
│   └── iter{k}/micrograph_{i}.mrc for i in range (0, 70), for k in range (1,9)     #Generate automatically when correction processing
└── evaluation/{change foldername} #Evaluation saving directory, generate automatically when auto Active Learning processing
    ├── initail_evaluation.html
    └── iter{k}_evaluation.html, for k in range (1,9)

```

## I. How to Use

### 1. Check Paths
Ensure that the paths are correctly configured in **`directory.py`**.

#### 1-1. Warning about these paths
When conducting multiple experiments, please modify the **`evaluation_folder_path`** in **directory.py** to prevent overwriting the evaluation results on the test set. <br> 
If you wish to save additional information as well, make sure to change the path for different experiments to avoid overwriting the results.

### 2. Run the Command
Once paths are set, run the following command to start the Active Learning process:

```bash
python -m AutoALTidy.autoAL_basePts # To execute main program
```
```bash
python -m AutoALTidy.utils.<others> # To check others functional programs in AutoALTidy/utils
```
#### 2-1. Select Uncertainty Method
During execution, you will be prompted to choose an Active Learning method.  
**Enter a number (1-5)** that corresponds to the method you'd like to use:  
<br>
1.Random: Selects particles add to next iterations **randomly**.  
<br>
2.Entropy Score: Selects particles based on their **entropy score**.  
<br>
3.Low Confidence: Selects particles based on **low confidence** levels.  
<br>
4.Entropy Score in Normalize Confidence: Selects particles using the entropy score with **normalized confidence**.  
<br>
5.Boundary Distance: Selects particles based on lower **|confidence - Topt|**.  
<br>

#### 2-2. Set IOU threshold
To set an IOU threshold to retain particles whose IOU value with the Groundtruth exceeds the specified threshold.  
<br>

#### 2-3. Set numbers of particle 
Enter a number to control the number of particles added in each iteration.

## II. AutoALTidy.utils

### correction.py

It is mainly called in the final step of the loop within the main program **`autoAL_basePts.py`** to generate the .box file for the next iteration.

### cbox2box

Processes the confidence values in the .box file differently based on the selected method.

### directory

**Almost** all path configurations should be set here.

### filter_pts

Determines the number of particles to add in each iteration, with three ways for addition: randomly selecting particles to add, adding the smaller values, or adding the larger values.

### formula

Essentially, this contains the calculation formulas for various indicator required by different methods in **`cbox2box`**.

### regular

The **shared process utilized** by each method, regardless of the indicator used.

### tool

A collection of shared utility functions, including path validation, integration of evaluation results, and more.

### workflow

Primarily used for detecting and processing **terminal outputs** within the automation workflow.
