#GroceryStoreSim.py
#Name:Bennett Schulte
#Date:11/24/25
#Assignment:Lab 11

import simpy
import random

eventLog = []
waitingShoppers = []
idleTime = 0


def shopper(env, id):
    arrive = env.now
    items = random.randint(5, 20)
    shoppingTime = items / 2
    yield env.timeout(shoppingTime)
    waitingShoppers.append((id, items, arrive, env.now))


def checker(env):
    global idleTime
    while True:
        if len(waitingShoppers) == 0:
            idleTime += 1
            yield env.timeout(1)
        else:
            customer = waitingShoppers.pop(0)
            items = customer[1]
            checkoutTime = items / 10
            if checkoutTime < 1:
                checkoutTime = 1
            yield env.timeout(checkoutTime)
            eventLog.append((customer[0], customer[1], customer[2], customer[3], env.now))


def customerArrival(env):
    num = 0
    while True:
        num += 1
        env.process(shopper(env, num))
        yield env.timeout(2)


def processResults():
    totalWait = 0
    totalShoppers = len(eventLog)
    maxWait = 0
    totalItems = 0

    for e in eventLog:
        wait = e[4] - e[3]
        totalWait += wait
        if wait > maxWait:
            maxWait = wait
        totalItems += e[1]

    avgWait = totalWait / totalShoppers
    avgItems = totalItems / totalShoppers

    print("Total shoppers served:", totalShoppers)
    print("Average wait time:", avgWait)
    print("Max wait time:", maxWait)
    print("Average number of items:", avgItems)
    print("Total idle time:", idleTime)


def main():
    env = simpy.Environment()

    env.process(customerArrival(env))

    for i in range(3):
        env.process(checker(env))

    env.run(until=180)

    print("Shoppers still waiting:", len(waitingShoppers))
    processResults()


main()
