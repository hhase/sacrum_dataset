
# ULTRASOUND SACRUM NAVIGATION DATA SET 
The present data set consists of lower back ultrasound (US) scans from 34 volunteers in the context of my master thesis in reinforcement learning-based autonomous robotic ultrasound (US) navigation. [This paper](https://arxiv.org/abs/2003.13321) further details the acquisition method and the related study.

The data set is available in [this link.](http://campar.in.tum.de/files/SacrumNavDataset/dataset.zip)

## ABOUT THE DATA SET
Each volunteer has an associated environment enabled for x-y cartesian navigation, to train a reinforcing learning (RL) agent. Herefore, each subject is represented by a grid of 11x15 bins, each containing 5 US-frames. The grids are built from *patient files* providing:
- A subject identifier
- A relative path to the frames corresponding to the subject
- A list of coordinates containing US-frames showing the sacrum
- A list of coordinates and the corresponding frame indexes
- An array to visualize the grid environment, where each number represents the closest frame to the center of the bin. The spine is of each subject is approximately located along the 6th row of this matrix, meaning that the most left column corresponds to the bottom part of the scanned volunteer.

Each volunteer also has a directory `Sacrum_SubjectXX` that contains the frames for that subject's environment. Additionally, the folder includes a .csv file consisting of the robot's position information for each acquired frame of said subject. This file can be used among others to rearrange the frames contained in the patient file, increase the number of frames per bin, or to get a better understanding of the data set.

The code used to create the *patient files* can be found in **create_patient_file.py**.
A sample patient loader can be found in **load_patient_file.py**. 

## CITATION
If you use this data set for academic work, please cite as:

```
@misc{hase2020ultrasoundguided,
	title={Ultrasound-Guided Robotic Navigation with Deep Reinforcement Learning},
	author={Hannes Hase and Mohammad Farid Azampour and Maria Tirindelli and Magdalini Paschali and Walter Simson and Emad Fatemizadeh and Nassir Navab},
	year={2020},
	eprint={2003.13321},
	archivePrefix={arXiv},
	primaryClass={cs.LG}
}
```

