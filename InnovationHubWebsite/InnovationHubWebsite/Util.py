class Util:
    def handle_file(self, f, name):
        path = 'UploadedFiles/' + name + '.stl'
        #path = 'The.stl'

        open(path, 'a').close()

        with open(path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        return(path)
