class DataPoint:
    def __init__(self):
        # Sử dụng dictionary để lưu trữ các trường dữ liệu
        self.__dict__['data'] = {}

    def __setattr__(self, key, value):
        # Thêm cặp key-value vào dictionary 'data'
        self.data[key] = value

    def __getattr__(self, key):
        # Lấy giá trị của key từ dictionary 'data', nếu không có trả về None
        return self.data.get(key, None)

    def __delattr__(self, key):
        # Xóa một trường trong dictionary 'data' theo key
        if key in self.data:
            del self.data[key]

    def to_dict(self):
        # Trả về toàn bộ dictionary data
        return self.data

    def __repr__(self):
        # Hiển thị thông tin các trường dữ liệu
        return f"DataPoint({self.data})"


class Result:
    def __init__(self, config):
        self.config = config

    def to_dict(self, dp):
        result = {}
        for key in self.config:
            result[key] = dp.data[key]
        return result