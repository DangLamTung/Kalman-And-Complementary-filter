import serial
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

def animate(i, xs, ys):
    with serial.Serial('COM25', 9600, timeout=1) as ser:
         # Read temperature (Celsius) from TMP102
        roll =  float(ser.readline())
        pitch = float(ser.readline())

        gyroX = float(ser.readline())
        gyroY = float(ser.readline())
        # Add x and y to lists
        xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
        ys.append(roll)

    # Limit x and y lists to 20 items
        xs = xs[-20:]
        ys = ys[-20:]

    # Draw x and y lists
        ax.clear()
        ax.plot(xs, ys)

    # Format plot
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        plt.title('MPU 6050')
        plt.ylabel('Roll')

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
plt.show()