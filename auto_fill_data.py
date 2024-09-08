import pandas as pd
import numpy as np
from datetime import datetime, timedelta

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

ngay_le = [
    '2023-01-01', '2023-04-30', '2023-05-01', '2023-09-02', '2023-02-10', '2023-02-11', '2023-02-12', '2023-02-13', '2023-02-14', '2023-02-15'
]

# Tạo danh sách các ngày trong năm 2023
start_date = datetime(2023, 1, 1)
dates = [start_date + timedelta(days=x) for x in range(365)]

# Tạo dữ liệu mẫu
data = []
for date in dates:
    for nl in nguyen_lieu:
        day_of_week = date.strftime('%A')
        weather = np.random.choice(['Nắng', 'Mưa'])
        holiday = 'Có' if date.strftime('%Y-%m-%d') in ngay_le else 'Không'
        
        if weather == 'Mưa':
            if nl in ['Thịt bò', 'Cá']:
                quantity = np.random.randint(50, 200)
            else:
                quantity = np.random.randint(1, 100)
        else:
            quantity = np.random.randint(1, 200)
        
        if holiday == 'Có':
            quantity *= 1.5
        
        data.append([date.strftime('%Y-%m-%d'), day_of_week, nl, quantity, weather, holiday])

df = pd.DataFrame(data, columns=['Ngày', 'Thứ', 'Nguyên liệu', 'Số lượng bán (kg)', 'Thời tiết', 'Ngày lễ'])

df.to_csv('dataset_restaurant.csv', index=False)

print(df.head())
