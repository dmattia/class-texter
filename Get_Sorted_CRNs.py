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


def is_Valid(value, CRN_Numbers):
	start = 0
	end = len(CRN_Numbers) - 1
	middle = (end) / 2

	while start <= end:
		middle_value = CRN_Numbers[middle]
		if middle_value > value:
			end = middle - 1
			middle = (start + end) / 2
		elif middle_value < value:
			start = middle + 1
			middle = (start + end) / 2
		else:
			return True
	return False






