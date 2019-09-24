from django.shortcuts import render
from rest_framework.views import APIView
import configparser
from LeaveManagement.settings import BASE_DIR
import os
import pyodbc
from django.http.response import JsonResponse
# Create your views here.

# this class contains utility functions
class Utils:

    # read config file
    def read_config(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(BASE_DIR, 'LeaveAPIs/config.ini'))
        return config

    # function for creating a database connection
    def create_db_connection(self):
        config = self.read_config()
        driver = config['SQL_Credentials']['driver']
        server = config['SQL_Credentials']['server']
        database = config['SQL_Credentials']['database']
        uid = config['SQL_Credentials']['uid']
        password = config['SQL_Credentials']['password']
        connection = pyodbc.connect(
            "driver={};server={};database={};uid={};PWD={}".format(driver, server, database, uid, password),
            autocommit=True)
        return connection

class ApplyForLeave(APIView):
    def __init__(self):
        self.leaverecordtable = 'leaveEntryManagement'
        self.leaveUserTable = 'leaveUserRecords'

    def get(self, request):
        pass

    def post(self, request):

        utils = Utils()
        try:
            dbconnection = utils.create_db_connection()
        except Exception as e:
            print('database connection error', e)
            return JsonResponse({'message':'error'})
        cursor = dbconnection.cursor()
        # columns_list = ['employeeId', 'leaveStartDate', 'leaveEndDate', 'leaveReason', 'attachment']
        # fetch ManagerId
        try:
            managerId = cursor.execute("select employeeManagerId from {tablename} where employeeId = {employee}".format(tablename=self.leaveUserTable, employee=request.data['employeeId']))
            managerId = managerId.fetchall()[0][0]
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'cannot retrieve managerid'})

        leaveQuery = """
            insert into {tableName}(employeeId,employeeManagerId, leaveStartDate, leaveEndDate, leaveReason, timeType)
            values('{employeeId}', '{manager}','{startdate}', '{enddate}', '{reason}', '{timeType}')
        """.format(tableName = self.leaverecordtable, employeeId=request.data['employeeId'], manager = managerId, startdate= request.data['leaveStartDate'], enddate=request.data['leaveEndDate']
                   , reason = request.data['leaveReason'], timeType= request.data['timeType'])
        try:
            cursor.execute(leaveQuery)
        except Exception as e:
            print(leaveQuery)
            print(e)
            return JsonResponse({"message": "cannot update database"})

        return JsonResponse({"message":'success'})




