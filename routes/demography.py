from flask import Blueprint, render_template
from models import IndexData, Index, db

demography_bp = Blueprint('demography', __name__)

@demography_bp.route('/demography')
def demography():
    # Get all the indexes with office_id = 100
    demography_indexes = db.session.query(Index).filter_by(office_id=100).all()

    indexes_data = []

    for index in demography_indexes:
        # Get all related Indexes_Data entries for the current index
        index_data_entries = db.session.query(IndexData).filter_by(index_id=index.id).all()
        labels = []
        values = []
        # Collect labels and values from each entry
        for entry in index_data_entries:
            labels.append(entry.label)  # Assuming 'label' is the field name
            values.append(float(str(entry.value).replace(',', '').replace('%', '')))  # Assuming 'value' is the field name

        indexes_data.append({"index_id": index.id, "labels": labels, "values": values})

    return render_template('demography.html', indexes_data = indexes_data)