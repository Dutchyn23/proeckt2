from datetime import datetime

class SensorType:
    def __init__(self, name, units):
        self.name = name
        self.units = units

    def get_info(self):
        """
        Повертає рядок з інформацією про тип датчика.

        :return: Рядок з інформацією про тип датчика
        """
        return f"Тип датчика: {self.name}, Одиниці вимірювання: {self.units}"

    def __str__(self):
        """
        Представлення об'єкту типу датчика у вигляді рядка.
        """
        return self.get_info()

class Sensor:
    def __init__(self, sensor_type, location, data=None):
        self.sensor_type = sensor_type
        self.location = location
        self.data = data or []

    def add_data(self, data_point):
        self.data.append(data_point)

    def get_data(self):
        current_hour = datetime.now().hour
        if current_hour < len(self.data):
            return self.data[current_hour]
        else:
            return None

    def __str__(self):
        current_data = self.get_data()
        all_data = self.data
        return f"Датчик: Тип: {self.sensor_type}, Місце розташування: {self.location}, Поточні дані: {current_data}, Усі дані: {all_data}"

    def print_current_data(self):
        current_data = self.get_data()
        print(f"Датчик: Тип: {self.sensor_type}, Місце розташування: {self.location}, Дані за поточну годину: {current_data}")

    def print_all_data(self):
        print(f"Датчик: Тип: {self.sensor_type}, Місце розташування: {self.location}, Усі дані: {self.data}")

class DataCollector:
    def __init__(self):
        self.collected_data = {}

    def add_sensor_data(self, sensor, data):
        """
        Додає дані датчика до словника зі зібраними даними.
        """
        self.collected_data[sensor] = data

    def get_collected_data(self):
        """
        Повертає словник зі зібраними даними.
        """
        return self.collected_data

class CentralSystem:
    
    def __init__(self, data_collector):
        self.data_collector = data_collector

    def receive_data(self, data_collector):
        self.data_collector = data_collector

    def generate_report(self):
        """
        Генерує звіт на основі зібраних даних.
        """
        collected_data = self.data_collector.get_collected_data()
        report = ""
        for sensor, data in collected_data.items():
            report += f"Датчик: {sensor}, Дані: {data}\n"
        return report

    def save_report_to_file(self, filename):
        """
        Зберігає згенерований звіт у файл.
        """
        report = self.generate_report()
        with open(filename, 'w') as f:
            f.write(report)

class IoTDevice:
    def __init__(self, device_id, location):
        self.device_id = device_id
        self.location = location
        self.sensors = []
        self.data_collector = DataCollector()
        self.initialize_sensors()

    def initialize_sensors(self):
        data_sensor1 = [10]  
        data_sensor2 = [15] 
        data_sensor3 = [20] 

        sensor1 = Sensor(sensor_type=SensorType(name="Якість повітря", units="ppm"), location=self.location, data=data_sensor1)
        sensor2 = Sensor(sensor_type=SensorType(name="Температура", units="Цельсій"), location=self.location, data=data_sensor2)
        sensor3 = Sensor(sensor_type=SensorType(name="Опади", units="мм"), location=self.location, data=data_sensor3)

        self.sensors.extend([sensor1, sensor2, sensor3])

    def collect_data(self):
        for sensor in self.sensors:
            data_point = sensor.get_data()  
            sensor.add_data(data_point)  
            self.data_collector.add_sensor_data(sensor, data_point)

    def transmit_data(self, central_system):
        central_system.receive_data(self.data_collector)

def add_new_device(device_list):
    if device_list:
        print("Ви вже додали пристрій IoT. Ви не можете додати більше одного пристрою.")
    else:
        device_id = len(device_list) + 1

        # Вибір типу девайсу
        print("Виберіть тип пристрою:")
        print("1. Якість повітря")
        print("2. Температура")
        print("3. Опади")
        device_type = input("Введіть номер типу пристрою: ")
        
        # Перевірка на правильність вводу
        while device_type not in ["1", "2", "3"]:
            print("Невірний ввід. Будь ласка, введіть номер типу пристрою зі списку.")
            device_type = input("Введіть номер типу пристрою: ")

        # Введення розташування пристрою
        location = input("Введіть місце розташування пристрою: ")

        # Створення пристрою відповідно до обраного типу
        new_device = IoTDevice(device_id, location)
        if device_type == "1":
            sensor1_data = input(f"Введіть дані для датчика 'Якість повітря' у {location}: ")
            sensor1 = Sensor(sensor_type=SensorType(name="Якість повітря", units="ppm"), location=location)
            sensor1.add_data(int(sensor1_data))
            new_device.sensors.append(sensor1)
        elif device_type == "2":
            sensor2_data = input(f"Введіть дані для датчика 'Температура' у {location}: ")
            sensor2 = Sensor(sensor_type=SensorType(name="Температура", units="Цельсій"), location=location)
            sensor2.add_data(int(sensor2_data))
            new_device.sensors.append(sensor2)
        else:
            sensor3_data = input(f"Введіть дані для датчика 'Опади' у {location}: ")
            sensor3 = Sensor(sensor_type=SensorType(name="Опади", units="мм"), location=location)
            sensor3.add_data(int(sensor3_data))
            new_device.sensors.append(sensor3)
        
        device_list.append(new_device)
        print(f"Новий пристрій додано з ID: {device_id} та розташуванням: {location}")


def save_data_and_generate_report(device_list, filename):
    data_collector = DataCollector()
    for device in device_list:
        device.collect_data()
        device.transmit_data(CentralSystem(data_collector))

    central_system = CentralSystem(data_collector)
    central_system.save_report_to_file(filename)
    print(f"Дані збережено та створено звіт у файл: {filename}")

def view_device_data(device_list):
    for device in device_list:
        print(f"IoT Device ID: {device.device_id}")
        for sensor in device.sensors:
            print(sensor)
        print()

def generate_summary_report(device_list):
    summary_report = ""
    for device in device_list:
        summary_report += f"IoT Device ID: {device.device_id}\n"
        for sensor in device.sensors:
            summary_report += str(sensor) + "\n"
        summary_report += "\n"
    return summary_report

def delete_device(device_list, device_id):
    for device in device_list:
        if device.device_id == device_id:
            device_list.remove(device)
            print(f"IoT Device з ID {device_id} успішно видалено.")
            return
    print(f"Пристрій IoT з ID {device_id} не знайдено.")

def print_menu():
    print("\nМеню:")
    print("1. Додати новий пристрій IoT")
    print("2. Переглянути дані пристроїв")
    print("3. Зберегти дані та згенерувати звіт")
    print("5. Видалити пристрій")
    print("6. Вихід")

def main():
    device_list = []
    filename = "результати.txt"
    while True:
        print_menu()
        choice = input("Введіть ваш вибір: ")
        if choice == "1":
            add_new_device(device_list)
        elif choice == "2":
            view_device_data(device_list)
        elif choice == "3":
            save_data_and_generate_report(device_list, filename)
        elif choice == "5":
            device_id = int(input("Введіть ID, який потрібно видалити: "))
            delete_device(device_list, device_id)
        elif choice == "6":
            print("Вихід з програми...")
            break
        else:
            print("Невірний вибір. Будь ласка, введіть правильний варіант.")

if __name__ == "__main__":
    main()
