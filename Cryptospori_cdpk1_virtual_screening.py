#installing DeepPurpose library and imporing required modules
!pip install DeepPurpose
from DeepPurpose import utils, dataset, CompoundPred
from DeepPurpose import DTI as models
import warnings
warnings.filterwarnings("ignore")

#############################################################################################
# installing dependencies 
!wget https://repo.anaconda.com/miniconda/Miniconda3-py37_4.8.2-Linux-x86_64.sh
!chmod +x Miniconda3-py37_4.8.2-Linux-x86_64.sh
!bash ./Miniconda3-py37_4.8.2-Linux-x86_64.sh -b -f -p /usr/local
!conda install -c rdkit rdkit -y
import sys

pip install git+https://github.com/bp-kelley/descriptastorus

pip install pandas-flavor==0.2.0
###############################################################################################
# Data encoding and splitting
X_drugs, X_targets, y = dataset.read_file_training_dataset_bioassay('./training2.txt')
print('Drug 1: ' + X_drugs[0])
print('Score 1: ' + str(y[0]))

drug_encoding = 'Morgan'

train, val, test = utils.data_process(X_drug = X_drugs, y = y, drug_encoding = drug_encoding,
                                      split_method='random',frac=[0.7,0.1,0.2],
                                      random_seed = 1)
train.head(1)

config = utils.generate_config(drug_encoding = drug_encoding,
                               cls_hidden_dims = [1024,1024,512],
                               train_epoch = 30,
                               LR = 0.001,
                               batch_size = 8,
                               hidden_dim_drug = 128,
                               )
import numpy as np
np.unique(y)

model = CompoundPred.model_initialize(**config)
model

model.train(train, val, test)

model.save_model('./final_deep_learning')

#######################################################################################################################
# loading 1930980 Enamine compounds in SMILES format
def doll (n=1930980):
    X_drug = dataset.pd.read_csv('Enamine_hts.txt').sample(n=n, replace = True).reset_index(drop = True)
    return X_drug.values
