import os
import shutil

class Logger:
    def __init__(self, output_folder, filename):
        self.output_folder = output_folder
        shutil.rmtree(output_folder,True)
        os.mkdir(output_folder)
        os.mkdir(output_folder + '/documentos')
        os.mkdir(output_folder + '/proceso')
        self.filename = filename
            
    def log(self, line):
        hs = open(self.output_folder + "/" + self.filename,"a")
        if(os.path.getsize(self.output_folder + "/" + self.filename) > 0):
            hs.write("\n"+line)
        else:
            hs.write(line)
        hs.close()