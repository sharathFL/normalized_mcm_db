from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import random

# Importing the table classes from create_db.py
from create_db import (
    FileType, MachineType, SensorType, File, Machine, Sensor, MachineSensorMapping, Base
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

def populate_initial_data():
    try:
        # Step 1: Insert File Types
        file_types = ["Audio", "Vibration"]
        file_type_records = [FileType(file_type_name=ft) for ft in file_types]
        session.add_all(file_type_records)
        session.commit()

        # Step 2: Insert Machine Types
        machine_types = ["CNC", "Drill", "Winch"]
        machine_type_records = [MachineType(machine_type_name=mt) for mt in machine_types]
        session.add_all(machine_type_records)
        session.commit()

        # Step 3: Insert Sensor Types
        sensor_types = ["Microphone", "Vibration Analyser"]
        sensor_type_records = [SensorType(sensor_type_name=st) for st in sensor_types]
        session.add_all(sensor_type_records)
        session.commit()

        # Step 4: Create 10 dummy machines
        machine_type_ids = [mt.machine_type_id for mt in session.query(MachineType).all()]
        if not machine_type_ids:
            raise ValueError("Machine types were not inserted properly.")
        
        machine_records = [
            Machine(
                machine_name=f"Machine_{i+1}",
                machine_type_id=random.choice(machine_type_ids),
                is_active=True,
                created_date=datetime.now()
            )
            for i in range(10)
        ]
        session.add_all(machine_records)
        session.commit()

        # Step 5: Create 20 dummy sensors
        sensor_type_ids = [st.sensor_type_id for st in session.query(SensorType).all()]
        if not sensor_type_ids:
            raise ValueError("Sensor types were not inserted properly.")
        
        sensor_records = [
            Sensor(
                sensor_name=f"Sensor_{i+1}",
                sensor_type_id=random.choice(sensor_type_ids),
                created_date=datetime.now()
            )
            for i in range(20)
        ]
        session.add_all(sensor_records)
        session.commit()

        # Step 6: Create mappings between machines and sensors
        machine_ids = [m.machine_id for m in session.query(Machine).all()]
        sensor_ids = [s.sensor_id for s in session.query(Sensor).all()]

        if not machine_ids or not sensor_ids:
            raise ValueError("Machines or Sensors were not inserted properly.")

        # Assign each machine 2-5 sensors, ensuring valid `machine_id` and `sensor_id`
        machine_sensor_mappings = []
        for machine_id in machine_ids:
            assigned_sensors = random.sample(sensor_ids, random.randint(2, 5))
            for sensor_id in assigned_sensors:
                machine_sensor_mappings.append(
                    MachineSensorMapping(machine_id=machine_id, sensor_id=sensor_id)
                )

        session.add_all(machine_sensor_mappings)
        session.commit()

        # Step 7: Create 100 dummy files linked to machine-sensor mappings
        file_type_ids = [ft.file_type_id for ft in session.query(FileType).all()]
        mapping_ids = [msm.id for msm in session.query(MachineSensorMapping).all()]

        file_records = [
            File(
                file_name=f"File_{i+1}",
                file_created_date=datetime.now(),
                file_type_id=random.choice(file_type_ids),
                machine_sensor_mapping_id=random.choice(mapping_ids)
            )
            for i in range(100)
        ]
        session.add_all(file_records)
        session.commit()

        print("Files, Machines, Sensors, and Mappings populated successfully.")
        
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    clear_existing_data()
    populate_initial_data()
