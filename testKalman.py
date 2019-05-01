import numpy as np
import matplotlib.pyplot as plt
dt = 0.000512
time = []
def read_data():
    currentSample = 0
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
    file_roll.close()
    file_pitch.close()
    file_gyroX.close()
    file_gyroY.close()

    return roll, pitch, gyroX, gyroY, time
def add_sum_noise(data,R):
    # thêm noise tuyến tính 
    # kết quả sẽ của hệ thống sẽ là y = G*x + v 
    # G là mô hình quan sát
    # R là ma trận hiệp phương sai của nhiễu
    # x là quan sát thực
    # trong trường hợp này vì quan sát nó hơi clean quá nên thêm tí noise xD
    # công thức sẽ là data + N(0,R)
    return data + np.random.multivariate_normal(np.zeros(shape =(R.shape[0])),R)
def get_state(position,velocity):
    return np.column_stack((position,velocity))

# ma trận chuyển trạng thái 
# F = [[1 dt] [0 1]] là đại diện cho phương trình trạng thái y = P*x + R
# vị trí sau sẽ là y_t+1 = y_t + dt*v
# vận tốc lúc sau sẽ là v_t+1 = v_t
# chú ý là ảnh hưởng của gia tốc đã bị bỏ qua

F = np.array([[1,dt],[0,1]])

# Ma trận hiệp phương sai nhiễu hệ thống này nói chung là đại ra chứ méo biết nữa :>
# ma trận này đại diện cho thành thành phần nhiễu N(0, R) của cảm biến, đồng thời ta 
# xét trong hệ hai cảm biến là gyro và accel đồng thời thể hiện trạng thái của hệ theo
# 2 cảm biến này (là velocity và position) nên Q phải là ma trận hiệp phương sai của
# sai số 2 cảm biến. Đồng thời cũng vì 2 cảm biến này độc lập nên ta có Q = [[Qa 0],[0 Qb]]*dt
# ta cần tìm 2 cái này, cơ mà tình hình là cop cái đã :"< chưa học ltđknc
Q = np.array([[0.0001,0],[0,0.0003]])

# Ma trận hiệp phương sai của dự đoán trước và sau
# cái này là để dự đoán nà owo
# ban đầu thì là 0 hết nhá :>

P = np.array([[0,0],[0,0]])

R = 0.003
#chạy thử lào OwO

_,pitch,_,gyroY,time = read_data()
x_hat = get_state(pitch,gyroY)

x_hat_kalman = []

H = np.array([1,0])

K = np.array([0,0])
S = np.array([0])
x_hat_kalman.append(np.array([0,0]))
for (i,pitch_angle) in enumerate(pitch):
    #bước update: x_hat = F*x + B*wi cái này lấy thứ F*x thôi
    #ta update lại trạng thái thứ i dựa trên kalman và
    #ma trận hiệp phương sai thứ i-1 đã tính
    x_hat_kalman.append(F.dot(x_hat_kalman[i]))
    #thêm ảnh hưởng gyro
    P = (F.dot(P)).dot(np.transpose(F))+Q
    S = (H.dot(P)).dot(np.transpose(H)) + R
    #bước tính lại:
    #lấy quan sát: khi ta quan sát thêm 1 giá trị
    #trong trường hợp này là x_hat thì ta có
    #P lúc này là P lúc k/k-1, tức hiệp phương sai
    #của Kalman lúc k và lấy mẫu lúc k-1, bây h cần
    #phải tính lại Pk/k, H là ma trận quan sát
    #chỉ lấy theo accel nên là góc pitch
    #tính kalman gain:
    K = (P.dot(np.transpose(H)))/S
    P = (np.diag((1,1)-K.dot(H))).dot(P)
    #Kalman gain thì nói chung méo có cái gì để spam cả
    #quan sát:
    y_qs = x_hat[i] - x_hat_kalman[i].dot(H) #quan sát và chỉ lấy cái accel
    x_hat_kalman[i+1] = x_hat_kalman[i] + K.dot(y_qs)

plt.scatter(time,pitch, marker="x",label='dữ liệu quan sát')
time.append(time[len(time)-1]+dt)
x_hat_kalman = np.array(x_hat_kalman)

print(x_hat_kalman.mean())
print(x_hat_kalman.std())
plt.plot(time,x_hat_kalman[:,0],'r-',label='giá trị dự đoán')
plt.legend()
plt.show()