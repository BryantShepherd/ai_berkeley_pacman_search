# Week 4 - Ghostbusters

**Điểm cuối cùng**: 25/25

![autograder](autograder.png)

## Câu hỏi 1

```py
def observe(self, observation, gameState):
    noisyDistance = observation
    emissionModel = busters.getObservationDistribution(noisyDistance)
    pacmanPosition = gameState.getPacmanPosition()

    "*** YOUR CODE HERE ***"

    allPossible = util.Counter()

    # Nếu noisyDistance là None -> ghostAgent đã bị bắt -> đặt allPossible[jailPos] = 1.0
    if noisyDistance is None:
        jailPos = self.getJailPosition()
        allPossible[jailPos] = 1.0
    else:
        for p in self.legalPositions:
            trueDistance = util.manhattanDistance(p, pacmanPosition)
            if emissionModel[trueDistance] > 0:
                allPossible[p] = emissionModel[trueDistance] * self.beliefs[p]

    "*** END YOUR CODE HERE ***"

    allPossible.normalize()
    self.beliefs = allPossible
```

## Câu hỏi 2

```py
def elapseTime(self, gameState):
    "*** YOUR CODE HERE ***"
    allPossible = util.Counter()

    for p in self.legalPositions:
        # Trả về các vị trí có thể di chuyển từ p và xác suất ghost sẽ di chuyển tới đó
        newPosDist = self.getPositionDistribution(
            self.setGhostPosition(gameState, p))
        for newPos, prob in newPosDist.items():
            allPossible[newPos] += prob * self.beliefs[p]

    allPossible.normalize()
    self.beliefs = allPossible
```

## Câu hỏi 3

```py
def chooseAction(self, gameState):
    pacmanPosition = gameState.getPacmanPosition()
    legal = [a for a in gameState.getLegalPacmanActions()]
    livingGhosts = gameState.getLivingGhosts()
    livingGhostPositionDistributions = \
        [beliefs for i, beliefs in enumerate(self.ghostBeliefs)
            if livingGhosts[i+1]]

    "*** YOUR CODE HERE ***"
    # Vị trí của ghostAgent với xác suất cao nhất
    closestGhostPos = livingGhostPositionDistributions[0].argMax()
    # Khoảng cách tới vị trí đó
    distanceToCGP = self.distancer.getDistance(pacmanPosition, closestGhostPos)

    # Tìm vị trí của ghostAgent mà có xác suất cao nhất + gần nhất với pacman.
    for l in livingGhostPositionDistributions:
        highestProbPos = l.argMax()
        distanceToHPP = self.distancer.getDistance(pacmanPosition, highestProbPos)
        distanceToCGP = self.distancer.getDistance(pacmanPosition, closestGhostPos)
        if (distanceToHPP < distanceToCGP):
            closestGhostPos = highestProbPos

    bestAction = legal[0]
    bestDistance = float('inf')
    # Tìm hành động giúp pacman tiến gần hơn tới ghostAgent.
    for action in legal:
        successorPosition = Actions.getSuccessor(pacmanPosition, action)
        distanceToClosestGhost = self.distancer.getDistance(successorPosition, closestGhostPos)
        if (distanceToClosestGhost < bestDistance):
            bestDistance = distanceToClosestGhost
            bestAction = action
    return bestAction
```

## Câu hỏi 4

(**Đọc hiểu**)

```py
def initializeUniformly(self, gameState):
    self.particles = list()
    # danh sách tất cả hành động của ghostAgent
    legalPositions = self.legalPositions
    particlePositions = [legalPositions[i % len(
        legalPositions)] for i in range(self.numParticles)]
    self.particles = particlePositions
    return self.particles

def observe(self, observation, gameState):
    noisyDistance = observation
    emissionModel = busters.getObservationDistribution(noisyDistance)
    pacmanPosition = gameState.getPacmanPosition()
    "*** YOUR CODE HERE ***"
    allPossible = util.Counter()
    # Nếu pacman bắt được ma, chuyển các particles thành vị trí của jail
    if noisyDistance == None:
        self.particles = [self.getJailPosition()
                            for i in range(self.numParticles)]
    else:
        # nếu không, cập nhật beliefs tương tự như trong ExactReference
        beliefs = self.getBeliefDistribution()
        for p in self.legalPositions:
            trueDistance = util.manhattanDistance(p, pacmanPosition)
            if emissionModel[trueDistance] > 0:
                allPossible[p] = emissionModel[trueDistance] * beliefs[p]

        # Nếu không có khả năng nào có thể xảy ra, initialize các particles một lần nữa.
        if allPossible.totalCount() == 0:
            self.initializeUniformly(gameState)
        else:
            self.particles = [util.sample(allPossible)
                                for i in range(self.numParticles)]

def getBeliefDistribution(self):
    "*** YOUR CODE HERE ***"
    beliefDistribution = util.Counter()
    for particle in self.particles:
        beliefDistribution[particle] += 1.0
    beliefDistribution.normalize()
    return beliefDistribution
```

## Câu hỏi 5

(**Đọc hiểu**)

```py
def elapseTime(self, gameState):
    "*** YOUR CODE HERE ***"
    newParticle = list()
    for i in range(self.numParticles):
        p = self.particles[i]
        newPosDist = self.getPositionDistribution(
            self.setGhostPosition(gameState, p))
        newParticle.append(util.sample(newPosDist))
    self.particles = newParticle
```

## Câu hỏi 6

(**Đọc hiểu**)

```py
def initializeParticles(self):
    "*** YOUR CODE HERE ***"
    # Danh sách vị trí hợp lý cho ghostAgent
    legalPossibleMultiGhostPositions = list(
        itertools.product(self.legalPositions, repeat=self.numGhosts))
    # randomly shuffling
    random.shuffle(legalPossibleMultiGhostPositions)
    particlePositions = [legalPossibleMultiGhostPositions[i % len(
        legalPossibleMultiGhostPositions)] for i in range(self.numParticles)]

    self.particles = particlePositions
    return self.particles

def observeState(self, gameState):
    pacmanPosition = gameState.getPacmanPosition()
    noisyDistances = gameState.getNoisyGhostDistances()
    if len(noisyDistances) < self.numGhosts:
        return
    emissionModels = [busters.getObservationDistribution(
        dist) for dist in noisyDistances]

    "*** YOUR CODE HERE ***"
    allPossible = util.Counter()
    for particleIndex in range(self.numParticles):
        ghostBelief = 1.0
        for ghostAgent in range(self.numGhosts):
            # Nếu noisyDistance is None, ghostAgent cần phải ở trong jail.
            if noisyDistances[ghostAgent] == None:
                self.particles[particleIndex] = self.getParticleWithGhostInJail(
                    self.particles[particleIndex], ghostAgent)
            else:
                # cập nhật self.beliefs dựa vào khoảng cách thật sự từ pacman đến ghostAgent
                trueDistance = util.manhattanDistance(
                    self.particles[particleIndex][ghostAgent], pacmanPosition)
                ghostBelief *= emissionModels[ghostAgent][trueDistance]
        allPossible[self.particles[particleIndex]] += ghostBelief

    # Nếu weight là vector 0, initialize lại
    if allPossible.totalCount() == 0:
        self.initializeParticles()
    else:
        # Nếu không, lấy tập mẫu từ allPossible.
        allPossible.normalize()
        newParticle = list()
        newParticle = [util.sample(allPossible)
                        for i in range(self.numParticles)]
        self.particles = newParticle

def getBeliefDistribution(self):
    "*** YOUR CODE HERE ***"
    beliefDistribution = util.Counter()
    for particle in self.particles:
        beliefDistribution[particle] += 1.0
    beliefDistribution.normalize()
    return beliefDistribution
```

## Câu hỏi 7

(**Đọc hiểu**)

```py
def elapseTime(self, gameState):
    newParticles = []
    newPosDist = {}

    for oldParticle in self.particles:
        newParticle = list(oldParticle)  # danh sách vị trí của ghostAgent

        "*** YOUR CODE HERE ***"
        if oldParticle not in newPosDist.keys():
            dist = []
            for ghostIndex in range(self.numGhosts):
                dist.append(getPositionDistributionForGhost\
                    (setGhostPositions(gameState, oldParticle),\
                    ghostIndex, self.ghostAgents[ghostIndex]))
                newPosDist[oldParticle] = dist
        for ghostIndex in range(self.numGhosts):
            newParticle[ghostIndex] = util.sample(
                newPosDist[oldParticle][ghostIndex])
        "*** END YOUR CODE HERE ***"
        newParticles.append(tuple(newParticle))
    self.particles = newParticles
```
