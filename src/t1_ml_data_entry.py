from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from create_db import Model, MachineSensorModelMapping, Base
from sqlalchemy import text

# Database Connection (PostgreSQL)
DATABASE_URL = "postgresql://postgres:Finiteloop123@postgres:5432/norm_db_00"

# Create the engine and session
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def add_or_update_model(
    machine_id,
    sensor_id,
    model_name,
    model_description,
    model_repository_url,
    model_branch,
    model_version=None,
    model_type=None,
    commit_hash=None  # New parameter for commit hash
):
    try:
        # Step 1: Insert or update the model in the Model table
        model = session.query(Model).filter_by(model_name=model_name).first()
        
        if model:
            # Update existing model details
            model.model_description = model_description
            model.model_repository_url = model_repository_url
            model.model_branch = model_branch
            model.model_version = model_version
            model.model_type = model_type
            model.commit_hash = commit_hash  # Update commit hash
            session.commit()  # Commit the update
            print(f"Updated existing model: {model_name}")
        else:
            # Add new model
            model = Model(
                model_name=model_name,
                model_description=model_description,
                model_repository_url=model_repository_url,
                model_branch=model_branch,
                model_version=model_version,
                model_type=model_type,
                commit_hash=commit_hash  # Set commit hash for new model
            )
            session.add(model)
            session.commit()  # Commit here to get model_id for mapping
            print(f"Added new model: {model_name}")

        # Step 2: Create a new machine-sensor-model mapping
        mapping = MachineSensorModelMapping(
            machine_id=machine_id,
            sensor_id=sensor_id,
            model_id=model.model_id
        )
        session.add(mapping)
        session.commit()
        print(f"Machine-Sensor-Model mapping added for model: {model_name}, machine ID: {machine_id}, sensor ID: {sensor_id}")
        
    except IntegrityError as e:
        session.rollback()
        print("Error: Integrity constraint violated. Ensure that machine, sensor, and model IDs are valid.")
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()

# Example usage with commit_hash
add_or_update_model(
    machine_id=1,
    sensor_id=1,
    model_name="TorchAutoEncoderModel",
    model_description="shallow model",
    model_repository_url="https://github.com/finite-loop/telescopii-mcm-model-builder.git",
    model_branch="org1",
    model_version="v1.0",
    model_type="Autoencoder",
    commit_hash="2ecf2acb058ce6274dcba46b106a37c53c66101e"  # Example commit hash
)
