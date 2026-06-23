import os
import json
import uuid
import shutil
import time
from datetime import datetime
from fastapi import UploadFile
import boto3

UPLOADS_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'uploads')
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'citizen_reports.json')

class ReportService:
    """
    Handles Citizen Report ingestion, AI classification matching, and JSON storage.
    """

    @staticmethod
    def ensure_db():
        os.makedirs(UPLOADS_DIR, exist_ok=True)
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        if not os.path.exists(DB_PATH):
            with open(DB_PATH, 'w') as f:
                json.dump([], f)

    @staticmethod
    def _analyze_report_text(description: str, location: str) -> dict:
        """
        Deterministic keyword NLP logic to assign severity and violation type.
        Replaces external LLM to ensure hackathon prototype speed and reliability.
        """
        text = f"{description.lower()} {location.lower()}"
        
        # Violation Type Extraction
        if "double" in text or "parallel" in text:
            v_type = "Double Parking"
        elif "footpath" in text or "pavement" in text or "sidewalk" in text:
            v_type = "Footpath Blocked"
        elif "no parking" in text or "sign" in text:
            v_type = "No Parking Zone"
        elif "commercial" in text or "loading" in text or "truck" in text:
            v_type = "Commercial Loading"
        else:
            v_type = "Obstructive Parking"

        # Severity Extraction
        if "ambulance" in text or "emergency" in text or "hospital" in text or "accident" in text or "completely blocked" in text:
            severity = "Critical"
            status = "Patrol Dispatched"
        elif "traffic" in text or "jam" in text or "stuck" in text or "junction" in text:
            severity = "High"
            status = "Action Taken"
        elif "footpath" in text or "slow" in text:
            severity = "Medium"
            status = "Verified"
        else:
            severity = "Low"
            status = "Under Review"

        return {
            "violation_type": v_type,
            "severity": severity,
            "status": status
        }

    @staticmethod
    def submit_report(location: str, description: str, file: UploadFile = None) -> dict:
        ReportService.ensure_db()
        
        report_id = f"REP-{str(uuid.uuid4().int)[:4]}"
        file_path = None
        
        # Handle file storage
        evidence_path = None
        if file:
            extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
            filename = f"{report_id}.{extension}"
            
            s3_endpoint = os.getenv("R2_ENDPOINT_URL")
            s3_access_key = os.getenv("R2_ACCESS_KEY_ID")
            s3_secret_key = os.getenv("R2_SECRET_ACCESS_KEY")
            s3_bucket = os.getenv("R2_BUCKET_NAME")
            s3_public_domain = os.getenv("R2_PUBLIC_DOMAIN", "")

            if s3_endpoint and s3_access_key and s3_secret_key and s3_bucket:
                try:
                    s3 = boto3.client(
                        's3',
                        endpoint_url=s3_endpoint,
                        aws_access_key_id=s3_access_key,
                        aws_secret_access_key=s3_secret_key
                    )
                    s3.upload_fileobj(file.file, s3_bucket, filename)
                    if s3_public_domain:
                        evidence_path = f"https://{s3_public_domain}/{filename}"
                    else:
                        evidence_path = f"{s3_endpoint}/{s3_bucket}/{filename}"
                except Exception as e:
                    print(f"R2 Upload failed, falling back to local: {e}")
                    file_path = os.path.join(UPLOADS_DIR, filename)
                    file.file.seek(0)
                    with open(file_path, "wb") as buffer:
                        shutil.copyfileobj(file.file, buffer)
                    evidence_path = f"/uploads/{filename}"
            else:
                file_path = os.path.join(UPLOADS_DIR, filename)
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                evidence_path = f"/uploads/{filename}"
                
        # Analyze intelligence locally
        analysis = ReportService._analyze_report_text(description, location)
        
        # Generate Record
        record = {
            "id": report_id,
            "loc": location,
            "description": description,
            "type": analysis["violation_type"],
            "severity": analysis["severity"],
            "status": analysis["status"],
            "timestamp": datetime.now().isoformat(),
            "time": "Just now",  # For UI compatibility
            "evidence_path": evidence_path
        }
        
        # Save to JSON
        with open(DB_PATH, 'r') as f:
            db = json.load(f)
            
        db.insert(0, record)  # prepend latest
        
        with open(DB_PATH, 'w') as f:
            json.dump(db, f, indent=2)
            
        return record

    @staticmethod
    def get_all_reports() -> list:
        ReportService.ensure_db()
        with open(DB_PATH, 'r') as f:
            db = json.load(f)
            
        # Dynamically recalculate "time ago" for realism if desired, but for now just return
        return db
