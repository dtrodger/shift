from abc import ABCMeta

from flask import current_app


class MongoCRUD(object):
    """
    API to handle core CRUD operations against MongoEngine models. Iterface to be inherited by Mongo middleware class.
    """

    __metaclass__ = ABCMeta

    @staticmethod
    def create(document, **kwargs):
        """
        Initializes an MongoEngine Document instance, save Document to database.

        Arguments:
            document (mongodb.Document)

        Key Word Arguments:
            **kwargs: MongoEngine model attribute names and values

        Return:
            new_document (mongodb.Document) if successful save, else (False)
        """

        try:
            # Initialize Document
            new_document = document(**kwargs)

            # Save to MongoDB
            new_document.save()
        except Exception as e:
            current_app.logger.error('Mongo - {}'.format(e.message))

            return False

        return new_document

    @staticmethod
    def get_first(document, **kwargs):
        """
        Query to return first MongoEngine model matching query.

        Arguments:
            document (mongodb.Document)

        Key Word Arguments:
            **kwargs: query parameters

        Return:
            document (mongodb.Document) if successful save, else (False)
        """

        try:
            # Query MongoDB.
            document = document.objects(**kwargs).first()
        except Exception as e:
            current_app.logger.error('Mongo - {}'.format(e.message))

            return False

        return document

    @staticmethod
    def get_all(document, **kwargs):
        """
        Query to return all MongoEngine models matching query.

        Arguments:
            document (mongodb.Document)

        Key Word Arguments:
            **kwargs: query parameters

        Return:
            documents (list) if successful save, else (False)
        """

        try:
            # Query MongoDB.
            documents = document.objects(**kwargs).all()
        except Exception as e:
            current_app.logger.error('Mongo - {}'.format(e.message))

            return False

        return documents

    @staticmethod
    def drop_collection(document):
        """
        Drops all collections associated with MongoEngine model.

        Arguments:
            document (mongodb.Document)

        Return:
            (True) if successful, else (False)
        """

        try:
            return document.drop_collection()

        except Exception as e:
            current_app.logger.error('Mongo - {}'.format(e.message))

            return False

    @staticmethod
    def update(document, **kwargs):
        """
        Updates MongoEngine model attributes. Saves changes to database.

        Arguments:
            document (MongoEngine model)

        Key Word Arguments:
            **kwargs: MongoEngine model attributes and associated values to update

        Return:
            document (MongoEngine model) if successful, else (False)

        """

        try:
            for attr, value in kwargs.iteritems():
                setattr(document, attr, value)

            document.save()

            return document
        except Exception as e:
            current_app.logger.error('Mongo - {}'.format(e.message))

            return False

    @staticmethod
    def delete(document):
        """
        Deletes MongoEngine Document.

        Arguments:
            document (MongoEngine Document)

        Return:
            (True) if successful delete, else (False)
        """

        try:
            # Delete MongEngine Document from database.
            return document.delete()
        except Exception as e:
            current_app.logger.error('Mongo - {}'.format(e.message))

            return False
