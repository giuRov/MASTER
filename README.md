# MASTER
## Multiple ASpect TrajEctoRy management and analysis

------------------------------------------------------
In order to monitor the tourism flow in Venice, the questions we want to answer are:

**a)** How do the stamps of the users vary in space and time?

**b)** Is it possible to classify the users into categories, like workers, students, tourists?

**c)** Are there typical patterns in the movements of the users?

**d)** Are there different behaviors during the weekday and at the weekend?

**e)** Which are the common itineraries for tourists?

**f)** Detect the behavior of tourists during the different days of their stay.




The project is organized as follow:

```
project
│   README.md
│   requirements.txt    
│
└───transformData
│   └───data.txt
│   
└───script
    └───clustering.ipynb
    |
    └───datasetInterfaces.ipynb
    |
    └───interfaces
    |   └───multipleDate
    |   │  └───code.py
    |   │  │
    |   │  └───output
    |   │
    |   └───singleDate
    |   │  └───code.py
    |   │  │
    |   │  └───output
    |   │
    |   └───trajectories
    |   │  └───code.py
    |   │  │
    |   │  └───outputMurano
    |   │  └───outputsingleMurano
    |   │
    |   └───videoSingleDay
    |      └───code.py
    |      │
    |      └───output
    |      └───outputVideo.mp4
    |
    └───newInterfaces
        └───MASTERlogo.png
        │
        └───clusters
        │  └───validations.py
        │  │
        │  └───clusterCarnivalAllTickets.png
        │  └───clusterCarnivalResidents.png
        │  └───clusterCarnivalTourists.png
        │
        └───validationsTourists
           └───tourists.py
           │
           └───carnivalOneWeek.mov
           └───carnivalThreeDays.mov
```

In the ```transformData``` folder there is a ```.txt``` file with the list of the datasets needed for the analysis. 

In the ```script``` folder there are two files with the ```.ipynb``` extension in which we analysed the datasets in the folder described above, and we built the ```.csv``` files used for displaying the data in the ```interfaces``` folder.

In the ```interfaces``` and in the ```newInterfaces``` folder, you can find a subfolder for each of the interfaces. In each of these subfolders, you find a file with the ```.py``` extension which contains the code used to build the interfaces and an ```output``` file with the results.


## Installation

If you want to run code locally, you can download the entire repository and install the requirements as follow:

    pip install -r requirements.txt
