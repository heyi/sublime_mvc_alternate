import sublime, sublime_plugin, os

class AltFiles:
    def get_file_info(self):
        file_name = self.window.active_view().file_name()
        file_path = os.path.split(file_name)
        flist = file_path[1].split('.')
        return [file_path[0], flist[0], flist[-1]]

    def find_in_open_files(self, filename):
        for view in self.window.views():
            if view.file_name():
                basename = os.path.basename(view.file_name())
            if basename == filename:
                return view.file_name()
        return None

    def find_in_folders(self, filename):
        for folder in self.window.folders():
            full_path = self.find_in_folder(filename, folder)
            if full_path:
                return full_path
        return None

    def find_in_folder(self, filename, folder):
        for root, dirs, files in os.walk(folder):
            if filename in files:
                return os.path.join(root, filename)
        return None

    def switch_file(self, file_ext):
        file_info = self.get_file_info()
        if file_ext  ==  file_info[2]:
            return
        file_name = file_info[1] + "." + file_ext
        file_full_path = self.find_in_open_files(file_name)
        if file_full_path is None:
            file_full_path = self.find_in_folders(file_name)
        if file_full_path is None:
            file_full_path = file_info[0] + "/" + file_info[1] + "." + file_ext
            open(file_full_path, 'w+')
        self.window.open_file(file_full_path)

class AltHtmlCommand(sublime_plugin.WindowCommand, AltFiles):
    def run(self):
        AltFiles.switch_file(self, 'html')

class AltCssCommand(sublime_plugin.WindowCommand,AltFiles):
    def run(self):
        AltFiles.switch_file(self, 'css')

class AltJsCommand(sublime_plugin.WindowCommand,AltFiles):
    def run(self):
        AltFiles.switch_file(self, 'js')
