import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import tensorflow as tf
from keras import layers
from keras import Sequential
import argparse

nguyen_lieu = [
    'Rau muống', 'Rau mồng tơi', 'Rau nhút', 'Rau răm', 'Dưa leo', 'Cà chua bi', 'Cà chua', 'Khoai tây', 'Khoai lang', 'Khoai mì',
    'Thịt heo', 'Thịt bò', 'Thịt lợn', 'Thịt gà', 'Thịt cừu', 'Cá basa', 'Cá hồi', 'Cá thu', 'Cá ngừ', 'Cá lóc',
    'Tôm sú', 'Tôm hùm', 'Mực ống', 'Mực nang', 'Cua đồng', 'Cua biển', 'Sườn cốt lết', 'Sườn non', 'Thăn heo', 'Thịt ba chỉ',
    'Rau cải', 'Rau ngót', 'Rau đay', 'Rau dền', 'Rau má', 'Rau thơm', 'Rau húng', 'Rau quế', 'Rau mùi', 'Rau tía tô',
    'Cà rốt', 'Củ cải trắng', 'Củ cải đỏ', 'Bí đỏ', 'Bí xanh', 'Bí đao', 'Bí ngô', 'Bí phấn', 'Bí đao', 'Bí ngô',
    'Thịt vịt', 'Thịt ngan', 'Thịt ngỗng', 'Thịt chim', 'Thịt thỏ', 'Thịt nai', 'Thịt đà điểu', 'Thịt trâu', 'Thịt dê', 'Thịt heo rừng',
    'Cá chép', 'Cá rô phi', 'Cá trê', 'Cá bống', 'Cá cơm', 'Cá kèo', 'Cá linh', 'Cá lăng', 'Cá mè', 'Cá trắm',
    'Tôm càng xanh', 'Tôm đất', 'Tôm thẻ', 'Tôm bạc', 'Mực lá', 'Mực trứng', 'Mực cơm', 'Mực sữa', 'Cua gạch', 'Cua thịt',
    'Sườn heo', 'Sườn bò', 'Thăn bò', 'Thịt bò bắp', 'Thịt bò gân', 'Thịt bò phi lê', 'Thịt bò xay', 'Thịt bò nạc', 'Thịt bò ba chỉ', 'Thịt bò thăn nội'
]

data = pd.read_csv('dataset_restaurant.csv')

# Tiền xử lý dữ liệu
data['Thời tiết'] = data['Thời tiết'].map({'Nắng': 1, 'Mưa': 0})
data['Ngày lễ'] = data['Ngày lễ'].map({'Có': 1, 'Không': 0})
data['Thứ'] = data['Thứ'].map({
    'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6,
    'Thứ 2': 0, 'Thứ 3': 1, 'Thứ 4': 2, 'Thứ 5': 3, 'Thứ 6': 4, 'Thứ 7': 5, 'Chủ nhật': 6
})

# Mã hóa cột Nguyên liệu thành số nguyên
data['Nguyên liệu'] = data['Nguyên liệu'].astype('category').cat.codes

# Chia dữ liệu
X = data[['Thứ', 'Thời tiết', 'Ngày lễ', 'Nguyên liệu']]
y = data['Số lượng bán (kg)']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Chuẩn hóa dữ liệu
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Xây dựng mô hình Neural Network
model = Sequential(
    [
        layers.Dense(64, input_dim=X_train.shape[1], activation='relu'),
        layers.Dense(32, activation='relu'),
        layers.Dense(1)
    ]
)

model.compile(optimizer='adam', loss='mean_squared_error')

# Huấn luyện mô hình
model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=1)

y_pred = model.predict(X_test)
print('Mean Squared Error:', mean_squared_error(y_test, y_pred))

# Hàm dự đoán số lượng nguyên liệu cần chuẩn bị
def predict_ingredients(day, weather, holiday):
    day_map = {'Thứ 2': 0, 'Thứ 3': 1, 'Thứ 4': 2, 'Thứ 5': 3, 'Thứ 6': 4, 'Thứ 7': 5, 'Chủ nhật': 6}
    weather_map = {'Nắng': 1, 'Mưa': 0}
    holiday_map = {'Có': 1, 'Không': 0}
    
    day_num = day_map[day]
    weather_num = weather_map[weather]
    holiday_num = holiday_map[holiday]
    
    predictions = []
    for nl in range(len(nguyen_lieu)):
        input_data = pd.DataFrame([[day_num, weather_num, holiday_num, nl]], columns=['Thứ', 'Thời tiết', 'Ngày lễ', 'Nguyên liệu'])
        input_data = scaler.transform(input_data)
        prediction = model.predict(input_data)
        predictions.append(prediction[0][0])
    
    return predictions

# Xử lý đầu vào từ dòng lệnh
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dự đoán số lượng nguyên liệu cần chuẩn bị.')
    parser.add_argument('--day', type=str, required=True, help='Thứ trong tuần (ví dụ: Thứ 2)')
    parser.add_argument('--wea', type=str, required=True, help='Thời tiết (ví dụ: Nắng)')
    parser.add_argument('--h', type=str, required=True, help='Ngày lễ (Có/Không)')
    
    args = parser.parse_args()
    
    day = args.day
    weather = args.wea
    holiday = args.h
    
    predictions = predict_ingredients(day, weather, holiday)
    print(f'Dự đoán số lượng nguyên liệu cần chuẩn bị cho {day}, thời tiết {weather}, ngày lễ {holiday}:')
    for nl, qty in zip(nguyen_lieu, predictions):
        print(f'{nl}: {qty:.2f} kg')
