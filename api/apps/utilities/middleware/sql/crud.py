# NOT IMPLEMENTED

# import abc
#
# from apps.extensions import sqldb
#
#
# class SQLABCCRUD(object):
#
#     @classmethod
#     def commit(cls):
#         try:
#             sqldb.session.commit()
#         except:
#             sqldb.session.rollback()
#             raise
#
#     @classmethod
#     def bulkcommit(cls, qty = 10000):
#         try:
#             if len(sqldb.session.new) % qty == 0:
#                 sqldb.session.commit()
#             else:
#                 pass
#         except:
#             raise
#
#     def update(self, obj):
#         sqldb.session.add(obj)
#         self.commit()
