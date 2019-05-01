import matplotlib.pyplot as plt
import numpy as np

file_roll = open("mpu_data_roll1.txt","r")
file_pitch = open("mpu_data_pitch1.txt","r")
file_gyroX = open("mpu_data_gyroX1.txt","r")
file_gyroY = open("mpu_data_gyroY1.txt","r")

time = []
roll = []
pitch = []

gyroX = []
gyroY = []

currentAngle = []
angle = []

currentSample = 0
dt = 0.00512
for l in file_roll.readlines():
    roll.append(float(l))
    currentSample += dt
    time.append(currentSample)

for a in file_gyroX.readlines():
    gyroX.append(float(a))

for b in file_pitch.readlines():
    pitch.append(float(b))

for c in file_gyroY.readlines():
    gyroY.append(float(c))
gyro_tmp = 0
gyro_angle = []

gyroY = np.array(gyroY)
pitch = np.array(pitch)

print(pitch.mean())
print(pitch.std())

for (i,t) in enumerate(time):
    gyro_tmp = gyro_tmp - dt*(gyroY[i] - 13.502737000000003)
    gyro_angle.append(gyro_tmp)
    #print(gyroY)

angle.append(0)
for (i,roll_angle) in enumerate(pitch):
    angle.append(0.9*(angle[i]+(gyroY[i] - 13.502737000000003)*dt) + (1-0.9)*(roll_angle+5.854612))

file_roll.close()
file_pitch.close()
file_gyroX.close()
file_gyroY.close()

angle = np.array(angle)
print(angle.mean())
print(angle.std())
print(gyroY[np.where(gyroY<0)])

plt.scatter(time,pitch,label='giá trị accel_angle khi đã trừ offset',linewidth=1)

plt.scatter(time,gyro_angle,label='giá trị gyro_angle khi đã trừ offset',linewidth=1)
time.append(time[len(time)-1]+dt)
plt.plot(time,angle,'r-',label='giá trị dự đoán')
plt.legend()
plt.show()

