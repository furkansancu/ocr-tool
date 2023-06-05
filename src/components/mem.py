import os, pathlib
import pickle

initial_data = {
    "tesseract_path": None
}

class MemoryHandler:
    def __init__(self):
        self.folderpath = pathlib.Path(os.getenv("APPDATA"), "OCRTool_fs")

        if not pathlib.Path.exists(self.folderpath):
            os.makedirs(self.folderpath)

        self.filename = "ocrtool_data.pkl"
        self.filepath = pathlib.Path(self.folderpath, self.filename)

        if not pathlib.Path.exists(self.filepath): 
            f = open(self.filepath, "a+")
            f.close()
            pickle.dump(initial_data, open( self.filepath, "wb" ))

    def GetData(self, dataname):
        data = pickle.load(open( self.filepath, "rb" ))
        return data[dataname]
    
    def SetData(self, dataname, datavalue):
        data = pickle.load(open( self.filepath, "rb" ))
        
        data[dataname] = datavalue
        pickle.dump(data, open( self.filepath, "wb" ))

        return self.GetData(dataname)