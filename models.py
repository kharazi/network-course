from mongoengine import Document, StringField, ReferenceField


class FileModel(Document):

    name = StringField(required=True, max_length=100)
    checksum = StringField(required=True, max_length=32)
    client = ReferenceField('ClientModel', required=True)


class ClientModel(Document):

    name = StringField(required=True)
    addr = StringField(required=True)