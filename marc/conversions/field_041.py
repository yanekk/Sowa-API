def setLanguage(record):
    data = record.field("008", True).data
    language_field = record.field("041", True)
    if not language_field.subfield("a", True):
        if language_field.subfield("h", True):
            record.field("008", True).data = data[0:35] + language_field.subfield("h", True).data + data[38:]
            return
    record.field("008", True).data = data[0:35] + language_field.subfield("a", True).data + data[38:]

