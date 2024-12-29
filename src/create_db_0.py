from sqlalchemy import create_engine, text, Column, Integer, String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Define the base for model classes
Base = declarative_base()

# Define database models
class FileType(Base):
    __tablename__ = 'file_type'
    file_type_id = Column(Integer, primary_key=True)
    file_type_name = Column(String, nullable=False)

class MachineType(Base):
    __tablename__ = 'machine_type'
    machine_type_id = Column(Integer, primary_key=True)
    machine_type_name = Column(String, nullable=False)

class SensorType(Base):
    __tablename__ = 'sensor_type'
    sensor_type_id = Column(Integer, primary_key=True)
    sensor_type_name = Column(String, nullable=False)

class File(Base):
    __tablename__ = 'file'
    file_id = Column(Integer, primary_key=True)
    file_name = Column(String, nullable=False)
    file_created_date = Column(DateTime, default=func.now())
    file_type_id = Column(Integer, ForeignKey('file_type.file_type_id'), nullable=False)
    file_type = relationship("FileType")

class Machine(Base):
    __tablename__ = 'machine'
    machine_id = Column(Integer, primary_key=True)
    machine_name = Column(String, nullable=False)
    machine_type_id = Column(Integer, ForeignKey('machine_type.machine_type_id'), nullable=False)
    is_active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=func.now())
    machine_type = relationship("MachineType")

class Sensor(Base):
    __tablename__ = 'sensor'
    sensor_id = Column(Integer, primary_key=True)
    sensor_name = Column(String, nullable=False)
    sensor_type_id = Column(Integer, ForeignKey('sensor_type.sensor_type_id'), nullable=False)
    created_date = Column(DateTime, default=func.now())
    sensor_type = relationship("SensorType")

class Model(Base):
    __tablename__ = 'model'
    model_id = Column(Integer, primary_key=True)
    model_name = Column(String, nullable=False)
    model_description = Column(String)
    model_repository_url = Column(String, nullable=False)
    model_branch = Column(String, nullable=False)
    model_version = Column(String, nullable=True)
    model_type = Column(String, nullable=True)
    created_date = Column(DateTime, default=func.now())

class MachineSensorMapping(Base):
    __tablename__ = 'machine_sensor_mapping'
    id = Column(Integer, primary_key=True)
    machine_id = Column(Integer, ForeignKey('machine.machine_id'), nullable=False)
    sensor_id = Column(Integer, ForeignKey('sensor.sensor_id'), nullable=False)

class MachineSensorModelMapping(Base):
    __tablename__ = 'machine_sensor_model_mapping'
    id = Column(Integer, primary_key=True)
    machine_id = Column(Integer, ForeignKey('machine.machine_id'), nullable=False)
    sensor_id = Column(Integer, ForeignKey('sensor.sensor_id'), nullable=False)
    model_id = Column(Integer, ForeignKey('model.model_id'), nullable=False)

class Prediction(Base):
    __tablename__ = 'prediction'
    prediction_id = Column(Integer, primary_key=True)
    machine_id = Column(Integer, ForeignKey('machine.machine_id'), nullable=False)
    sensor_id = Column(Integer, ForeignKey('sensor.sensor_id'), nullable=False)
    model_id = Column(Integer, ForeignKey('model.model_id'), nullable=False)
    file_id = Column(Integer, ForeignKey('file.file_id'), nullable=False)
    prediction_type = Column(String, nullable=False)
    prediction_value = Column(String, nullable=True)
    created_date = Column(DateTime, default=func.now())


# User Table (Renamed to mcm_user)
class McmUser(Base):
    __tablename__ = 'mcm_user'

    user_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)


# Roles Table
class Role(Base):
    __tablename__ = 'role'

    role_id = Column(Integer, primary_key=True)
    role_name = Column(String, nullable=False)


# User Roles (Association Table)
class UserRole(Base):
    __tablename__ = 'user_role'

    user_id = Column(Integer, ForeignKey('mcm_user.user_id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('role.role_id'), primary_key=True)

    user = relationship("McmUser")
    role = relationship("Role")

# Database URL for connection to the default database (postgres)
DEFAULT_DATABASE_URL = "postgresql://postgres:Finiteloop123@postgres:5432/postgres"
TARGET_DATABASE_URL = "postgresql://postgres:Finiteloop123@postgres:5432/norm_db_00"

def create_database():
    # Connect to the default database to create norm_db_00 if it doesn't exist
    default_engine = create_engine(DEFAULT_DATABASE_URL)
    with default_engine.connect() as conn:
        conn.execute(text("COMMIT"))  # Needed for database creation
        conn.execute(text("CREATE DATABASE norm_db_00"))

    # Create tables in the norm_db_00 database
    engine = create_engine(TARGET_DATABASE_URL, echo=True)
    Base.metadata.create_all(engine)
    print("Database and tables created successfully.")

if __name__ == "__main__":
    try:
        create_database()
    except Exception as e:
        print(f"Error creating database or tables: {e}")
