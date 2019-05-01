import serial
import io
import matplotlib.pyplot as plt

rollArray = []
gyroArray = []
time = []
dt = 0.000512
currentSample = 0

file_roll = open("mpu_data_roll1.txt","w+")
file_pitch = open("mpu_data_pitch1.txt","w+")
file_gyroX = open("mpu_data_gyroX1.txt","w+")
file_gyroY = open("mpu_data_gyroY1.txt","w+")

with serial.Serial('COM25', 9600, timeout=1) as ser:
    while(len(rollArray)<10000):
        roll =  float(ser.readline())
        pitch = float(ser.readline())

        gyroX = float(ser.readline())
        gyroY = float(ser.readline())

        rollArray.append(roll)
        gyroArray.append(gyroX)
        
        
        currentSample += dt
        time.append(currentSample)
        
        file_roll.write(str(roll)+"\n")
        file_pitch.write(str(pitch)+"\n")
        file_gyroX.write(str(gyroX)+"\n")
        file_gyroY.write(str(gyroY)+"\n")

        print("roll =  %.2f  pitch = %.2f gyroX = %.2f gyroY = %.2f" %(roll,pitch,gyroX,gyroY))
plt.subplots_adjust(left=0.0, bottom=0.0, right=1.0, top=0.9,wspace=0.0, hspace=0.0)
plt.scatter(time, rollArray,  marker="x")
plt.show()
file_roll.close() 
file_pitch.close() 
file_gyroX.close() 
file_gyroY.close() 