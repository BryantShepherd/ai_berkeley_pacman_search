# mira.py
# -------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# Mira implementation
import util
PRINT = True

class MiraClassifier:
    """
    Mira classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """
    def __init__( self, legalLabels, max_iterations):
        self.legalLabels = legalLabels
        self.type = "mira"
        self.automaticTuning = False
        self.C = 0.001
        self.legalLabels = legalLabels
        self.max_iterations = max_iterations
        self.initializeWeightsToZero()

    def initializeWeightsToZero(self):
        "Resets the weights of each label to zero vectors"
        self.weights = {}
        for label in self.legalLabels:
            self.weights[label] = util.Counter() # this is the data-structure you should use

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        "Outside shell to call your method. Do not modify this method."

        self.features = trainingData[0].keys() # this could be useful for your code later...

        if (self.automaticTuning):
            Cgrid = [0.002, 0.004, 0.008]
        else:
            Cgrid = [self.C]

        return self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, Cgrid)

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, Cgrid):
        """
        This method sets self.weights using MIRA.  Train the classifier for each value of C in Cgrid,
        then store the weights that give the best accuracy on the validationData.

        Use the provided self.weights[label] data structure so that
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        representing a vector of values.
        """            

        potentialWeights = {}
        for c in Cgrid:
            tempWeight = self.weights.copy()
            for _ in range(self.max_iterations):
                for i, data in enumerate(trainingData):
                    actual = trainingLabels[i]
                    prediction = self.classifyWeight([data], tempWeight)[0]

                    if (actual != prediction):
                        r = ((tempWeight[prediction] - tempWeight[actual]) * data + 1.0 ) / (data * data * 2)
                        r = min(c, r)

                        # compromise for the fact that there is no multiplyAll()
                        # method exist on Counter.
                        f = None
                        if (r == 0):
                            f = data - data
                        else:
                            f = data.copy()
                            f.divideAll(1.0 / r)
                        
                        tempWeight[actual] = tempWeight[actual] + f
                        tempWeight[prediction] = tempWeight[prediction] - f
            potentialWeights[c] = tempWeight

        maxScore = float('-inf')
        maxAccuracyC = float("inf")

        for c in Cgrid:
            score = 0
            for i, data in enumerate(validationData):
                actual = validationLabels[i]
                prediction = self.classifyWeight([data], potentialWeights[c])[0]
                if (actual == prediction): score += 1

            if (score >= maxScore):
                maxAccuracyC = min(c, maxAccuracyC) if score == maxScore else c
                maxScore = score

        self.weights = potentialWeights[maxAccuracyC]
        self.weights["c"] = maxAccuracyC

    def classifyWeight(self, data, weights):
        guesses = []
        for datum in data:
            vectors = util.Counter()
            for l in self.legalLabels:
                vectors[l] = weights[l] * datum
            guesses.append(vectors.argMax())
        return guesses

    def classify(self, data ):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label.  See the project description for details.

        Recall that a datum is a util.counter...
        """
        guesses = []
        for datum in data:
            vectors = util.Counter()
            for l in self.legalLabels:
                vectors[l] = self.weights[l] * datum
            guesses.append(vectors.argMax())
        return guesses


