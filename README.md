# 0hh1 - Solver

Aims to solve the ['0hh1 puzzle'](https://0hh1.com/) for all the sizes (4x4, 6x6, 8x8, 10x10 12x12). for both the web version (using selenium) and on android version (using adb)

# usage

```commandline
# clone the repo
git clone https://github.com/Adwaith-Rajesh/0hh1-solver.git

# get you chrome driver from here. https://chromedriver.chromium.org/downloads
# place the driver in the bin dir of the venv or modify the code to add the drivers path.

# run the following command

python3 main.py web 12

# here 12 stands for the shape of your puzzle, this can be 4, 6, 8, 10, 12

# in order for verbose output you can use this
python3 main.py web 8 -v

```
