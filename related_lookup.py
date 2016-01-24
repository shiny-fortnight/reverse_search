import sqlite3 as sql
import re, os

db = '../dab.sqlite3'
fileExists = os.path.isfile(db)

forum_table = 'forums'
ads_table = 'ads'

forum_columns = [4,6,7]
ads_columns = [4,4,6,9]

def _getPhoneNumber(inPhone):
    re.sub("\D", "", inPhone) 
    inPhone = inPhone.replace('-','')
    if inPhone[0] == '1':
        inPhone = inPhone[1:]
    assert len(inPhone) == 10
    return inPhone


class GetRelatedInfo:
    def __init__(self):
        self.con = sql.connect(db)
        self.cur = self.con.cursor()

    def checkPhoneNumber(self, number):
        """
        Input: a string representing a phone number
        Output: a dictionary with the structure:
            dict has two keys: 'ads' and 'forums'
            each key points to a list of related values to 
            the input number (Note: list can be empty
            
            Returned ads have the structure:
                [url, ad_title, ad_content, location]                

            Returned forum posts have the structure:
                [url, post_content, username]
        """
        outputDict = dict()
        outputDict['ads'] = list()
        outputDict['forums'] = list()
        
        if not fileExists:
            return outputDict

        try:
            cleaned = _getPhoneNumber(number)
        except AssertionError:
            raise ValueError("Invalid phone number input")
        
        ads_query = 'SELECT * FROM ' + ads_table + ' WHERE col_12 is ' + cleaned
        self.cur.execute(ads_query)
        ads_results = self.cur.fetchall()
        if len(ads_results) > 0:
            ads_lst = list()
            for result in ads_results:
                new_results = [(val if val is not '\N' else None) for key, val in enumerate(result) if key in ads_columns]
                ads_lst.append(new_results)
            outputDict['ads'] = ads_lst

        forum_query = 'SELECT * FROM ' + forum_table + ' WHERE col_12 is ' + cleaned
        self.cur.execute(forum_query)
        forum_results = self.cur.fetchall()
        if len(forum_results) > 0:
            for_lst = list()
            for result in forum_results:
                new_results = [(val if val is not '\N' else None) for key, val in enumerate(result) if key in forum_columns]
                for_lst.append(new_results)
            outputDict['forums'] = for_lst

        return outputDict

if __name__=="__main__":
    gri = GetRelatedInfo()
    print gri.checkPhoneNumber('7738926531')
    print gri.checkPhoneNumber('2284160022')
