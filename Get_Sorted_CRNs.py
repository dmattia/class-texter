import requests
from bs4 import BeautifulSoup
from class_search_web_scrapping import  GetClasses, GetOptions

def Write_Courses():
	Options = GetOptions()
	subjects = Options[3].values()
	term = "201520"
	ATTR = '0ANY'
	Division = "UG"
	Campus = "M"
	Credit = "A"
	Courses = GetClasses(term, subjects, Credit, ATTR, Division, Campus)
	return Courses


def Get_Crns():
	Courses = Write_Courses()
	CRNs = {}
	Sorted_Crns = []

	for course in Courses:
		CRNs[course["CRN"]] = course["Title"] + "|" + course["Course - Sec"] + "|" + course["CRN"] + "|" + course["Opn"]
	
	Sorted_Crns = sorted(CRNs.keys())
	return Sorted_Crns, CRNs