from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, json
from models import db, Index, IndexData, Office
from datetime import datetime
import csv
import io
from sqlalchemy import exists
import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
import elasticsearch

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

def parse_date(date_str):
    """Parse different date formats and return year and month"""
    try:
        # Try to parse full date format (31.1.2025)
        if '.' in date_str:
            date_obj = datetime.strptime(date_str, '%d.%m.%Y')
            return date_obj.year, date_obj.month
        # Try to parse year only format (2025)
        else:
            year = int(date_str)
            return year, None
    except Exception as e:
        print(f"Error parsing date {date_str}: {e}")
        return None, None

def get_indices_status():
    """Get status for all indices comparing their last label with current date"""
    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month
    
    indices_info = {
        'offices': {},  # This will now be a nested dictionary by office
        'economy': {},
        'demography': {}
    }
    
    try:
        # First, get all offices with id < 100
        offices = db.session.query(Office).filter(Office.id < 100).all()
        # Initialize sub-dictionaries for each office
        indices_info['offices'] = {office.name: {} for office in offices}
        
        indices = db.session.query(Index).all()
        
        for index in indices:
            try:
                last_record = (db.session.query(IndexData)
                             .filter(IndexData.index_id == index.id)
                             .order_by(IndexData.label.desc(), IndexData.id.desc())
                             .first())
                
                index_data = {
                    'name': index.name,
                    'last_update': None,
                    'status': 'empty',
                    'is_kpi': index.is_kpi
                }

                if last_record:
                    year, month = parse_date(last_record.label)
                    
                    if year:
                        if month:
                            is_current = (year == current_year and 
                                        month == current_month)
                        else:
                            is_current = (year == current_year or year == current_year - 1)
                        
                        index_data.update({
                            'last_update': last_record.label,
                            'status': 'current' if is_current else 'outdated'
                        })
                    else:
                        index_data.update({
                            'last_update': last_record.label,
                            'status': 'error',
                            'error': 'Invalid date format'
                        })

                # Group assignment with office subdivision
                if index.office_id == 100:
                    indices_info['economy'][index.name] = index_data
                elif index.office_id == 101:
                    indices_info['demography'][index.name] = index_data
                elif index.office_id < 100:
                    # Get office name
                    office_name = next((office.name for office in offices if office.id == index.office_id), 'Other')
                    indices_info['offices'][office_name][index.name] = index_data
                    
            except Exception as e:
                error_data = {
                    'name': index.name,
                    'last_update': None,
                    'status': 'error',
                    'error': str(e)
                }
                
                if index.office_id == 100:
                    indices_info['economy'][index.name] = error_data
                elif index.office_id == 101:
                    indices_info['demography'][index.name] = error_data
                elif index.office_id < 100:
                    office_name = next((office.name for office in offices if office.id == index.office_id), 'Other')
                    indices_info['offices'][office_name][index.name] = error_data

    except Exception as e:
        print(f"Error getting indices: {e}")
    
    return indices_info

@admin_bp.route('/admin/dashboard')
def admin_dashboard():
    """Render admin dashboard with initial indices status"""
    try:
        indices_status = get_indices_status()
        print("Indices Status:", indices_status)  # Debug print
        return render_template('admin_screen.html', indices_status=json.dumps(indices_status))
    except Exception as e:
        print(f"Error in admin_dashboard: {e}")
        return render_template('admin_screen.html', indices_status=json.dumps({}))

@admin_bp.route('/admin/indices-status')
def get_indices_status_endpoint():
    """API endpoint for getting indices status"""
    try:
        return jsonify(get_indices_status())
    except Exception as e:
        print(f"Error in get_indices_status_endpoint: {e}")
        return jsonify({'error': str(e)}), 500

