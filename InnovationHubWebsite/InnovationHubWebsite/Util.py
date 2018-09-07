from datetime import *
from .models  import *
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
        return('Thor')

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
