from datetime import *
from .models  import *
from random import randint
from openpyxl import load_workbook
from openpyxl import Workbook
#from pymesh import stl, obj

class Util:
    def handle_file(self, f, name, user, jobid):

        date = '_' + str(datetime.now().day) + '_' + str(datetime.now().month) + '_' + str(datetime.now().year) + '_' + str(datetime.now().hour)+ '_' + str(datetime.now().minute)+ '_' + str(datetime.now().second) + '_'

        name += date + user.first_name + '_' + user.last_name
        name  = str(jobid) + '_' + name

        path = 'UploadedFiles/' + name + '.stl'
        #path = 'The.stl'

        open(path, 'a').close()

        with open(path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        path1 = path
        path2 = 'static/JS/3DModels/' + name + '.obj'

        f2 = self.convertSTLtoOBJ(f)
        #f2 = self.saveSTLasOBJ(path1, path2, f)

        open(path2, 'a').close()

        with open(path2, 'wb+') as destination:
            for chunk in f2.chunks():
                destination.write(chunk)

        return(path1, path2)

    def convertSTLtoOBJ(self, f):
        return(f)
    #def saveSTLasOBJ(self, path1, path2, f):
    #    PyMesh = pymesh()
    #    mesh = PyMesh.load_mesh(path1)
    #    PyMesh.save_mesh(path2, mesh)
    #def saveSTLasOBJ(self, path1, path2, f):
        #mesh = pymesh.meshio.load_mesh(path1, drop_zero_dim=False)
        #pymesh.meshio.save_mesh(path2, mesh)
        #pymesh.test()
        #m = stl.Stl(path1)
        #m.save_obj(path2)


    def getPrintStartTime(self):
        return(datetime.now())

    def getPrintEndTime(self, f):
        return(datetime.now())

    def getPrinterName(self):
        printer = ['Thor', 'Artemis', 'Zeus']
        return(printer[randint(0, 2)])

    def getProfile(self, user):
        profiles = list(Profile.objects.all())

        for i in range(0, len(profiles)):
            if(profiles[i].equals(user)):
                return profiles[i]


    def getQuota(self, user):
        if(user.is_authenticated):
            profiles = list(Profile.objects.all())

            for i in range(0, len(list(profiles))):
                if(profiles[i].equals(user)):
                    profile = profiles[i]

            timeS = profile.quota

            timeH = str(int(timeS / 3600))
            timeS = timeS % 3600
            timeM = str(int(timeS / 60))
            timeS = str(timeS % 60)

            if(len(timeH) < 2):
                timeH = '0' + timeH
            if(len(timeM) < 2):
                timeM = '0' + timeM
            if(len(timeS) < 2):
                timeS = '0' + timeS

            quota = timeH + ':' + timeM + ':' + timeS

            #context = {'Quota' : '00:31:23'}
            return({'Quota' : quota})
        else:
            return({'Quota' : '--:--:--'})

    def changeGrade(self, diff):
        profiles = list(Profile.objects.all())

        for p in profiles:
            p.grade += diff
            p.save()


    """def readFrom(a,b):
          wb = load_workbook(filename=a)
          ws = wb[b]
          data=[]
          for i in range(1,len(list(ws.rows))):
             row=list(ws.rows)[i]
             k=[]
             for cell in row:
                k.append(cell.value)
             data.append(k)
          return(data)

    def writeTo(a,b,c):
       wb = load_workbook(a)
       ws = wb[b]
       for i in range(1,len(list(ws.rows))):
             row=list(ws.rows)[i]
             count=0
             print(len(list(row)))
             for cell in row:
                try:
                   cell.value=c[i-1][count]
                except:
                   cell.value=None
                count=count+1
       try:
          for j in range(i,len(c)):
             ws.append(c[j-1])
       except:
          print('')
       wb.save(a)"""


    def readFrom(self, file_name, sheet_name):
          wb = load_workbook(filename=file_name)
          ws = wb[sheet_name]
          data=[]
          for i in range(0,len(list(ws.rows))):
             row=list(ws.rows)[i]
             k=[]
             for cell in row:
                k.append(cell.value)
             data.append(k)
          return(data)

    def writeTo(self, file_name, file_data):
       wb = Workbook()
       ws = wb.active

       #file_name = 'InnovationHubWebsite/' + file_name

       for i in range(0,len(file_data)):
           ws.append(file_data[i])
           #print(file_data[i])
           #print('appending')
       wb.save(file_name)
