# AutoALTidy<br>
### Auto Active Learning - Tidy Version **(Maybe)**
You still need to run [**`initial_random_select.py`**](https://github.com/Gratia2533/cryyy/blob/main/main_pts/initial_random_select.py) first to generate **`partial_box/initial`** before proceeding.
## How to Use

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
python -m AutoALTidy.utils.<others.py> # To check others functional programs in AutoALTidy/utils
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
4.Entropy Score in Normalize Confidence: Selects particles using the entropy score within **normalized confidence**.  
<br>
5.Boundary Distance: Selects particles based on lower **|confidence - Topt|**.  
<br>

#### 2-2. Set IOU threshold
To set an IOU threshold to retain particles whose IOU value with the Groundtruth exceeds the specified threshold.  
<br>

#### 2-3. Set numbers of particle 
Enter a number to control the number of particles added in each iteration.
