from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean, text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func

# Base declarative class
Base = declarative_base()

# File Types Table
class FileType(Base):
    __tablename__ = 'file_types'

    file_type_id = Column(Integer, primary_key=True)
    file_type_name = Column(String, nullable=False)

    files = relationship("File", back_populates="file_type")


# Files Table
class File(Base):
    __tablename__ = 'files'

    file_id = Column(Integer, primary_key=True)
    file_name = Column(String, nullable=False)
    file_created_date = Column(DateTime, default=func.now())
    file_type_id = Column(Integer, ForeignKey('file_types.file_type_id'))

    file_type = relationship("FileType", back_populates="files")


# Sensor Types Table
class SensorType(Base):
    __tablename__ = 'sensor_types'

    sensor_type_id = Column(Integer, primary_key=True)
    sensor_type_name = Column(String, nullable=False)

    sensors = relationship("Sensor", back_populates="sensor_type")


# Machine Types Table
class MachineType(Base):
    __tablename__ = 'machine_types'

    machine_type_id = Column(Integer, primary_key=True)
    machine_type_name = Column(String, nullable=False)

    machines = relationship("Machine", back_populates="machine_type")


# Machine Table
class Machine(Base):
    __tablename__ = 'machine'

    machine_id = Column(Integer, primary_key=True)
    machine_name = Column(String, nullable=False)
    machine_type_id = Column(Integer, ForeignKey('machine_types.machine_type_id'))
    is_active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=func.now())

    machine_type = relationship("MachineType", back_populates="machines")


# Sensor Table
class Sensor(Base):
    __tablename__ = 'sensor'

    sensor_id = Column(Integer, primary_key=True)
    sensor_name = Column(String, nullable=False)
    sensor_type_id = Column(Integer, ForeignKey('sensor_types.sensor_type_id'))
    created_date = Column(DateTime, default=func.now())

    sensor_type = relationship("SensorType", back_populates="sensors")


# Model Table to store machine learning models
class Model(Base):
    __tablename__ = 'model'

    model_id = Column(Integer, primary_key=True)
    model_name = Column(String, nullable=False)
    created_date = Column(DateTime, default=func.now())
    model_description = Column(String, nullable=True)


# Machine-Sensor Mapping Table
class MachineSensorMapping(Base):
    __tablename__ = 'machine_sensor_mapping'

    id = Column(Integer, primary_key=True)
    machine_id = Column(Integer, ForeignKey('machine.machine_id'))
    sensor_id = Column(Integer, ForeignKey('sensor.sensor_id'))

    machine = relationship("Machine")
    sensor = relationship("Sensor")


# Machine-Sensor-Model Mapping Table
class MachineSensorModelMapping(Base):
    __tablename__ = 'machine_sensor_model_mapping'

    id = Column(Integer, primary_key=True)
    machine_id = Column(Integer, ForeignKey('machine.machine_id'))
    sensor_id = Column(Integer, ForeignKey('sensor.sensor_id'))
    model_id = Column(Integer, ForeignKey('model.model_id'))

    machine = relationship("Machine")
    sensor = relationship("Sensor")
    model = relationship("Model")


# Predictions Table (Now includes machine, sensor, model, and file references)
class Predictions(Base):
    __tablename__ = 'predictions'

    prediction_id = Column(Integer, primary_key=True)
    machine_id = Column(Integer, ForeignKey('machine.machine_id'))
    sensor_id = Column(Integer, ForeignKey('sensor.sensor_id'))
    model_id = Column(Integer, ForeignKey('model.model_id'))
    file_id = Column(Integer, ForeignKey('files.file_id'))  # Added file reference
    prediction_type = Column(String, nullable=False)
    prediction_value = Column(String, nullable=False)
    created_date = Column(DateTime, default=func.now())

    machine = relationship("Machine")
    sensor = relationship("Sensor")
    model = relationship("Model")
    file = relationship("File")


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
    __tablename__ = 'roles'

    role_id = Column(Integer, primary_key=True)
    role_name = Column(String, nullable=False)


# User Roles (Association Table)
class UserRole(Base):
    __tablename__ = 'user_roles'

    user_id = Column(Integer, ForeignKey('mcm_user.user_id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.role_id'), primary_key=True)

    user = relationship("McmUser")
    role = relationship("Role")


# Database Connection (PostgreSQL)
DATABASE_URL = "postgresql://postgres:Finiteloop123@postgres:5432/norm_db_00"

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)

# Drop tables manually with CASCADE
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS files CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS model CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS machine_sensor_mapping CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS machine_sensor_model_mapping CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS sensor CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS machine CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS predictions CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS sensor_types CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS machine_types CASCADE;"))
    conn.execute(text('DROP TABLE IF EXISTS mcm_user CASCADE;'))
    conn.execute(text("DROP TABLE IF EXISTS roles CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS user_roles CASCADE;"))

# Create all tables again
Base.metadata.create_all(engine)

# Optional: Session management for future data insertion
Session = sessionmaker(bind=engine)
session = Session()

# You can now use `session.add()` and `session.commit()` to insert data into the tables.
