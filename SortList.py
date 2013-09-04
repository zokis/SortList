import sublime
import sublime_plugin


class SortListCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        prepend = append = ''
        region = self.view.sel()[0]
        selection = self.view.substr(region)

        if selection:
            if selection[0] in ('(', '['):
                prepend = selection[0]

            if selection[-1] in (')', ']'):
                append = selection[-1]

            txt_list = selection
            if prepend:
                txt_list = txt_list[1:]
            if append:
                txt_list = txt_list[:-1]
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

        list_items = txt_list.split(',')

        for key, value in enumerate(list_items):
            list_items[key] = value.strip()

        list_items.sort()
        columns_79 = 1
        for index, item in enumerate(list_items):
            columns_79 += len(item) + 2
            if columns_79 >= 79:
                if index:
                    list_items.insert(index-1, '\n')
                columns_79 = 1

        while '' in list_items:
            list_items.remove('')

        result = ', '.join(list_items) \
            .replace('\n,', '\n').replace(' \n ', '\n')
        self.view.replace(edit, region, "%s%s%s" % (prepend, result, append))
