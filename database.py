from flask_pymongo import PyMongo, ObjectId # Import Flask-PyMongo utilities

# Exceptions
class InsertFailureException(Exception):
    pass

class QueryFailureException(Exception):
    pass

class DeleteFailureException(Exception):
    pass

class UpdateFailureException(Exception):
    pass

class Database:
    instance = None # Singleton pattern, instance holds a single occurence of the database
    mongoURI = "mongodb://localhost:27017/todo" # Indicates mongo server location and corresponding database, "todo"

    @staticmethod
    def getInstance(app):
        """
        Return the database instance if it has been instantiated.
        Otherwise, instantiate an instance and integrate to given Flask app.
        """
        if Database.instance is None:
            Database(app)
        return Database.instance
    
    @staticmethod
    def replaceObjectID(document):
        """
        Replace all _id values in a JSON-style dictionary document with 
        the MongoDB ObjectID type value. This is a requirement when using
        MongoDB's unique IDs.
        """
        for key in document:
            if isinstance(document[key], dict):
                Database.replaceObjectID(document[key]) # Recursively update nested documents
            elif key == "_id" and not isinstance(key, ObjectId): # Update entry matching {_id: "sdfr23hfk23f23"} to {_id: ObjectID("sdfr23hfk23f23")}
                document[key] = ObjectId(document[key])

    def __init__(self, app):
        """
        Initialize the database object and integrate into Flask app.
        """
        if Database.instance is not None:
            raise Exception("This class follows singleton patterns! Use getInstance.")   # Direct instantiation not allowed
        else:
            app.config["MONGO_URI"] = Database.mongoURI # Integrate Mongo with Flask
            self.db = PyMongo(app).db   # Save database value into object
            Database.instance = self    # Save the instance
    
    def insert(self, collection, document):
        """
        Insert a single document into the given collection within the db.
        Throws InsertFailureException on failure.
        """
        res = self.db[collection].insert_one(document)  # Insert using Mongo
        if not res.acknowledged:    # Ensure successful insert
            raise InsertFailureException("Failed to insert!")

    def query(self, collection, query = {}):
        """
        Locate a list of documents matching a query, from a given collection 
        in the db. By default, the query matches all documents in the collection.
        Throws QueryFailureException on failure. 
        """
        Database.replaceObjectID(query) # Update all _id keys for use with Mongo
        try:
            return list(self.db[collection].find(query))    # Find using Mongo and convert to list
        except TypeError:   # Ensure successful find
            raise QueryFailureException("TypeError was found!")

    def delete(self, collection, query):
        """
        Delete the first document from a collection in the db who matches a given query. 
        Throws DeleteFailureException on failure.
        """
        Database.replaceObjectID(query) # Update all _id keys for use with Mongo
        res = self.db[collection].delete_one(query) # Delete using Mongo
        if not res.acknowledged or res.deleted_count != 1:  # Ensure successful delete
            raise DeleteFailureException("Failed to delete!")

    def update(self, collection, query, document):
        """
        Update the first document from a collection in the db who matches a given query. 
        Throws UpdateFailureException on failure.
        """
        Database.replaceObjectID(query) # Update all _id keys for use with Mongo
        res = self.db[collection].update_one(query, document) # Update using Mongo
        if not res.acknowledged:    # Ensure successful update
            raise UpdateFailureException("Failed to update!")