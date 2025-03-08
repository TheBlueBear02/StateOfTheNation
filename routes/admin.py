from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from models import db, Index, IndexData, Office
from datetime import datetime
import csv
import io
from sqlalchemy import exists
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define the admin password (store securely in production)
admin_bp = Blueprint('admin', __name__)

# Get admin password from environment variable
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
if not ADMIN_PASSWORD:
    raise ValueError("ADMIN_PASSWORD environment variable is not set")

@admin_bp.route("/admin", methods=["GET", "POST"])
def admin():
    if "admin_logged_in" in session:
        indexes = db.session.query(Index).all()
        return render_template("admin-screen/admin_screen.html", indexes=indexes)  

    if request.method == "POST":
        password = request.form.get("password")
        if password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin.admin"))

        return render_template("admin-screen/admin_login.html", error="Incorrect password")

    return render_template("admin-screen/admin_login.html")

@admin_bp.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin.admin"))

@admin_bp.route("/upload_csv", methods=["POST"])
def upload_csv():
    try:
        office_id = request.form.get("office_id")
        index_id = request.form.get("index_id")
        file = request.files.get("csv_file")

        if not file or not office_id or not index_id:
            return jsonify({"error": "Missing required parameters"}), 400

        try:
            index_id = int(index_id)
        except ValueError:
            return jsonify({"error": "Invalid index_id"}), 400

        # Get existing dates from DB and standardize their format
        existing_records = db.session.query(IndexData).filter(IndexData.index_id == index_id).all()
        existing_dates = {}
        
        for record in existing_records:
            try:
                date_obj = datetime.strptime(record.label.strip(), "%d.%m.%Y").strftime("%d.%m.%Y")
                existing_dates[date_obj] = record.value
            except ValueError:
                date_obj = datetime.strptime(record.label.strip(), "%d.%m.%Y").strftime("%d.%m.%Y")
                existing_dates[date_obj] = record.value

        # Read file content
        file_content = file.read().decode("utf-8")
        file_stream = io.StringIO(file_content)
        csv_reader = csv.reader(file_stream)
        next(csv_reader, None)  # Skip header row if present

        new_rows = []
        invalid_rows = []
        duplicate_rows = []
        
        csv_data = list(csv_reader)

        for row in csv_data:
            if len(row) < 2:
                continue

            date_str, value = row[0].strip(), row[1].strip()
            
            try:
                date_obj = datetime.strptime(date_str, "%d.%m.%Y").strftime("%d.%m.%Y")
                
                if date_obj in existing_dates:
                    duplicate_rows.append(date_obj)
                else:
                    new_rows.append(IndexData(
                        index_id=index_id,
                        label=date_obj,
                        value=value
                    ))
                    existing_dates[date_obj] = value
            
            except ValueError:
                invalid_rows.append(date_str)
                continue

        # Save new rows to database
        if new_rows:
            db.session.bulk_save_objects(new_rows)
            db.session.commit()

        # Prepare response
        response = {
            "message": f"Processed CSV file successfully",
            "new_records": len(new_rows),
            "duplicates": len(duplicate_rows),
            "invalid_dates": len(invalid_rows),
            "total_csv_rows": len(csv_data)
        }

        if invalid_rows:
            response["invalid_rows"] = invalid_rows
        if duplicate_rows:
            response["duplicate_rows"] = duplicate_rows

        return jsonify(response), 200

    except Exception as e:
        print(f"Error processing CSV: {str(e)}")
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/add_index", methods=['POST'])
def add_index():
    try:
        index_name = request.form.get('index_name')
        is_kpi = request.form.get('kpi_policy') == "true"
        news_feed_id = request.form.get('news_feed_id')
        index_info = request.form.get('index_info')
        alert = request.form.get('alert') == "true"
        is_shown = request.form.get('is_shown') == "true"
        icon_url = request.form.get('icon_url')
        chart_type = request.form.get('chart_type')
        office_id = request.form.get('office_id')
        source = request.form.get('source')

        if not index_name or not office_id or not chart_type:
            return jsonify({"success": False, "error": "Index Name, Office, and Chart Type are required!"})

        new_index = Index(
            name=index_name,
            info=index_info,
            icon=icon_url,
            is_kpi=is_kpi,
            office_id=office_id,
            news_feed_id=news_feed_id,
            alert=alert,
            is_shown=is_shown,
            chart_type=chart_type,
            source=source
        )

        db.session.add(new_index)
        db.session.commit()

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@admin_bp.route("/get_offices", methods=["GET"])
def get_offices():
    return jsonify([{"id": o.id, "name": o.name} for o in Office.query.all()])

@admin_bp.route("/get_indexes/<int:office_id>", methods=["GET"])
def get_indexes(office_id):
    indexes = db.session.query(Index).filter_by(office_id=office_id).all()
    return jsonify([{"id": index.id, "name": index.name} for index in indexes])

@admin_bp.route("/get_index_data/<int:office_id>/<int:index_id>", methods=["GET"])
def get_index_data(office_id, index_id):
    try:
        # Verify the index belongs to the specified office
        index = db.session.query(Index).filter_by(id=index_id, office_id=office_id).first()
        if not index:
            return jsonify({"error": "Index not found for this office"}), 404

        # Get all data for this index, ordered by id
        index_data = db.session.query(IndexData)\
            .filter_by(index_id=index_id)\
            .order_by(IndexData.id)\
            .all()
        
        # Convert to list of dictionaries
        data = [{
            "id": item.id,
            "label": item.label,
            "value": item.value
        } for item in index_data]
        
        return jsonify(data)

    except Exception as e:
        print(f"Error fetching index data: {str(e)}")
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/delete_index_data/<int:row_id>", methods=["DELETE"])
def delete_index_data(row_id):
    try:
        # Find the record
        record = db.session.query(IndexData).get(row_id)
        if not record:
            return jsonify({"success": False, "error": "Record not found"}), 404

        # Delete the record
        db.session.delete(record)
        db.session.commit()

        return jsonify({"success": True, "message": "Record deleted successfully"})

    except Exception as e:
        db.session.rollback()
        print(f"Error deleting index data: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
