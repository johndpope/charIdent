from preprocess import Preprocess
from dataset import Dataset

p = Preprocess()
p.preprocessDirectory()

# d = Dataset('./output')
# d.loadDataset();
# print d.darray[0][1].im