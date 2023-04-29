import logging
import io
import csv
class CsvFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        self.output = io.StringIO()
        self.writer = csv.writer(self.output,quoting=csv.QUOTE_ALL,delimiter=",")
    def format(self,record):
        row_value = [res for res in record.msg]
        self.writer.writerow(row_value)
        data = self.output.getvalue()
        self.output.truncate(0)
        self.output.seek(0)
        return data.strip()
    
# multiple logger for various application
readable_logger = logging.getLogger("readable_logger")
readable_logger.setLevel(logging.DEBUG)
readable_handler = logging.FileHandler("test1.csv",encoding="utf-8")
readable_handler.setFormatter(CsvFormatter())
readable_logger.addHandler(readable_handler)
readable_logger.info(["กกกกกก","ๅ/-ภ/-ภ2","test3"])
text_logger = logging.getLogger("text_logger")
text_logger.setLevel(logging.DEBUG)
text_handler = logging.FileHandler("test2.csv",encoding="utf-8")
text_handler.setFormatter(CsvFormatter())
text_logger.addHandler(text_handler)
text_logger.info(["กกกกกก","ๅ/-ภ/-ภ2","test3dddddd"])