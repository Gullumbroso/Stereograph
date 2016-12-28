import gspread
import re
from oauth2client.service_account import ServiceAccountCredentials
from algorithm.models import *


class Data:

    def __init__(self):
        self.nodes = set()
        self.edges = []
        self.edges = []
        self.edges = []
        self.populate_arrays()

    def num_of_search_to_weight(self, num_of_search):
        if num_of_search == "LOW":
            return 1
        elif num_of_search == "MEDIUM":
            return 1 / 5
        elif num_of_search == "HIGH":
            return 1 / 20

    def populate_arrays(self):
        scope = ['https://spreadsheets.google.com/feeds']

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            './local_static/A-Star_Algorithm-e13b7033c464.json', scope)

        gc = gspread.authorize(credentials)

        wks = gc.open_by_key("13zVMccgzUZ8oIk2V4joIVC3AiT98iXmMVMqau4Yfy6o")
        sheet = wks.sheet1

        phrases = sheet.col_values(1)
        num_of_searches = sheet.col_values(2)
        nodes = sheet.col_values(3)
        groups = sheet.col_values(4)
        opposite = sheet.col_values(5)

        re_exp = re.compile('(\w+) people are (\w+)')

        edges = []
        is_negation = False

        for i in range(1, sheet.row_count):
            phrase = phrases[i]
            matcher_is = re_exp.match(phrase)
            if matcher_is:
                if " not " in phrase:
                    is_negation = True
                    phrase = phrase.replace('not ', '')
                    matcher_is = re_exp.match(phrase)
                # a is b
                p1 = matcher_is.group(1)
                p2 = matcher_is.group(2)
                if p1 != p2:
                    weight = self.num_of_search_to_weight(num_of_searches[i])
                    edges.append((p1, p2, weight, is_negation))
                is_negation = False

        # for i in range(len(nodes)):
        #     if nodes[i] == '':
        #         continue
        #     c = Characteristic(value=nodes[i], group=groups[i], opposite=opposite[i])
        #     try:
        #         c.save()
        #     except ValueError:
        #         print(ValueError)
        for edge in edges:
            e = Edge(source=edge[0], destination=edge[1], weight=edge[2], is_negative=edge[3])
            try:
                e.save()
            except ValueError:
                print(ValueError)