from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import random

# Import the table classes from your create_db.py
from create_db import Machine, Sensor, Model, File, Predictions, FileType, MachineType, SensorType, MachineSensorMapping, MachineSensorModelMapping, Base

# Database Connection (PostgreSQL)
DATABASE_URL = "postgresql://postgres:Finiteloop123@postgres:5432/norm_db_00"

# Create the engine and session
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Define some dummy data
machine_names = ['Machine A', 'Machine B', 'Machine C']
sensor_names = ['Temperature Sensor', 'Pressure Sensor', 'Vibration Sensor']
model_names = ['Model 1', 'Model 2', 'Model 3']
file_names = ['File_A', 'File_B', 'File_C']
prediction_types = ['Classification', 'Regression', 'Anomaly Detection']
file_type_names = ['Audio', 'Video', 'Text']
machine_type_names = ['Type A', 'Type B', 'Type C']  # Dummy machine types
sensor_type_names = ['Temperature', 'Pressure', 'Vibration']  # Dummy sensor types

# Insert dummy file types
file_types = [FileType(file_type_name=name) for name in file_type_names]
session.add_all(file_types)
session.commit()

# Insert dummy machine types
machine_types = [MachineType(machine_type_name=name) for name in machine_type_names]
session.add_all(machine_types)
session.commit()

# Insert dummy sensor types (this fixes the foreign key issue)
sensor_types = [SensorType(sensor_type_name=name) for name in sensor_type_names]
session.add_all(sensor_types)
session.commit()

# Insert dummy machines
machines = [Machine(machine_name=name, machine_type_id=random.choice([mt.machine_type_id for mt in machine_types]), is_active=True, created_date=datetime.now()) for name in machine_names]
session.add_all(machines)
session.commit()

# Insert dummy sensors
sensors = [Sensor(sensor_name=name, sensor_type_id=random.choice([st.sensor_type_id for st in sensor_types]), created_date=datetime.now()) for name in sensor_names]
session.add_all(sensors)
session.commit()

# Insert dummy models
models = [Model(model_name=name, model_description="Dummy Model", created_date=datetime.now()) for name in model_names]
session.add_all(models)
session.commit()

# Insert dummy files
files = [File(file_name=name, file_created_date=datetime.now(), file_type_id=random.choice([ft.file_type_id for ft in file_types])) for name in file_names]
session.add_all(files)
session.commit()

# Create machine-sensor mappings
machine_sensor_mappings = [
    MachineSensorMapping(machine_id=random.choice([m.machine_id for m in machines]), sensor_id=random.choice([s.sensor_id for s in sensors]))
    for _ in range(6)  # Insert 6 mappings
]
session.add_all(machine_sensor_mappings)
session.commit()

# Create machine-sensor-model mappings
machine_sensor_model_mappings = [
    MachineSensorModelMapping(
        machine_id=random.choice([m.machine_id for m in machines]),
        sensor_id=random.choice([s.sensor_id for s in sensors]),
        model_id=random.choice([mod.model_id for mod in models])
    )
    for _ in range(6)  # Insert 6 mappings
]
session.add_all(machine_sensor_model_mappings)
session.commit()

# Insert dummy predictions
predictions = [
    Predictions(
        machine_id=random.choice([m.machine_id for m in machines]),
        sensor_id=random.choice([s.sensor_id for s in sensors]),
        model_id=random.choice([mod.model_id for mod in models]),
        file_id=random.choice([f.file_id for f in files]),
        prediction_type=random.choice(prediction_types),
        prediction_value=f"Prediction {i+1}",
        created_date=datetime.now()
    )
    for i in range(10)  # Insert 10 predictions
]
session.add_all(predictions)
session.commit()

print("Dummy data inserted successfully.")
