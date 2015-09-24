from dataset import Dataset
import network
import cPickle as pickle

d = Dataset('./dataset')
print 'Loading dataset...',
d.loadDataset();
print 'done.'
print 'Partitioning dataset...',
(training_data, test_data) = d.getPartitions()
print 'done'
print 'Intialising Neural Network...',
net = network.Network([784, 20, 62])
print 'done'
print 'Training Neural Network...'
net.SGD(training_data, 30, 124, 3.0, test_data = test_data)
print 'done'
fout = open('network.pkl', 'wb')
pickle.dump(net, fout, pickle.HIGHEST_PROTOCOL)