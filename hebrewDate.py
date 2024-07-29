from datetime import datetime


def get_date(): # return today's date
    return datetime.today()

def getJewishMonthName(month, year):
  if month == 1:
    return "ניסן"
  elif month == 2:
    return "אייר"
  elif month == 3:
    return "סיון"
  elif month == 4:
    return "תמוז"
  elif month == 5:
    return "אב"
  elif month == 6:
    return "אלול"
  elif month == 7:
    return "תשרי"
  elif month == 8:
    return "חשוון"
  elif month == 9:
    return "כסלו"
  elif month == 10:
    return "טבת"
  elif month == 11:
    return "שבט"
  elif month == 12:
    if leap_year(year):
      return "אדר א'"
    else:
      return "אדר"
    
  elif month == 13:
    return "אדר ב'"


def leap_year(year):
  if year % 4 == 0 and year / 100 != 0 or year % 400 == 0:
    return True
  return False

def get_hebrewDate():
    today = get_date()
    day = today.day
    month = today.month
    year = today.year

    hebrew_month = getJewishMonthName(month,year)
    print(hebrew_month)
get_hebrewDate()
