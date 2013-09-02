import sublime
import sublime_plugin


class SortListCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        prepend = append = ''
        region = self.view.sel()[0]
        selection = self.view.substr(region)

        if selection:
            if selection[0] == '(' or selection[0] == '[':
                prepend = selection[0]

            if selection[-1] == ')' or selection[-1] == ']':
                append = selection[-1]

            txt_list = selection
            if prepend:
                txt_list = txt_list[1:]
            if append:
                txt_list = txt_list[0:-1]
        else:
            p1 = 0
            p2 = self.view.size()
            cursor = self.view.sel()[0].begin()
            text = self.view.substr(sublime.Region(p1, p2))

            for i in range(cursor, p1, -1):
                c = text[i]
                if c in ('[', '('):
                    p1 = i+1
                    break
            for i in range(cursor, p2):
                c = text[i]
                if c in (']', ')'):
                    p2 = i
                    break
            txt_list = text[p1:p2]
            region = sublime.Region(p1, p2)

        txt_list = txt_list.split(',')

        for key, value in enumerate(txt_list):
            txt_list[key] = value.strip()

        txt_list.sort()

        while '' in txt_list:
            txt_list.remove('')

        result = "%s%s%s" % (prepend, ', '.join(txt_list), append)

        self.view.replace(edit, region, result)
