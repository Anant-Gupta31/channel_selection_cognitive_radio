
import random
import matplotlib.pyplot as plt
# from PLOTTING import *

from numpy import *


T=100
K=8
Users=4

def arraybheja(It,t):
    newarray=[]

    for x in range(Users):
        newarray.append(It[x][t])

    return newarray

def Repeat(x):
    _size = len(x)
    repeated = []
    for i in range(_size):
        k = i + 1
        for j in range(k, _size):
            if x[i] == x[j] and x[i] not in repeated:
                repeated.append(x[i])
    return repeated


print("Beginning of Learning Phase \n")
T=100
K=8
Users=4

Lock= [0 for i in range(Users)]

Arms = K

Sum = [[0 for i in range(10000)] for j in range(Users)]

Number = [[0 for i in range(10000)] for j in range(Users)]

Reward = [[0 for i in range(10000)] for j in range(Users)]

Final_Mean = [[0 for i in range(K)] for j in range(Users)]

deviation=0.03

Correct_Probability=[0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2]

sa = [-1 for i in range(Users)]     #index on which user is playing

flag= [0 for i in range(Users)]

indicator=[0 for i in range(Users)]

RepeatedArms = []
Arm = [K-i for i in range(K)]

collisions_learning=0

collisions_indicator= [0 for i in range(Users)]



learning_rounds=2000
trekking_rounds=8000

Collision_plot = [0 for i in range(Users)]

Regret_plot = [0 for i in range(10000)]

Regret_learning = 0

Max_Learning= 0

primary= [-1 for i in range(Users)]

sum1=0

for x in range(Users):
    Max_Learning+=Correct_Probability[x]

for t in range(learning_rounds):

    indicator = [0 for i in range(Users)]


    for x in range(Users):


        if Lock[x]==1:
            sa[x]=(sa[x]+1)%K
        else:
            sa[x]=random.randint(1,K)

    # if (t==0):
    #     sa=[1,2,5,2]

    for x in range(Users):
        primary[x]=round(random.random(),3)
        # flag=1

    #flag = 0
    for x in range(Users):

        if Lock[x]==0 and primary[x]<Correct_Probability[sa[x]]:
            RepeatedArms=array(Repeat(sa))
            occurrence = sa.count(sa[x])    #checking who all are on the arm sa[x]

            if occurrence==1 and primary[x]<Correct_Probability[sa[x]]:
                Lock[x]=1
                indicator[x]=1
            else:
                for y in range(x, Users):
                    if sa[y]==sa[x]:
                        indicator[y]=0

        elif Lock[x]==1:
            RepeatedArms = Repeat(sa)
            occurrence = sa.count(sa[x])

            if occurrence==1 and primary[x]<Correct_Probability[sa[x]]:
                # Lock[x]=1
                indicator[x]=1
            else:
                for y in range(x,Users):
                    if sa[y]==sa[x]:
                        indicator[y]=0

        if indicator[x] == 1 and primary[x]<Correct_Probability[sa[x]]:
            Reward[x][sa[x]] = (random.uniform(Correct_Probability[sa[x]] - 0.01, Correct_Probability[sa[x]] + 0.01))
            Sum[x][sa[x]] += Reward[x][sa[x]]
            sum1+=Reward[x][sa[x]]
            Number[x][sa[x]] += 1
        else:
            Number[x][sa[x]] += 1

    # print(f"Chosen arm after round {t + 1}")
    # print(sa)

    # print(primary)
    # print(sum1)
    if len(Repeat(sa)) > 0:
        collisions_learning+=len(Repeat(sa))
    # print(sa)
    # print(collisions_learning)
    Regret_learning=round(Max_Learning*(t+1)-sum1,3)

    Regret_plot[t]=Regret_learning

    # print(Regret_learning)
for x in range(Users):
    for y in range(8):
        Final_Mean[x][y] = round(Sum[x][y]/Number[x][y],5)

# print("Final Arm after Learning")
# print(sa)

# print(Regret_learning)

print("collisions_learning")
print(collisions_learning)

print("\n Final mean of Each player")
print(Final_Mean)
print("Arms at end of Learning")
print(sa)





#TREKKING


# print("Start of Trekking")

Yk = [[0 for i in range(10000)] for j in range(Users)]

It = [[0 for i in range(10000)] for j in range(Users)]


TrekkingLock=[0 for i in range(Users)]


J=[]    #arm index of reserved

# sa=[0,1,4,2]

print("Arm at start of trekking")

print(sa)


for x in range(Users):
    if sa[x]==0:
        TrekkingLock[x]=1
        It[x][0]=0
    J.append(sa[x])

collision_trekking=0

Regret_trekking = 0

Reward_trekking = 0

Sum_Trekking = [[0 for i in range(K)] for j in range(Users)]

for x in range(Users):
    if J[x]!=0:
        It[x][0]=J[x]-1


M = [(i+1)*10 for i in range(8)]
print("Trekking Started")
flagx = [0 for i in range(K)]

for t in range(1,trekking_rounds+1):

    for x in range(Users):

        if TrekkingLock[x]==1:
            It[x][t]=It[x][t-1]
            flagx[x]=1

        elif Yk[x][J[x]] <= M[It[x][t]]:
            It[x][t] = It[x][t-1]

        elif It[x][t-1]!=0:
            It[x][t] = It[x][t-1]-1
            J[x] = It[x][t-1]
        else:
            It[x][t]=0
            TrekkingLock[x]=1
            J[x]=0

        Yk[x][J[x]] += 1

    newarra=arraybheja(It,t)
    newarray=[]
    for x in range(Users):
        newarray.append(newarra[x])

    # print(newarray)
    for x in range(Users):

        if newarray.count(It[x][t])>1 and random.random()<Correct_Probability[It[x][t]]:
            It[x][t]=J[x]
            TrekkingLock[x]=1
            collision_trekking += 1

        elif random.random()<Correct_Probability[It[x][t]] and flagx[x]==0:
            Reward_trekking+=Correct_Probability[It[x][t]]

        if flagx[x]==1:
            Reward_trekking += Correct_Probability[It[x][t]]

    Regret_plot[learning_rounds+t-1] = Regret_learning + Max_Learning*(t) - Reward_trekking
newfinal = []
for x in range(Users):
    newfinal.append(It[x][2500])

print(newfinal)
print(collision_trekking)
print(TrekkingLock)

Total_Collision=collision_trekking+collisions_learning

print(f"Total Collisions {Total_Collision}")
print(f"Total Reward {Reward_trekking+sum1}")

print(f"Regret {Max_Learning*(learning_rounds+trekking_rounds)-(Reward_trekking+sum1)}")


x = [i for i in range(10000)]

plt.plot(x,Regret_plot)
plt.xlabel("Number of Rounds")
plt.ylabel("Regret")
plt.show()


