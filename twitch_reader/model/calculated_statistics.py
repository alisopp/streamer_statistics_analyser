from mongoengine import Document, DynamicField, StringField


class CalculatedStatistics(Document):

    observation_date = DynamicField()
    title_sub = StringField(unique=True)
    chart_data = DynamicField()