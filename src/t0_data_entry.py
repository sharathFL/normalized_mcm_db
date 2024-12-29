from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import random

# Import the table classes from create_db.py
from create_db import (
    FileType, MachineType, SensorType, Machine, Sensor, MachineSensorMapping, File, Base
)

# Database Connection (PostgreSQL)
DATABASE_URL = "postgresql://postgres:Finiteloop123@postgres:5432/norm_db_00"

# Create the engine and session
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def clear_existing_data():
    """Clear all existing data in the tables to avoid duplicates."""
    try:
        # Use SQLAlchemy text() for raw SQL execution
        session.execute(text("TRUNCATE TABLE machine_sensor_mapping, sensor, machine, file, sensor_type, machine_type, file_type RESTART IDENTITY CASCADE;"))
        session.commit()
        print("Existing data cleared.")
    except Exception as e:
        session.rollback()
        print(f"Error clearing existing data: {e}")

def simulate_data(machine_name, machine_type_name, sensor_type_name, file_type_name, sensor_names):
    try:
        # Step 1: Insert File Type
        file_type = FileType(file_type_name=file_type_name)
        session.add(file_type)
        session.commit()

        # Step 2: Insert Machine Type
        machine_type = MachineType(machine_type_name=machine_type_name)
        session.add(machine_type)
        session.commit()

        # Step 3: Insert Sensor Type
        sensor_type = SensorType(sensor_type_name=sensor_type_name)
        session.add(sensor_type)
        session.commit()

        # Step 4: Insert Machine with specified machine type
        machine = Machine(
            machine_name=machine_name,
            machine_type_id=machine_type.machine_type_id,
            is_active=True,
            created_date=datetime.now()
        )
        session.add(machine)
        session.commit()

        # Step 5: Insert Sensors with specified sensor type and add machine-sensor mappings
        sensors = []
        for sensor_name in sensor_names:
            sensor = Sensor(
                sensor_name=sensor_name,
                sensor_type_id=sensor_type.sensor_type_id,
                created_date=datetime.now()
            )
            session.add(sensor)
            session.commit()
            
            # Create machine-sensor mapping
            mapping = MachineSensorMapping(
                machine_id=machine.machine_id,
                sensor_id=sensor.sensor_id
            )
            session.add(mapping)
            sensors.append(sensor)
        session.commit()

        # Step 6: Generate 100 random files
        for i in range(100):
            file = File(
                file_name=f"File_{i+1}",
                file_created_date=datetime.now(),
                file_type_id=file_type.file_type_id,
                machine_sensor_mapping_id=random.choice([m.id for m in session.query(MachineSensorMapping).all()])
            )
            session.add(file)

        session.commit()
        print("Data simulation complete with 100 random files generated.")
        
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    clear_existing_data()  # Clear existing data to start fresh
    simulate_data(
        machine_name="CNC_1",
        machine_type_name="CNC",
        sensor_type_name="Microphone",
        file_type_name="Audio",
        sensor_names=["Sensor_A",]  # Add sensors to be associated with the machine
    )
