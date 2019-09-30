"""
Module for M5DB query utilities
Author: Prasanna Kumar Tripathy
"""

from DBConnection import DBConnection


class DBComponent(object):

    def dbconnect(self, **params):
        """
        :param params: required parameters to establish the connection with the m5db
        :return: True / False
        :Author: Prasanna
        """
        # Check the mandatory parameters
        if (not params.get('hostname', None) or
                not params.get('port', None) or
                not params.get('username', None) or
                not params.get('password', None) or
                not params.get('dbname', None)):
            return False

        status = True
        try:
            if params.get('db_type', None):
                self.db = DBConnection(params['db_type'])
            else:
                self.db = DBConnection()

            # Connect to the DB
            self.db.connect(params['hostname'], params['port'],
                              params['username'], params['password'],
                              params['dbname'])
        except Exception as e:
            print(e)
            status = False
        return status

    def dbquery(self, query, result_as_dict=True):
        """
        :param query: db query to be executed
        :param result_as_dict: Whether the query result is desired in dictionary
        :return: status and query result
        """
        # verify the mandatory parameter. Query except 'SELECT' is not allowed
        if 'select' != query.strip().split(' ')[0].lower():
            return False, None

        try:
            data = self.db.execute_query(query, result_as_dict)
            if not data:
                raise Exception("db query failed!!")
        except Exception as e:
            print(e)
            return False, None

        return True, data



