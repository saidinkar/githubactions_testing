from utilities.CustomLogging import getLogger

log = getLogger()
class FileReader:
    def __init__(self):
        pass

    def read_file(self,filePath, mode='r'):
        """
        Read data from the given file
       """
        log.info("Read the contents from the given file")
        with open(filePath, mode) as data_file:
            list_data = data_file.readlines()
        return list_data

    def write_file(self,filePath, listData, mode='r'):
        """
        Write given data to the file
        """
        log.info("Write the given data to the file")
        with open(filePath, mode) as out_data:
            for data in listData:
                out_data.write(data)