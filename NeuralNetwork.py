import numpy
import copy

class NN:

    def __init__(self, input_layer_size, output_layer_size, number_of_inputs, nodes_in_layer, randomize_weights = False, randomize_bias = False):

        r_upper = 1.0
        r_lower = 0

        #index = layer, last is output
        self.weights= [numpy.ones((input_layer_size,number_of_inputs)),
                       numpy.ones((output_layer_size,input_layer_size))]

        self.bias   = [numpy.zeros((input_layer_size,1)),
                       numpy.zeros((output_layer_size,1))]

        for layer_size in nodes_in_layer:
            #add a new layer before the last, update the weights array

            self.weights.insert(len(self.weights)-1, numpy.ones((layer_size,self.weights[-2].shape[0])))

            self.weights[-1] = numpy.ones((output_layer_size,self.weights[-2].shape[0]))

            self.bias.insert(len(self.bias)- 1, numpy.zeros((layer_size,1)))
            #fix up weights for the second to last => last layer
            self.bias[-1] = numpy.zeros((1,1))

        if(randomize_weights):
            counter = 0
            for layer in self.weights:
                self.weights[counter] = (r_upper-r_lower) * numpy.random.rand(layer.shape[0],layer.shape[1])
                counter+=1

        if(randomize_bias):
            counter = 0
            for b in self.bias:
                self.bias[counter] = numpy.random.rand(len(b),1)
                counter+=1

    def sigmoid(self, input):

        return 1.0/(1.0 + numpy.exp(-input))

    def sigmoid_derivative(self,input):

        return self.sigmoid(input) * (1 - self.sigmoid(input))

    def compute_output(self,x):

        #i'm not sure if this is a correct formulation one neuron per input
        #in fact i know this isn't, but we'll propagate logic through other layers
        j = 0

        sigmoid = lambda y: 1.0/(1.0 + numpy.exp(-y))

        previous_layer = numpy.apply_along_axis(sigmoid, 1, numpy.dot(self.weights[0],x) + self.bias[0])

        #print previous_layer

        for i in range(1, len(self.weights)):

            previous_layer = numpy.apply_along_axis(sigmoid, 1, numpy.dot(self.weights[i],previous_layer) + self.bias[i])

        return previous_layer

    def randomize(self, weight_layers, bias_layer):

        new_network = self.copy(self)

        for layer in weight_layers:
            if(layer < 0 or layer > len(self.weights)):
                raise AssertionError('Attempt to access non-existent layer for weighting: %i' % layer)
            temp_weight = numpy.zeros(self.weights[layer].shape[0],
                                      self.weights[layer].shape[1])
            for i in range(0, self.weights[layer].shape[0]):
                for j in range(0, self.weights[layer].shape[1]):
                    temp_weight[i][j] = numpy.random.normal(self.weights[layer][i][j],size=1)
            new_network.weights[layer] = temp_weight

        for layer in bias_layer:
            if(layer < 0 or layer > len(self.bias)):
                raise AssertionError('Attempt to access non-existent layer for biasing: %i' % layer)
            new_network.bias[layer] = numpy.asarray([numpy.random.normal(x,size=1) for x in self.bias[layer]])

        return new_network

    def copy(self, neural_network):

        new_network = NN(0,0,0,[])

        new_network.weights = copy.deepcopy(neural_network.weights)
        new_network.bias    = copy.deepcopy(neural_network.bias)

        return new_network

    def print_network(self):

        counter = 0

        for layer in self.weights:

            print 'Layer %i has %i nodes' % (counter, layer.shape[0])
            counter+=1


if __name__ == '__main__':

    basic_network = NN(input_layer_size=6, output_layer_size=1, number_of_inputs=5, nodes_in_layer=[])

    #print 'Basic network output: %f' % basic_network.compute_output([-50, -0.5, -1, 0, 0])

    #test layer addition during construction

    multi_layered_network = NN(input_layer_size=1024, output_layer_size=10, number_of_inputs=5, nodes_in_layer=[512, 256, 64])

    multi_layered_network.print_network()

    print 'Multi-layered output: %s' % str(multi_layered_network.compute_output(numpy.random.rand(5,1)))

    random_network = NN(input_layer_size=1024,
                        output_layer_size = 10,
                        number_of_inputs=5,
                        nodes_in_layer=[512, 256, 64],
                        randomize_weights=True)



