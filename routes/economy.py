from flask import Blueprint, render_template
from models import db, IndexData

economy_bp = Blueprint('economy', __name__)

@economy_bp.route('/economy')
def economy():
   
    # Main Graph data
    main_labels = []
    main_values = []
    temp_values = []
    
    debt_per_year = db.session.query(IndexData).filter_by(index_id=5).all()
    income_per_year = db.session.query(IndexData).filter_by(index_id=6).all()
    expenses_per_year = db.session.query(IndexData).filter_by(index_id=7).all()
    interest_per_year = db.session.query(IndexData).filter_by(index_id=8).all()
    gdp_per_year = db.session.query(IndexData).filter_by(index_id=9).all()

    indexes = []
    indexes.append(debt_per_year)
    indexes.append(income_per_year)
    indexes.append(expenses_per_year)
    indexes.append(interest_per_year)
    indexes.append(gdp_per_year)


    for row in income_per_year:
        main_labels.append(row.label)

    for index in indexes: 
        for row in index:  
            temp_values.append(row.value)
        main_values.append(temp_values)
        temp_values = []
    

    last_year_expenses = db.session.query(IndexData).filter_by(index_id=10).all()
    expenses_lables = []
    expenses_values = []
  
    for row in last_year_expenses:
        expenses_lables.append(row.label)
        expenses_values.append(row.value)
    
    last_year_income = db.session.query(IndexData).filter_by(index_id=11).all()
    income_lables = []
    income_values = []

    for row in last_year_income:
        income_lables.append(row.label)
        income_values.append(row.value)

    return render_template('economy.html', main_lables=main_labels, main_values=main_values, expenses_lables=expenses_lables, expenses_values=expenses_values,income_lables=income_lables,income_values=income_values)

