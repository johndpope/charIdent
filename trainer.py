from dataset import Dataset
import network
import cPickle as pickle

d = Dataset('./dataset')
d.loadDataset();
(training_data, test_data) = d.getPartitions()
net = network.Network([784, 75, 62])
net.SGD(training_data, 10, 30, 3.0, test_data = test_data)
fout = open('network.pkl', 'wb')
pickle.dump(net, fout, pickle.HIGHEST_PROTOCOL)