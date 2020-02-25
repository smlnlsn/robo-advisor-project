Create and activate a new Anaconda virtual environment:

conda create -n stocks-env python=3.7 # (first time only)
conda activate stocks-env
From within the virtual environment, install the required packages specified in the "requirements.txt" file you created:

pip install -r requirements.txt
From within the virtual environment, demonstrate your ability to run the Python script from the command-line:

python app/robo_advisor.py